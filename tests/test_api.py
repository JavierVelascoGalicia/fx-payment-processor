from fastapi.testclient import TestClient
from wallets_api.main import app
from wallets_api.database import drop_all_tables, create_all_tables

drop_all_tables()

test_client = TestClient(app)
create_all_tables()


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


def test_get_wallets_by_id():
    response = test_client.get("/wallets/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_get_user_by_id_error():
    response = test_client.get("/users/2222")
    assert response.status_code == 404


def test_create_wallet():
    response = test_client.post("/wallets/1", json={"currency": "MXN"})
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["balance"] == 0
    assert data["currency"] == "MXN"


def test_get_wallets_by_id_after_update():
    response = test_client.get("/wallets/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


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


def test_convert_wallet_to_usd():
    response = test_client.post("/wallets/1/convert",
                                json={"from_currency": "MXN", "to_currency": "USD", "amount": 1000})
    assert response.status_code == 200
    data = response.json()
    assert data["USD"] == 53
    assert round(data["MXN"], 2) == 17867.92


def test_withdraw_wallet():
    response = test_client.post("/wallets/1/withdraw",
                                json={"currency": "USD", "amount": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["currency"] == "USD"
    assert data["amount"] == 43


def test_get_wallet_balances():
    response = test_client.get("/wallets/1/balances")
    assert response.status_code == 200
    data = response.json()
    assert data["USD"] == 43
    assert round(data["MXN"], 2) == 17867.92


def test_get_wallet_balances_error():
    response = test_client.get("/wallets/2123123/balances")
    assert response.status_code == 404


def test_get_wallet_transactions():
    response = test_client.get("/wallets/1/transactions")
    assert response.status_code == 200


def test_delete_user():
    response = test_client.delete("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Ok"
    assert data["detail"] == "Resource deleted"


def test_get_user_deleted():
    response = test_client.get("/users/1")
    assert response.status_code == 400
    data = response.json()
    assert data["error"] == "User deleted"


def test_get_wallet_by_deleted_user():
    response = test_client.get("/wallets/1")
    assert response == 400
    data = response.json()
    assert data["error"] == "User deleted"
