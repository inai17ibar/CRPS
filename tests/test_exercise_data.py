"""Tests to validate the integrity of exercise JSON data."""

import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _all_exercise_files():
    """Discover all exercises.json files."""
    return list(DATA_DIR.glob("*/exercises.json"))


@pytest.fixture(params=_all_exercise_files(), ids=lambda p: p.parent.name)
def exercise_file(request):
    path = request.param
    with open(path, encoding="utf-8") as f:
        return {"language": path.parent.name, "exercises": json.load(f)}


class TestExerciseDataIntegrity:
    def test_is_non_empty_list(self, exercise_file):
        """exercises.json should contain a non-empty list."""
        exercises = exercise_file["exercises"]
        assert isinstance(exercises, list)
        assert len(exercises) > 0

    def test_ids_are_sequential(self, exercise_file):
        """IDs should start at 1 and increment without gaps."""
        ids = sorted(e["id"] for e in exercise_file["exercises"])
        expected = list(range(1, len(ids) + 1))
        assert ids == expected, f"IDs {ids} are not sequential from 1"

    def test_code_is_non_empty_string(self, exercise_file):
        """Code field should be a non-empty string."""
        for ex in exercise_file["exercises"]:
            assert isinstance(ex["code"], str)
            assert len(ex["code"].strip()) > 0, f"Exercise {ex['id']} has empty code"

    def test_explanation_is_non_empty(self, exercise_file):
        """Each exercise should have a non-empty explanation."""
        for ex in exercise_file["exercises"]:
            assert ex.get("explanation", "").strip() != "", (
                f"Exercise {ex['id']} has empty explanation"
            )

    def test_no_duplicate_choices(self, exercise_file):
        """Choices within an exercise should be unique."""
        for ex in exercise_file["exercises"]:
            choices = ex["choices"]
            assert len(choices) == len(set(choices)), (
                f"Exercise {ex['id']} has duplicate choices"
            )
