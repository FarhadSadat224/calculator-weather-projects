const expression = document.querySelector("#expression");
const result = document.querySelector("#result");
const message = document.querySelector("#message");

let left = "";
let operator = "";
let right = "";

function render() {
  expression.textContent = `${left || "0"} ${operator} ${right}`.trim();
  result.textContent = right || left || "0";
}

function addValue(value) {
  const target = operator ? "right" : "left";
  if (value === "." && (target === "left" ? left : right).includes(".")) return;
  if (target === "left") left += value;
  else right += value;
  message.textContent = "";
  render();
}

function chooseOperator(value) {
  if (!left) left = "0";
  operator = value;
  message.textContent = "";
  render();
}

async function calculate() {
  if (!left || !operator || !right) return;
  try {
    const response = await fetch("/api/calc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ left: Number(left), operator, right: Number(right) }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Calculation failed");
    expression.textContent = `${left} ${operator} ${right}`;
    result.textContent = String(data.result);
    left = String(data.result);
    operator = "";
    right = "";
  } catch (error) {
    message.textContent = error.message;
  }
}

function clear() { left = ""; operator = ""; right = ""; message.textContent = ""; render(); }
function backspace() {
  if (right) right = right.slice(0, -1);
  else if (operator) operator = "";
  else left = left.slice(0, -1);
  render();
}

document.querySelectorAll("[data-value]").forEach((button) => button.addEventListener("click", () => addValue(button.dataset.value)));
document.querySelectorAll("[data-operator]").forEach((button) => button.addEventListener("click", () => chooseOperator(button.dataset.operator)));
document.querySelector('[data-action="calculate"]').addEventListener("click", calculate);
document.querySelector('[data-action="clear"]').addEventListener("click", clear);
document.querySelector('[data-action="backspace"]').addEventListener("click", backspace);
document.addEventListener("keydown", (event) => {
  if (/^[0-9.]$/.test(event.key)) addValue(event.key);
  else if (["+", "-", "*", "/"].includes(event.key)) chooseOperator(event.key);
  else if (event.key === "Enter" || event.key === "=") calculate();
  else if (event.key === "Escape") clear();
  else if (event.key === "Backspace") backspace();
});

render();