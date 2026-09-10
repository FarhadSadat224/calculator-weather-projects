from unittest.mock import patch

import requests

from weather_app import app, get_weather


GEOCODE_RESPONSE = {
    "results": [{"name": "Lisbon", "country": "Portugal", "latitude": 38.72, "longitude": -9.14}]
}
FORECAST_RESPONSE = {
    "current": {
        "temperature_2m": 22.4,
        "apparent_temperature": 23.1,
        "relative_humidity_2m": 58,
        "weather_code": 2,
        "wind_speed_10m": 12.0,
    },
    "daily": {"temperature_2m_max": [25.0], "temperature_2m_min": [16.0]},
}


def test_weather_endpoint_returns_normalized_weather():
    with patch("weather_app.requests.get") as get:
        get.side_effect = [FakeResponse(GEOCODE_RESPONSE), FakeResponse(FORECAST_RESPONSE)]
        response = app.test_client().get("/api/weather?city=Lisbon")

    assert response.status_code == 200
    assert response.json["city"] == "Lisbon"
    assert response.json["condition"] == "Partly cloudy"
    assert response.json["icon"] == "sun-cloud"
    assert response.json["high"] == 25.0


def test_weather_endpoint_rejects_blank_city():
    response = app.test_client().get("/api/weather?city= ")

    assert response.status_code == 400
    assert response.json["error"] == "Enter a city name"


def test_weather_endpoint_returns_not_found_for_unknown_city():
    with patch("weather_app.requests.get", return_value=FakeResponse({})):
        response = app.test_client().get("/api/weather?city=Atlantis")

    assert response.status_code == 404


def test_weather_endpoint_hides_provider_failures():
    with patch("weather_app.requests.get", side_effect=requests.Timeout):
        response = app.test_client().get("/api/weather?city=Lisbon")

    assert response.status_code == 502
    assert response.json["error"] == "Weather service is temporarily unavailable"


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload