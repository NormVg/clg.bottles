import os
import tempfile

# Point every test at a throwaway database before the app is imported.
os.environ["CLG_BOTTLES_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.utils.db import get_connection


@pytest.fixture(autouse=True)
def clean_database():
    connection = get_connection()
    connection.execute("DELETE FROM sessions")
    connection.execute("DELETE FROM items")
    connection.execute("DELETE FROM folders")
    connection.execute("DELETE FROM media")
    connection.execute("DELETE FROM users")
    connection.commit()
    connection.close()


@pytest.fixture
def client():
    """A signed-in client: every bookmark test starts with a real session."""
    test_client = TestClient(app)
    response = test_client.post(
        "/api/auth/signup",
        json={"name": "Test", "email": "test@example.com", "password": "secret123"},
    )
    assert response.status_code == 201
    return test_client
