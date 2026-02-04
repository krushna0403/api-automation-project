import yaml
from client.api_client import APIClient

def test_api_health():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    client = APIClient(config["base_url"])
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "API is running"

