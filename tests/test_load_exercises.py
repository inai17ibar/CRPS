"""Tests for _load_exercises helper."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from app.routers.exercises import _load_exercises


class TestLoadExercises:
    def test_loads_existing_language(self):
        """Python exercises should load successfully."""
        exercises = _load_exercises("python")
        assert isinstance(exercises, list)
        assert len(exercises) > 0

    def test_returns_empty_for_unknown_language(self):
        """Non-existent language should return empty list."""
        exercises = _load_exercises("nonexistent_lang_xyz")
        assert exercises == []

    def test_exercise_has_required_fields(self):
        """Each exercise should contain all required fields."""
        required_keys = {"id", "title", "description", "difficulty", "filename",
                         "code", "question", "choices", "correct", "explanation"}
        exercises = _load_exercises("python")
        for ex in exercises:
            missing = required_keys - set(ex.keys())
            assert missing == set(), f"Exercise {ex.get('id')} missing keys: {missing}"

    def test_exercise_ids_are_unique(self):
        """Exercise IDs must be unique within a language."""
        exercises = _load_exercises("python")
        ids = [e["id"] for e in exercises]
        assert len(ids) == len(set(ids)), "Duplicate exercise IDs found"

    def test_correct_index_within_choices_range(self):
        """correct index must be valid for the choices list."""
        exercises = _load_exercises("python")
        for ex in exercises:
            assert 0 <= ex["correct"] < len(ex["choices"]), (
                f"Exercise {ex['id']}: correct={ex['correct']} out of range "
                f"for {len(ex['choices'])} choices"
            )

    def test_difficulty_is_valid(self):
        """Difficulty must be one of easy, medium, hard."""
        exercises = _load_exercises("python")
        valid = {"easy", "medium", "hard"}
        for ex in exercises:
            assert ex["difficulty"] in valid, (
                f"Exercise {ex['id']}: invalid difficulty '{ex['difficulty']}'"
            )

    def test_choices_has_at_least_two(self):
        """Each exercise should have at least 2 choices."""
        exercises = _load_exercises("python")
        for ex in exercises:
            assert len(ex["choices"]) >= 2, (
                f"Exercise {ex['id']}: only {len(ex['choices'])} choice(s)"
            )
