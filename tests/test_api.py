from fastapi.testclient import TestClient
from wallets_api.main import app

test_client = TestClient(app)


def test_create_user():
    response = test_client.post("/users", json={})
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data


def test_get_user_by_id():
    response = test_client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1


def test_delete_user():
    response = test_client.delete("/users/1")
    assert response.status_code == 200
