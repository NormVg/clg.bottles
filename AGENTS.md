# AGENTS.md

Rules for AI agents working in this repo. Read this before writing any code.

## What this project is

clg.bottles is a simple writing app built for a college assignment.

- Backend: FastAPI (Python 3.13) with SQLite and plain SQL.
- Frontend: Vue 3 + TypeScript on Vite (pnpm).

The code must stay simple enough that a beginner can read it and explain it.
Simple and working beats clever and fancy, every time. If a noob cannot
explain a line, rewrite that line.

## Hard rules

1. Keep every file under 200 lines. Split it into another file before it grows past that.
2. Write plain, explicit code, step by step. No clever one-liners, no magic, no fancy patterns.
3. Use simple OOP: one class per job, a plain `__init__`, a few small methods.
   No inheritance trees, no abstract classes, no design patterns.
4. Use simple raw SQL with Python's built-in `sqlite3`. No ORM, no query builder.
   One simple query at a time. If a query gets complicated, do two simple queries instead.
5. Keep tables flat and simple: `id INTEGER PRIMARY KEY`, plain text columns,
   `created_at TEXT`. Add a foreign key only when the assignment really needs it.
6. Put feature code in `backend/app/modules/<feature>/` and shared helpers in
   `backend/app/utils/`. `main.py` only creates the app and includes routers.
7. Every API endpoint gets a pytest test in `backend/tests/`.
8. Every feature gets a small runnable script in `backend/scripts/` that calls the
   real API and prints the result. Use Python's built-in `urllib.request`.
9. Write real, working code, not placeholders. If something is unfinished, say so.
10. Comments and docstrings: short, plain English, explain what the code does.
11. Do not add new dependencies unless really needed. Ask before adding anything heavy.
12. Frontend: one component per job, plain `ref` and `fetch`, no state libraries or UI kits.

## Layout

    clg.bottles/
      AGENTS.md
      README.md
      backend/
        app/
          main.py          # FastAPI app + router wiring only
          modules/         # one folder per feature: notes/, users/, ...
          utils/           # small shared helpers: db.py, validation.py, ...
        scripts/           # manual API check scripts
        tests/             # pytest tests, one file per feature
        pyproject.toml
        requirements.txt
      frontend/
        src/               # App.vue, main.ts, style.css, components/
        vite.config.ts     # dev proxy: /api -> http://127.0.0.1:8000

The SQLite database file is `backend/app.db`. It is gitignored; never commit it.
Uploaded files are stored as BLOBs in that same database. There is no external
storage and no uploads folder.

## Commands

Backend, from `backend/`:

    .venv/bin/uvicorn app.main:app --reload      # API on http://127.0.0.1:8000
    .venv/bin/pytest                             # run the tests
    .venv/bin/python scripts/check_notes.py      # run one check script

Frontend, from `frontend/`:

    pnpm dev      # dev server on http://localhost:5173 (proxies /api to :8000)
    pnpm build    # type-check + production build

## How to add a feature

1. Add the table in `app/utils/db.py` with a simple `CREATE TABLE IF NOT EXISTS`.
2. Add a class in `app/modules/<feature>/` that holds the SQL queries as methods.
3. Add the routes in `app/modules/<feature>/routes.py` and include the router in `app/main.py`.
4. Add a test in `tests/test_<feature>.py`.
5. Add a script in `scripts/check_<feature>.py`.
6. Run `pytest` and `pnpm build` before calling it done.

## Style example

Good - simple and obvious:

    class NoteRepository:
        def __init__(self, db_path):
            self.db_path = db_path

        def get_all(self):
            connection = sqlite3.connect(self.db_path)
            rows = connection.execute("SELECT id, title, body FROM notes").fetchall()
            connection.close()
            return rows

Bad - too clever:

    notes = [Note(**dict(zip(columns, row))) for row in rows if row[2] is not None]

## Git

- This folder is its own git repo. Run git from here, never from the parent `room/` repo.
- Commit after each coherent change. Never push without being asked.
