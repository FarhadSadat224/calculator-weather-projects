from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

app = Flask(__name__)

WEATHER_CODES = {
    0: ("Clear sky", "sun"),
    1: ("Mainly clear", "sun-cloud"),
    2: ("Partly cloudy", "sun-cloud"),
    3: ("Overcast", "cloud"),
    45: ("Foggy", "fog"),
    48: ("Rime fog", "fog"),
    51: ("Light drizzle", "rain"),
    53: ("Drizzle", "rain"),
    55: ("Heavy drizzle", "rain"),
    61: ("Light rain", "rain"),
    63: ("Rain", "rain"),
    65: ("Heavy rain", "rain"),
    71: ("Light snow", "snow"),
    73: ("Snow", "snow"),
    75: ("Heavy snow", "snow"),
    80: ("Rain showers", "rain"),
    81: ("Rain showers", "rain"),
    82: ("Heavy rain showers", "rain"),
    85: ("Snow showers", "snow"),
    86: ("Heavy snow showers", "snow"),
    95: ("Thunderstorm", "storm"),
    96: ("Thunderstorm with hail", "storm"),
    99: ("Thunderstorm with hail", "storm"),
}


def fetch_json(url: str, params: dict[str, str | int]) -> dict:
    response = requests.get(url, params=params, timeout=8)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Weather provider returned an invalid response")
    return payload


def get_weather(city: str) -> dict:
    locations = fetch_json(
        GEOCODING_URL,
        {"name": city, "count": 1, "language": "en", "format": "json"},
    ).get("results")
    if not locations:
        raise LookupError("City not found")

    location = locations[0]
    forecast = fetch_json(
        FORECAST_URL,
        {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "auto",
            "forecast_days": 1,
        },
    )
    current = forecast["current"]
    daily = forecast["daily"]
    code = int(current["weather_code"])
    condition, icon = WEATHER_CODES.get(code, ("Unknown conditions", "cloud"))

    return {
        "city": location["name"],
        "country": location.get("country", ""),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "condition": condition,
        "weather_code": code,
        "icon": icon,
        "high": daily["temperature_2m_max"][0],
        "low": daily["temperature_2m_min"][0],
        "units": {"temperature": "°C", "wind_speed": "km/h"},
    }


@app.get("/")
def index():
    return send_from_directory(STATIC_DIR, "weather.html")


@app.get("/api/weather")
def weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Enter a city name"}), 400

    try:
        return jsonify(get_weather(city))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except (requests.RequestException, KeyError, TypeError, ValueError):
        return jsonify({"error": "Weather service is temporarily unavailable"}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)