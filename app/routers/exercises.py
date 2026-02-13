import json
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def _load_exercises(language: str) -> list[dict]:
    path = DATA_DIR / language / "exercises.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# --------------- Pages ---------------

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Top page – language / difficulty selection."""
    languages = [
        d.name for d in DATA_DIR.iterdir() if d.is_dir() and (d / "exercises.json").exists()
    ]
    return templates.TemplateResponse("index.html", {"request": request, "languages": languages})


@router.get("/exercises/{language}", response_class=HTMLResponse)
async def exercise_list(request: Request, language: str):
    """List exercises for a language."""
    exercises = _load_exercises(language)
    return templates.TemplateResponse(
        "exercise_list.html",
        {"request": request, "language": language, "exercises": exercises},
    )


@router.get("/exercises/{language}/{exercise_id}", response_class=HTMLResponse)
async def exercise_detail(request: Request, language: str, exercise_id: int):
    """Show a single exercise."""
    exercises = _load_exercises(language)
    exercise = next((e for e in exercises if e["id"] == exercise_id), None)
    if exercise is None:
        return HTMLResponse("Exercise not found", status_code=404)
    return templates.TemplateResponse(
        "exercise.html",
        {"request": request, "language": language, "exercise": exercise},
    )


# --------------- API ---------------

class AnswerRequest(BaseModel):
    selected: int


@router.post("/api/exercises/{language}/{exercise_id}/check")
async def check_answer(language: str, exercise_id: int, body: AnswerRequest):
    """Check if the selected choice is correct."""
    exercises = _load_exercises(language)
    exercise = next((e for e in exercises if e["id"] == exercise_id), None)
    if exercise is None:
        return {"error": "Exercise not found"}

    correct = exercise["correct"]
    is_correct = body.selected == correct
    return {
        "correct": is_correct,
        "expected": correct,
        "explanation": exercise.get("explanation", ""),
    }
