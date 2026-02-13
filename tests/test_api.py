"""Tests for the answer-check API."""

import pytest


@pytest.mark.anyio
async def test_correct_answer(client):
    """Submitting the correct choice should return correct=True."""
    # Exercise 1, correct answer is index 1
    resp = await client.post(
        "/api/exercises/python/1/check",
        json={"selected": 1},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["correct"] is True
    assert data["expected"] == 1
    assert data["explanation"] != ""


@pytest.mark.anyio
async def test_wrong_answer(client):
    """Submitting a wrong choice should return correct=False."""
    resp = await client.post(
        "/api/exercises/python/1/check",
        json={"selected": 0},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["correct"] is False
    assert data["expected"] == 1


@pytest.mark.anyio
async def test_check_nonexistent_exercise(client):
    """Checking an answer for a non-existent exercise should return error."""
    resp = await client.post(
        "/api/exercises/python/9999/check",
        json={"selected": 0},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_check_nonexistent_language(client):
    """Checking an answer for a non-existent language should return error."""
    resp = await client.post(
        "/api/exercises/unknown_lang/1/check",
        json={"selected": 0},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_check_missing_body(client):
    """Missing request body should return 422."""
    resp = await client.post("/api/exercises/python/1/check")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_all_exercises_correct_answers(client):
    """Verify that the correct index for every exercise is actually accepted."""
    from app.routers.exercises import _load_exercises

    exercises = _load_exercises("python")
    for ex in exercises:
        resp = await client.post(
            f"/api/exercises/python/{ex['id']}/check",
            json={"selected": ex["correct"]},
        )
        data = resp.json()
        assert data["correct"] is True, (
            f"Exercise {ex['id']} ({ex['title']}): "
            f"expected correct={ex['correct']} to be accepted"
        )
