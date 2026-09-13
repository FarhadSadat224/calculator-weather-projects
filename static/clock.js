const hourHand = document.querySelector("#hour-hand");
const minuteHand = document.querySelector("#minute-hand");
const secondHand = document.querySelector("#second-hand");
const digitalTime = document.querySelector("#digital-time");
const period = document.querySelector("#period");
const dateLabel = document.querySelector("#date-label");
const formatToggle = document.querySelector("#format-toggle");
const secondsToggle = document.querySelector("#seconds-toggle");

let use24Hour = true;
let showSeconds = true;

function pad(value) {
  return String(value).padStart(2, "0");
}

function updateClock() {
  const now = new Date();
  const milliseconds = now.getMilliseconds();
  const seconds = now.getSeconds() + milliseconds / 1000;
  const minutes = now.getMinutes() + seconds / 60;
  const hours = (now.getHours() % 12) + minutes / 60;

  hourHand.style.transform = `translateX(-50%) rotate(${hours * 30}deg)`;
  minuteHand.style.transform = `translateX(-50%) rotate(${minutes * 6}deg)`;
  secondHand.style.transform = `translateX(-50%) rotate(${seconds * 6}deg)`;
  secondHand.classList.toggle("is-hidden", !showSeconds);

  const displayHour = use24Hour ? now.getHours() : (now.getHours() % 12 || 12);
  const secondsText = showSeconds ? `:${pad(now.getSeconds())}` : "";
  digitalTime.textContent = `${pad(displayHour)}:${pad(now.getMinutes())}${secondsText}`;
  period.textContent = use24Hour ? "LOCAL / 24H" : `${now.getHours() >= 12 ? "PM" : "AM"} / LOCAL`;
  dateLabel.textContent = new Intl.DateTimeFormat(undefined, {
    weekday: "long", month: "long", day: "numeric", year: "numeric",
  }).format(now);

  requestAnimationFrame(updateClock);
}

function updateButton(button, active, activeText, inactiveText) {
  button.classList.toggle("is-active", active);
  button.setAttribute("aria-pressed", String(active));
  button.textContent = active ? activeText : inactiveText;
}

formatToggle.addEventListener("click", () => {
  use24Hour = !use24Hour;
  updateButton(formatToggle, use24Hour, "24 HOUR", "12 HOUR");
});

secondsToggle.addEventListener("click", () => {
  showSeconds = !showSeconds;
  updateButton(secondsToggle, showSeconds, "SECONDS ON", "SECONDS OFF");
});

updateClock();
