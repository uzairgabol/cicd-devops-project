import pytest
from app import app, data_store


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def clear_data_store():
    data_store.clear()  # Reset the in-memory DB before each test


def test_create_item(client):
    res = client.post("/item", json={"id": "1", "name": "Test Item"})
    assert res.status_code == 201
    assert res.get_json()["item"]["name"] == "Test Item"


def test_create_duplicate_item(client):
    client.post("/item", json={"id": "2", "name": "Item 2"})
    res = client.post("/item", json={"id": "2", "name": "Item 2"})
    assert res.status_code == 400


def test_get_item(client):
    client.post("/item", json={"id": "3", "name": "Item 2"})
    res = client.get("/item/3")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Item 3"


def test_update_item(client):
    client.post("/item", json={"id": "4", "name": "Old Name"})
    res = client.put("/item/4", json={"id": "4", "name": "New Name"})
    assert res.status_code == 200
    assert res.get_json()["item"]["name"] == "New Name"


def test_delete_item(client):
    client.post("/item", json={"id": "5", "name": "Delete Me"})
    res = client.delete("/item/5")
    assert res.status_code == 200
    get_res = client.get("/item/5")
    assert get_res.status_code == 404


def test_get_all_items(client):
    client.post("/item", json={"id": "6", "name": "Item A"})
    client.post("/item", json={"id": "7", "name": "Item B"})
    res = client.get("/items")
    data = res.get_json()
    assert "6" in data
    assert "7" in data
