from pathlib import Path

from fastapi import FastAPI, HTTPException # pyright: ignore[reportMissingImports]
from fastapi.responses import FileResponse # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field # pyright: ignore[reportMissingImports]


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="Calculator API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class Calculation(BaseModel):
	left: float = Field(..., description="The first number")
	operator: str = Field(..., pattern=r"^[+\-*/]$")
	right: float = Field(..., description="The second number")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
	return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/calc")
async def calculate(calculation: Calculation) -> dict[str, float | str]:
	if calculation.operator == "+":
		result = calculation.left + calculation.right
	elif calculation.operator == "-":
		result = calculation.left - calculation.right
	elif calculation.operator == "*":
		result = calculation.left * calculation.right
	elif calculation.operator == "/":
		if calculation.right == 0:
			raise HTTPException(status_code=400, detail="Cannot divide by zero")
		result = calculation.left / calculation.right
	else:
		raise HTTPException(status_code=400, detail="Unsupported operator")

	return {
		"left": calculation.left,
		"operator": calculation.operator,
		"right": calculation.right,
		"result": result,
	}