"""Calls the running API and prints what it gets back.

Run it with the backend up: .venv/bin/python scripts/check_bookmarks.py
"""

import json
import urllib.request

BASE = "http://127.0.0.1:8000/api"


def call(method: str, path: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(BASE + path, data=data, method=method)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request) as response:
        raw = response.read()
        return response.status, json.loads(raw) if raw else None


def main() -> None:
    print("health:", call("GET", "/health"))
    print("create folder:", call("POST", "/folders", {"path": "/demo/inspo"}))
    print(
        "create link:",
        call(
            "POST",
            "/items",
            {"type": "link", "url": "https://example.com", "path": "/demo"},
        ),
    )
    print("list /demo:", call("GET", "/fs?path=/demo"))
    print("search:", call("GET", "/search?q=example"))

    folders = call("GET", "/folders")[1]
    demo = next(folder for folder in folders if folder["path"] == "/demo")
    print("delete folder:", call("DELETE", f"/folders/{demo['id']}"))


if __name__ == "__main__":
    main()
