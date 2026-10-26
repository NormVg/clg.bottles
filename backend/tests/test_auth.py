from fastapi.testclient import TestClient

from app.main import app


def test_signup_creates_a_session(client):
    response = client.get("/api/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_duplicate_email_is_rejected(client):
    response = client.post(
        "/api/auth/signup",
        json={"name": "Other", "email": "test@example.com", "password": "secret123"},
    )

    assert response.status_code == 400


def test_login_with_wrong_password_is_rejected(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrong"},
    )

    assert response.status_code == 401


def test_login_after_logout_works(client):
    assert client.post("/api/auth/logout").status_code == 204
    assert client.get("/api/auth/me").status_code == 401

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "secret123"},
    )

    assert response.status_code == 200
    assert client.get("/api/auth/me").status_code == 200


def test_bookmarks_require_a_session():
    anonymous = TestClient(app)

    assert anonymous.get("/api/fs").status_code == 401
    assert anonymous.get("/api/folders").status_code == 401
