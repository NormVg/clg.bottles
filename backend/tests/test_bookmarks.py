import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.db import get_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_database():
    connection = get_connection()
    connection.execute("DELETE FROM items")
    connection.execute("DELETE FROM folders")
    connection.execute("DELETE FROM media")
    connection.commit()
    connection.close()


def test_create_folder_creates_missing_parents():
    response = client.post("/api/folders", json={"path": "/Design/Inspo"})

    assert response.status_code == 201
    assert response.json()["path"] == "/design/inspo"

    listing = client.get("/api/fs", params={"path": "/design"}).json()
    assert [folder["name"] for folder in listing["folders"]] == ["inspo"]


def test_create_link_uses_hostname_as_default_title():
    client.post("/api/folders", json={"path": "/design"})

    response = client.post(
        "/api/items",
        json={"type": "link", "url": "https://www.example.com/page", "path": "/design"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "example.com"
    listing = client.get("/api/fs", params={"path": "/design"}).json()
    assert len(listing["items"]) == 1


def test_rename_folder_moves_its_subtree():
    client.post("/api/folders", json={"path": "/design/inspo"})
    folder = client.get("/api/fs").json()["folders"][0]

    response = client.patch(f"/api/folders/{folder['id']}", json={"name": "references"})

    assert response.status_code == 200
    assert response.json()["path"] == "/references"
    listing = client.get("/api/fs", params={"path": "/references"}).json()
    assert [child["name"] for child in listing["folders"]] == ["inspo"]


def test_delete_folder_removes_its_items():
    client.post("/api/folders", json={"path": "/design"})
    client.post(
        "/api/items",
        json={"type": "note", "title": "idea", "note": "hello", "path": "/design"},
    )
    folder = client.get("/api/fs", params={"path": "/design"}).json()["folder"]

    response = client.delete(f"/api/folders/{folder['id']}")

    assert response.status_code == 204
    assert client.get("/api/fs", params={"path": "/design"}).status_code == 404


def test_search_finds_items_and_folders():
    client.post("/api/folders", json={"path": "/design"})
    client.post(
        "/api/items",
        json={"type": "link", "url": "https://piedpiper.com", "title": "pied piper", "path": "/design"},
    )

    item_results = client.get("/api/search", params={"q": "pied"}).json()
    assert [item["title"] for item in item_results["items"]] == ["pied piper"]

    folder_results = client.get("/api/search", params={"q": "desi"}).json()
    assert [folder["path"] for folder in folder_results["folders"]] == ["/design"]


def test_update_and_delete_item():
    created = client.post(
        "/api/items", json={"type": "note", "title": "idea", "note": "hello"}
    ).json()

    updated = client.patch(f"/api/items/{created['id']}", json={"title": "better idea"}).json()
    assert updated["title"] == "better idea"
    assert updated["note"] == "hello"

    assert client.delete(f"/api/items/{created['id']}").status_code == 204
    assert client.get("/api/fs").json()["items"] == []
