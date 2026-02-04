# tests/test_users.py
import pytest
from utils.logger import get_logger

logger = get_logger()


# ---------------- POSITIVE TESTS ----------------

def test_create_user_success(create_test_user):
    payload = {
        "name": "Alice",
        "email": "alice@example.com",
        "role": "user"
    }

    response = create_test_user(payload)
    body = response.json()

    logger.info(f"Created user: {body}")

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    assert body["email"] == payload["email"]
    assert "id" in body
    assert body["role"] == payload["role"]


def test_get_user_success(api_client, create_test_user):
    payload = {
        "name": "FetchUser",
        "email": "fetch@example.com",
        "role": "user"
    }

    create_response = create_test_user(payload)
    user_id = create_response.json()["id"]

    response = api_client.get(f"/users/{user_id}")
    body = response.json()

    logger.info(f"Fetched user: {body}")

    assert response.status_code == 200
    assert body["id"] == user_id
    assert body["email"] == payload["email"]


# ---------------- NEGATIVE TESTS ----------------

def test_create_user_duplicate_email(create_test_user):
    payload = {
        "name": "Bob",
        "email": "duplicate@example.com",
        "role": "user"
    }

    create_test_user(payload)  # First creation succeeds
    response = create_test_user(payload)  # Second should fail

    logger.info(f"Attempted duplicate creation: {response.json()}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_get_user_not_found(api_client):
    response = api_client.get("/users/9999")
    logger.info(f"Get non-existent user: {response.json()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_create_user_invalid_email(create_test_user):
    payload = {
        "name": "Invalid",
        "email": "not-an-email",
        "role": "user"
    }

    response = create_test_user(payload)
    logger.info(f"Invalid email creation response: {response.json()}")

    assert response.status_code == 422


def test_create_user_missing_field(create_test_user):
    payload = {
        "name": "NoRole",
        "email": "norole@example.com"  # Missing 'role'
    }

    response = create_test_user(payload)
    logger.info(f"Missing field response: {response.json()}")

    assert response.status_code == 422


# ---------------- DELETE TESTS ----------------

def test_delete_user_success(api_client, create_test_user):
    payload = {
        "name": "DeleteMe",
        "email": "delete@example.com",
        "role": "user"
    }

    create_response = create_test_user(payload)
    user_id = create_response.json()["id"]

    delete_response = api_client.delete(f"/users/{user_id}")
    logger.info(f"Deleted user: {delete_response.json()}")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully"


def test_delete_user_not_found(api_client):
    response = api_client.delete("/users/9999")
    logger.info(f"Delete non-existent user: {response.json()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
