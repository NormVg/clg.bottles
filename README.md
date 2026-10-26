# clg.bottles

A quiet bookmark manager for a college assignment: folders, links, notes,
and raw file uploads, with accounts and a landing page.

FastAPI + SQLite on the back, Vue 3 + TypeScript on the front.

## The product

bottles is a small, quiet place to keep the things you want to come back to.
It is built for one person at a desk: no feed, no recommendations, no social
layer. You open it, see your shelf, and put something on it.

The idea is a filesystem you actually enjoy using. Folders are paths
(`/design/inspo`), not a pile of tags. A link, a note, and a file are all
just rows on the same shelf, so there is one place to look and one search
box to use.

The flow is deliberately short:

1. The landing page says what the app is and gets out of the way.
2. You create an account; your shelf is yours alone.
3. You land on the root folder. Press `n` for a link, `t` for a note,
   `u` to upload, `f` for a folder, `/` to search.
4. Hover a row to see what is inside before you open it.
5. Everything persists in one SQLite file, so the app is the same on every
   reload and easy to back up.

The design follows the old bottles app: monochrome editorial, hairline
structure, lowercase labels, and motion that completes in small segments
rather than one long animation. The landing carries the living dither
texture and the gemstone mark; the app itself stays still so the content is
the only thing moving.

## What it does

- **landing** - a quiet home screen with the living dither texture and the
  gemstone bottle mark, themed light and dark.
- **accounts** - sign up with a name, email, and password. Each account has
  its own shelf; nobody sees anyone else's bookmarks.
- **folders** - a tree addressed by path (`/design/inspo`). Missing parents
  are created on the fly; renaming moves the whole subtree.
- **links** - saved with a url. The title comes from the hostname unless you
  give one; hover previews resolve the page's og:image.
- **notes** - a title and a body, expandable in the list. Paste text anywhere
  to save one instantly.
- **files** - drag a file anywhere onto the window, or use the upload form.
  Images and videos preview inline; everything is stored raw in the database.
- **hover previews** - the floating thumbnail follows the cursor: media
  images and videos preview from their own bytes, links resolve their
  og:image through the API.
- **search** - one box across items and folder paths.
- **theme** - light and dark, remembered in localStorage.

## Stack

- Backend: Python 3.13, FastAPI, SQLite with plain SQL, PBKDF2 passwords.
- Frontend: Vue 3 + TypeScript, Vite, pnpm, `@paper-design/shaders` for the
  dither and gem.
- No external services: no S3, no Postgres, no auth provider.

## Structure

    clg.bottles/
      backend/
        app/
          main.py              # app + router wiring
          modules/
            auth/              # signup, login, sessions
            bookmarks/         # folders, items, uploads, previews, search
          utils/               # db, paths, files, urls, security
        scripts/               # manual API check script
        tests/                 # pytest suite
        requirements.txt
      frontend/
        src/
          components/          # browser, rows, surfaces, landing, login
          components/ui/       # button, input, textarea, icon, toast, shaders
          composables/         # session, theme, toast, drop zone, hover preview
          api.ts               # fetch client
          types.ts             # wire types
        vite.config.ts         # dev proxy: /api -> 127.0.0.1:8000

## Getting started

### Backend

    cd backend
    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt
    .venv/bin/uvicorn app.main:app --reload

API at http://127.0.0.1:8000, interactive docs at http://127.0.0.1:8000/docs.

### Frontend

    cd frontend
    pnpm install
    pnpm dev

Open http://localhost:5173. Vite binds the IPv6 loopback only, so curl it via
`http://[::1]:5173` (browsers reach localhost normally).

### Tests and build

    cd backend && .venv/bin/pytest
    cd frontend && pnpm build

The check script exercises the running API end to end:

    cd backend && .venv/bin/python scripts/check_bookmarks.py

## API

| Method | Path | What it does |
| --- | --- | --- |
| POST | `/api/auth/signup` | create an account and start a session |
| POST | `/api/auth/login` | sign in |
| POST | `/api/auth/logout` | sign out |
| GET | `/api/auth/me` | the signed-in user |
| GET | `/api/fs?path=/` | list a folder |
| GET | `/api/folders` | every folder, path-ordered |
| POST | `/api/folders` | create a folder path (mkdir -p) |
| PATCH | `/api/folders/{id}` | rename a folder and its subtree |
| DELETE | `/api/folders/{id}` | delete a folder and its contents |
| POST | `/api/items` | create a link or note |
| PATCH | `/api/items/{id}` | rename or edit an item |
| DELETE | `/api/items/{id}` | delete an item |
| GET | `/api/items/{id}/preview` | the link's title and og:image |
| POST | `/api/media` | upload a file (multipart) |
| GET | `/api/media/{id}/raw` | the raw bytes |
| GET | `/api/media/{id}/download` | the file as an attachment |
| GET | `/api/search?q=` | search items and folders |

Every bookmark route needs a session; the browser sends the `session_token`
cookie automatically.

## Storage

Everything lives in `backend/app.db`: users, sessions, folders, items, and the
uploaded file bytes as BLOBs. There is no external storage and no uploads
folder. The database file is gitignored.

- Passwords: PBKDF2-SHA256 with a random salt, from the standard library.
- Sessions: a random token in an HttpOnly cookie, stored in the `sessions` table.
- Uploads: capped at 25 MB, stored raw in the `media` table.
- Previews: fetched server-side with a 5 second timeout and cached for 6 hours.

## Notes

- This folder is its own git repo nested under the shared `room/` parent. Run
  git from here, never from the parent.
- The project started as a port of an older Nuxt bottles app; the bookmark
  side was kept and the docs side was dropped.
- The dither and gem shaders are vendored from `@paper-design/shaders`.
