def test_upload_creates_media_item_and_serves_bytes(client):
    client.post("/api/folders", json={"path": "/design"})

    response = client.post(
        "/api/media",
        files={"file": ("photo.png", b"fake-image-bytes", "image/png")},
        data={"path": "/design", "title": "photo"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["media"]["filename"] == "photo.png"
    assert body["item"]["type"] == "media"
    assert body["item"]["title"] == "photo"

    listing = client.get("/api/fs", params={"path": "/design"}).json()
    assert listing["items"][0]["media"]["filename"] == "photo.png"

    raw = client.get(f"/api/media/{body['media']['id']}/raw")
    assert raw.status_code == 200
    assert raw.content == b"fake-image-bytes"
    assert raw.headers["content-type"] == "image/png"

    download = client.get(f"/api/media/{body['media']['id']}/download")
    assert "attachment" in download.headers["content-disposition"]


def test_delete_media_item_removes_the_media_row(client):
    created = client.post(
        "/api/media",
        files={"file": ("note.txt", b"hello", "text/plain")},
        data={"path": "/", "title": "note"},
    ).json()

    client.delete(f"/api/items/{created['item']['id']}")

    assert client.get(f"/api/media/{created['media']['id']}/raw").status_code == 404
