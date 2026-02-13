"""Tests for page endpoints."""

import pytest


@pytest.mark.anyio
async def test_index_page(client):
    """Top page should render and list python as a language."""
    resp = await client.get("/")
    assert resp.status_code == 200
    assert "python" in resp.text.lower()


@pytest.mark.anyio
async def test_exercise_list_page(client):
    """Exercise list should render with exercise titles."""
    resp = await client.get("/exercises/python")
    assert resp.status_code == 200
    # Should contain at least one exercise title from the JSON
    assert "リスト内包表記" in resp.text


@pytest.mark.anyio
async def test_exercise_list_unknown_language(client):
    """Listing exercises for unknown language should return 200 with empty list."""
    resp = await client.get("/exercises/unknown_lang")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_exercise_detail_page(client):
    """Exercise detail should render code and choices."""
    resp = await client.get("/exercises/python/1")
    assert resp.status_code == 200
    assert "language-python" in resp.text  # highlight.js class
    assert "choice-btn" in resp.text


@pytest.mark.anyio
async def test_exercise_detail_not_found(client):
    """Non-existent exercise ID should return 404."""
    resp = await client.get("/exercises/python/9999")
    assert resp.status_code == 404
