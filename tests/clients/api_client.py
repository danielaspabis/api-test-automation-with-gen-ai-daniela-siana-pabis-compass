import requests
from tests.utils.config import BASE_URL

REQUEST_TIMEOUT = 10


class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()

    def post(self, endpoint, payload=None, headers=None):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    def get(self, endpoint, headers=None):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    def delete(self, endpoint, headers=None):
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    def put(self, endpoint, payload=None, headers=None):
        return self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
