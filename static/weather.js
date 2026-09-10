const form = document.querySelector("#weather-form");
const cityInput = document.querySelector("#city");
const result = document.querySelector("#weather-result");

const icons = { sun: "☼", "sun-cloud": "◌", cloud: "☁", fog: "≋", rain: "☂", snow: "❄", storm: "ϟ" };

function formatNumber(value) { return Number(value).toFixed(0); }

function renderWeather(weather) {
  result.innerHTML = `
    <article class="weather-card">
      <div>
        <h2 class="place">${weather.city}</h2>
        <span class="country">${weather.country}</span>
        <div class="condition-row">
          <div class="weather-icon" aria-label="${weather.condition}">${icons[weather.icon] || icons.cloud}</div>
          <div><p class="condition">${weather.condition}</p><p class="temperature">${formatNumber(weather.temperature)}${weather.units.temperature}</p></div>
        </div>
      </div>
      <div class="metrics">
        <div class="metric"><span class="metric-label">FEELS LIKE</span><span class="metric-value">${formatNumber(weather.feels_like)}${weather.units.temperature}</span></div>
        <div class="metric"><span class="metric-label">HUMIDITY</span><span class="metric-value">${weather.humidity}%</span></div>
        <div class="metric"><span class="metric-label">WIND</span><span class="metric-value">${formatNumber(weather.wind_speed)} ${weather.units.wind_speed}</span></div>
        <div class="metric"><span class="metric-label">TODAY / HIGH LOW</span><span class="metric-value">${formatNumber(weather.high)}° / ${formatNumber(weather.low)}°</span></div>
      </div>
    </article>`;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = cityInput.value.trim();
  if (!city) return;
  result.innerHTML = '<p class="loading">READING THE SKY...</p>';
  try {
    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to find that city");
    renderWeather(data);
  } catch (error) {
    result.innerHTML = `<p class="error">${error.message}</p>`;
  }
});