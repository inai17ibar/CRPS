# CRPS - Code Reading Practice System

コードリーディング練習システム。AIが生成したコードやOSSのコードを読み解く力を鍛えるためのWebアプリケーション。

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000

## Tech Stack

- **Backend:** Python / FastAPI
- **Frontend:** HTML / CSS / JS (Jinja2 templates)
- **Syntax Highlighting:** highlight.js

## Adding Exercises

Add JSON files to `data/<language>/exercises.json`. See `data/python/exercises.json` for the schema.
