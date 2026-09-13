# Calculator, Weather, and Luxury Clock

A small collection of browser-based projects built with Python, HTML, CSS, and JavaScript.

## Projects

### Calculator

A responsive calculator UI backed by a FastAPI endpoint.

- FastAPI backend
- Basic arithmetic: addition, subtraction, multiplication, and division
- Keyboard input support
- Divide-by-zero validation

### Weather App

A live weather dashboard powered by the Open-Meteo API.

- Search by city
- Current temperature and condition
- Feels-like temperature, humidity, wind, and daily high/low
- No API key required

### Luxury Analog Clock

A responsive real-time analog clock with a clean watch-inspired interface.

- Smooth analog hour, minute, and second hands
- Digital time and date
- 12-hour and 24-hour modes
- Toggleable seconds hand
- Responsive layout for desktop and mobile

## Requirements

- Python 3.10 or newer
- A modern web browser

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/FarhadSadat224/calculator-weather-projects.git
cd calculator-weather-projects
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the environment with:

```powershell
.venv\Scripts\activate
```

## Run the Calculator and Clock

Start the FastAPI app:

```bash
uvicorn Calculator:app --reload
```

Open the calculator at:

```text
http://127.0.0.1:8000
```

Open the luxury clock at:

```text
http://127.0.0.1:8000/static/clock.html
```

## Run the Weather App

Open a second terminal, activate the virtual environment, and run:

```bash
python weather_app.py
```

Open the weather app at:

```text
http://127.0.0.1:5000
```

The weather API endpoint is:

```text
http://127.0.0.1:5000/api/weather?city=London
```

## Tests

Run the weather tests with:

```bash
python -m pytest
```

## Project Structure

```text
Calculator.py              FastAPI calculator server
weather_app.py             Flask weather server
static/index.html          Calculator interface
static/weather.html        Weather interface
static/clock.html          Luxury clock interface
static/app.js              Calculator behavior
static/weather.js          Weather behavior
static/clock.js            Clock behavior
static/styles.css          Calculator styles
static/weather.css         Weather styles
static/clock.css           Clock styles
test_weather_app.py        Weather API tests
requirements.txt           Python dependencies
```

## Data Source

Weather data is provided by [Open-Meteo](https://open-meteo.com/).
