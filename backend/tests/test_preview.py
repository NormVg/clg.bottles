from app.modules.bookmarks.preview import IMAGE_PATTERNS, TITLE_PATTERNS, _first, _image


def test_preview_parsing_reads_og_tags():
    html = """
    <html><head>
      <meta property="og:title" content="Pied Piper Handbook" />
      <meta property="og:image" content="/images/cover.png" />
    </head></html>
    """

    assert _first(html, TITLE_PATTERNS) == "Pied Piper Handbook"
    assert _image(html, "https://piedpiper.com/handbook") == "https://piedpiper.com/images/cover.png"


def test_preview_requires_a_link(client):
    note = client.post(
        "/api/items", json={"type": "note", "title": "idea", "note": "hello"}
    ).json()

    response = client.get(f"/api/items/{note['id']}/preview")

    assert response.status_code == 404
