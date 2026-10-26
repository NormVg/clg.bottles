from fastapi.testclient import TestClient

from app.main import app


def test_create_folder_creates_missing_parents(client):
    response = client.post("/api/folders", json={"path": "/Design/Inspo"})

    assert response.status_code == 201
    assert response.json()["path"] == "/design/inspo"

    listing = client.get("/api/fs", params={"path": "/design"}).json()
    assert [folder["name"] for folder in listing["folders"]] == ["inspo"]


def test_create_link_uses_hostname_as_default_title(client):
    client.post("/api/folders", json={"path": "/design"})

    response = client.post(
        "/api/items",
        json={"type": "link", "url": "https://www.example.com/page", "path": "/design"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "example.com"
    listing = client.get("/api/fs", params={"path": "/design"}).json()
    assert len(listing["items"]) == 1


def test_rename_folder_moves_its_subtree(client):
    client.post("/api/folders", json={"path": "/design/inspo"})
    folder = client.get("/api/fs").json()["folders"][0]

    response = client.patch(f"/api/folders/{folder['id']}", json={"name": "references"})

    assert response.status_code == 200
    assert response.json()["path"] == "/references"
    listing = client.get("/api/fs", params={"path": "/references"}).json()
    assert [child["name"] for child in listing["folders"]] == ["inspo"]


def test_delete_folder_removes_its_items(client):
    client.post("/api/folders", json={"path": "/design"})
    client.post(
        "/api/items",
        json={"type": "note", "title": "idea", "note": "hello", "path": "/design"},
    )
    folder = client.get("/api/fs", params={"path": "/design"}).json()["folder"]

    response = client.delete(f"/api/folders/{folder['id']}")

    assert response.status_code == 204
    assert client.get("/api/fs", params={"path": "/design"}).status_code == 404


def test_search_finds_items_and_folders(client):
    client.post("/api/folders", json={"path": "/design"})
    client.post(
        "/api/items",
        json={"type": "link", "url": "https://piedpiper.com", "title": "pied piper", "path": "/design"},
    )

    item_results = client.get("/api/search", params={"q": "pied"}).json()
    assert [item["title"] for item in item_results["items"]] == ["pied piper"]

    folder_results = client.get("/api/search", params={"q": "desi"}).json()
    assert [folder["path"] for folder in folder_results["folders"]] == ["/design"]


def test_create_note_keeps_title_and_body(client):
    response = client.post(
        "/api/items",
        json={"type": "note", "title": "idea", "note": "the text to keep"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["type"] == "note"
    assert body["title"] == "idea"
    assert body["note"] == "the text to keep"

    listing = client.get("/api/fs").json()
    assert listing["items"][0]["note"] == "the text to keep"


def test_update_and_delete_item(client):
    created = client.post(
        "/api/items", json={"type": "note", "title": "idea", "note": "hello"}
    ).json()

    updated = client.patch(f"/api/items/{created['id']}", json={"title": "better idea"}).json()
    assert updated["title"] == "better idea"
    assert updated["note"] == "hello"

    assert client.delete(f"/api/items/{created['id']}").status_code == 204
    assert client.get("/api/fs").json()["items"] == []


def test_users_only_see_their_own_bookmarks(client):
    client.post("/api/items", json={"type": "note", "title": "mine", "note": "secret"})

    other = TestClient(app)
    other.post(
        "/api/auth/signup",
        json={"name": "Other", "email": "other@example.com", "password": "secret123"},
    )

    assert other.get("/api/fs").json()["items"] == []
    assert client.get("/api/fs").json()["items"][0]["title"] == "mine"
