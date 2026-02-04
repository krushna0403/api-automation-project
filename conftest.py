import pytest
from client.api_client import APIClient
from utils.logger import get_logger

logger = get_logger()

BASE_URL = "http://127.0.0.1:8000"

# ---------------- API CLIENT FIXTURE ----------------
@pytest.fixture(scope="session")
def api_client():
    """Return a reusable API client."""
    return APIClient(BASE_URL)


# ---------------- USER FIXTURE ----------------
@pytest.fixture
def create_test_user(api_client):
    """Create a new user for tests and delete after test."""
    users_to_cleanup = []

    def _create_user(payload):
        response = api_client.post("/users", payload)
        if response.status_code == 201:
            user_id = response.json()["id"]
            users_to_cleanup.append(user_id)
            logger.info(f"Created test user: {payload['email']} with id {user_id}")
        return response

    yield _create_user

    # Cleanup
    for user_id in users_to_cleanup:
        api_client.delete(f"/users/{user_id}")
        logger.info(f"Deleted test user with id {user_id}")


# ---------------- ORDER FIXTURE ----------------
@pytest.fixture
def create_test_order(api_client, create_test_user):
    """Create a new order for a user and delete after test."""
    orders_to_cleanup = []

    def _create_order(user_payload, order_payload):
        # Ensure user exists
        user_response = create_test_user(user_payload)
        if user_response.status_code != 201:
            return user_response  # Return the failed user creation
        user_id = user_response.json()["id"]

        # Add user_id to order
        order_payload["user_id"] = user_id
        order_response = api_client.post("/orders", order_payload)
        if order_response.status_code == 201:
            order_id = order_response.json()["order_id"]
            orders_to_cleanup.append(order_id)
            logger.info(f"Created test order: {order_payload['product']} with id {order_id}")
        return order_response

    yield _create_order

    # Cleanup
    for order_id in orders_to_cleanup:
        api_client.delete(f"/orders/{order_id}")
        logger.info(f"Deleted test order with id {order_id}")
