# tests/test_orders.py
import pytest
from utils.logger import get_logger

logger = get_logger()


# ---------------- POSITIVE TESTS ----------------

def test_create_order_success(api_client, create_test_user):
    # First create a user using fixture
    user_payload = {
        "name": "OrderUser",
        "email": "orderuser@example.com",
        "role": "user"
    }
    user_response = create_test_user(user_payload)
    user_id = user_response.json()["id"]

    order_payload = {
        "user_id": user_id,
        "product": "Laptop",
        "quantity": 2
    }

    response = api_client.post("/orders", order_payload)
    body = response.json()

    logger.info(f"Created order: {body}")

    assert response.status_code == 201
    assert body["user_id"] == user_id
    assert body["product"] == order_payload["product"]
    assert "order_id" in body


def test_get_order_success(api_client, create_test_user):
    # Create user and order
    user_payload = {
        "name": "FetchOrderUser",
        "email": "fetchorder@example.com",
        "role": "user"
    }
    user_id = create_test_user(user_payload).json()["id"]

    order_payload = {
        "user_id": user_id,
        "product": "Tablet",
        "quantity": 1
    }
    order_id = api_client.post("/orders", order_payload).json()["order_id"]

    response = api_client.get(f"/orders/{order_id}")
    body = response.json()

    logger.info(f"Fetched order: {body}")

    assert response.status_code == 200
    assert body["order_id"] == order_id
    assert body["product"] == order_payload["product"]


# ---------------- NEGATIVE TESTS ----------------

def test_create_order_user_not_found(api_client):
    order_payload = {
        "user_id": 9999,  # non-existent
        "product": "Tablet",
        "quantity": 1
    }

    response = api_client.post("/orders", order_payload)
    logger.info(f"Create order with invalid user: {response.json()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"


def test_create_order_invalid_quantity(api_client, create_test_user):
    user_payload = {
        "name": "BadQtyUser",
        "email": "badqty@example.com",
        "role": "user"
    }
    user_id = create_test_user(user_payload).json()["id"]

    order_payload = {
        "user_id": user_id,
        "product": "Phone",
        "quantity": -3  # invalid
    }

    response = api_client.post("/orders", order_payload)
    logger.info(f"Create order with invalid quantity: {response.json()}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Quantity must be greater than zero"


def test_get_order_not_found(api_client):
    response = api_client.get("/orders/9999")
    logger.info(f"Fetch non-existent order: {response.json()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Order not found"
