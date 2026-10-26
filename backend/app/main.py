from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .modules.auth.routes import router as auth_router
from .modules.bookmarks.routes import router as bookmarks_router
from .utils.db import init_db

init_db()

app = FastAPI(title="clg.bottles API")

# Vite dev-server origins only; tighten this list before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(bookmarks_router)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
