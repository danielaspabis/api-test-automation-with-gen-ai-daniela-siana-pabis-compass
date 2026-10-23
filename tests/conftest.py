import pytest
from tests.clients.api_client import APIClient
from faker import Faker
import uuid

fake = Faker()

def _created_id(response, resource):
    assert response.status_code == 201, (
        f"Could not create {resource}: expected 201, got "
        f"{response.status_code}: {response.text}"
    )
    resource_id = response.json().get("_id")
    assert resource_id, f"Create {resource} response did not include '_id': {response.text}"
    return resource_id


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    yield client
    client.session.close()

@pytest.fixture
def generate_user_data():
    def _generate(admin="false"):
        return {
            "nome": fake.name(),
            "email": f"qa_{uuid.uuid4()}@serverest.dev",
            "password": "password123",
            "administrador": admin
        }
    return _generate

@pytest.fixture
def admin_user(api_client, generate_user_data):
    user_data = generate_user_data(admin="true")
    response = api_client.post("/usuarios", payload=user_data)
    user_id = _created_id(response, "admin user")
    try:
        yield user_data
    finally:
        api_client.delete(f"/usuarios/{user_id}")

@pytest.fixture
def admin_token(api_client, admin_user):
    resp = api_client.post("/login", payload={"email": admin_user["email"], "password": admin_user["password"]})
    assert resp.status_code == 200, (
        f"Could not log in admin user: expected 200, got "
        f"{resp.status_code}: {resp.text}"
    )
    token = resp.json().get("authorization")
    assert token, f"Login response did not include 'authorization': {resp.text}"
    return token

@pytest.fixture
def common_user(api_client, generate_user_data):
    user_data = generate_user_data(admin="false")
    response = api_client.post("/usuarios", payload=user_data)
    user_id = _created_id(response, "common user")
    user_data["_id"] = user_id
    try:
        yield user_data
    finally:
        api_client.delete(f"/usuarios/{user_id}")

@pytest.fixture
def common_token(api_client, common_user):
    resp = api_client.post("/login", payload={"email": common_user["email"], "password": common_user["password"]})
    assert resp.status_code == 200, (
        f"Could not log in common user: expected 200, got "
        f"{resp.status_code}: {resp.text}"
    )
    token = resp.json().get("authorization")
    assert token, f"Login response did not include 'authorization': {resp.text}"
    return token

@pytest.fixture
def test_product(api_client, admin_token):
    payload = {
        "nome": f"Produto QA {uuid.uuid4()}",
        "preco": 150,
        "descricao": "Produto de teste automatizado",
        "quantidade": 100
    }
    headers = {"Authorization": admin_token}
    resp = api_client.post("/produtos", payload=payload, headers=headers)
    prod_id = _created_id(resp, "product")
    try:
        yield {"id": prod_id, "payload": payload}
    finally:
        api_client.delete(f"/produtos/{prod_id}", headers=headers)
