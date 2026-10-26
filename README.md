# clg.bottles

A simple bookmark manager: folders, links, notes, and raw file uploads.
FastAPI + SQLite on the back, Vue 3 + TypeScript on the front.

## Structure

- `backend/` - FastAPI app (Python 3.13), SQLite, plain SQL
  - `app/modules/bookmarks/` - folders, items, uploads, search
  - `app/utils/` - database, path, and filename helpers
  - `tests/` - pytest suite
  - `scripts/` - manual API check script
- `frontend/` - Vue 3 + TypeScript on Vite (pnpm)

Git: this folder is its own repo nested under the shared `room/` parent, so run all git commands from here, never from the parent.

## Backend

```sh
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

API at http://127.0.0.1:8000, interactive docs at http://127.0.0.1:8000/docs.

Tests:

```sh
cd backend && .venv/bin/pytest
```

Check the running API:

```sh
cd backend && .venv/bin/python scripts/check_bookmarks.py
```

## Frontend

```sh
cd frontend
pnpm install
pnpm dev
```

Dev server at http://localhost:5173. Vite binds the IPv6 loopback only, so
curl it via `http://[::1]:5173` (browsers reach localhost normally).

Production build:

```sh
cd frontend && pnpm build
```

## What it does

- folders: a tree addressed by path (`/design/inspo`), created on the fly
- links: saved with a url, titled from the hostname unless you give one
- notes: a title and a body, expandable in the list
- uploads: raw files stored as BLOBs in the same SQLite database, up to 25 MB
- search: one box across items and folder paths
- theme: light and dark, remembered in localStorage

## API

| Method | Path | What it does |
| --- | --- | --- |
| GET | `/api/fs?path=/` | list a folder |
| GET | `/api/folders` | every folder, path-ordered |
| POST | `/api/folders` | create a folder path |
| PATCH | `/api/folders/{id}` | rename a folder |
| DELETE | `/api/folders/{id}` | delete a folder and its contents |
| POST | `/api/items` | create a link or note |
| PATCH | `/api/items/{id}` | rename or edit an item |
| DELETE | `/api/items/{id}` | delete an item |
| POST | `/api/media` | upload a file (multipart) |
| GET | `/api/media/{id}/raw` | the raw bytes |
| GET | `/api/media/{id}/download` | the file as an attachment |
| GET | `/api/search?q=` | search items and folders |

## Storage

Everything lives in `backend/app.db`: folders, items, and the uploaded file
bytes. There is no external storage and no uploads folder. The database file
is gitignored.
