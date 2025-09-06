from fastapi.testclient import TestClient
from wallets_api.main import app

test_client = TestClient(app)


def test_create_user():
    response = test_client.post("/users", json={"user_id": 1})
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data


def test_get_user_by_id():
    response = test_client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1


def test_create_wallet():
    response = test_client.post("/wallets/1", json={"currency": "USD"})
    assert response.status_code == 200


def test_fund_wallet():
    response = test_client.post("/wallets/1/fund",
                                json={"currency": "USD", "amount": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 1000
    assert data["currency"] == "USD"


def test_convert_wallet():
    response = test_client.post("/wallets/1/convert",
                                json={"from_currency": "USD", "to_currency": "MXN", "amount": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["USD"] == 0
    assert round(data["MXN"], 2) == 18867.92


def test_withdraw_wallet():
    response = test_client.post("/wallets/1/withdraw",
                                json={"currency": "MXN", "amount": 10})
    assert response.status_code == 200
    


def test_get_wallet_balances():
    response = test_client.get("/wallets/1/balances")
    assert response.status_code == 200
    