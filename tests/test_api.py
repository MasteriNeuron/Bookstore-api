# tests/test_api.py
from fastapi.testclient import TestClient


def register_user(client: TestClient, email: str, password: str):
    return client.post(
        "/auth/register",
        json={"email": email, "password": password},
    )


def login(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    return client.post("/auth/token", data=data)


def test_health(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_register_and_login(client: TestClient):
    email = "test@example.com"
    password = "secret123"

    r = register_user(client, email, password)
    assert r.status_code == 200
    assert r.json()["email"] == email

    token_resp = login(client, email, password)
    assert token_resp.status_code == 200
    data = token_resp.json()
    assert "access_token" in data


def test_books_list_empty(client: TestClient):
    resp = client.get("/books")
    assert resp.status_code == 200
    assert resp.json() == []
