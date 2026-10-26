# clg.bottles

FastAPI + Vue 3 project.

## Structure

- `backend/` - FastAPI app (Python 3.13) with a pytest suite
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

## How the two halves talk

The Vite dev server proxies `/api/*` to the FastAPI backend at
`http://127.0.0.1:8000` (see `frontend/vite.config.ts`), and the backend's
CORS allowlist covers only the two Vite dev origins. The home page fetches
`/api/health` on mount, so the whole stack is verified just by opening it.

For a production deployment, serve `frontend/dist` from FastAPI (or a
reverse proxy) and drop the dev proxy.
