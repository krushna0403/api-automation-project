import requests

class APIClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout

    def get(self, endpoint):
        return requests.get(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout
        )

    def post(self, endpoint, json=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            json=json,
            timeout=self.timeout
        )

    def delete(self, endpoint):
        return requests.delete(
            f"{self.base_url}{endpoint}",
            timeout=self.timeout
        )
