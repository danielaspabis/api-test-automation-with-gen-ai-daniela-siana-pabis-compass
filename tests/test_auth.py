import pytest
import uuid

@pytest.mark.smoke
@pytest.mark.positive
def test_login_success(api_client, admin_user):
    # TC-API-AUTH-001
    payload = {"email": admin_user["email"], "password": admin_user["password"]}
    response = api_client.post("/login", payload=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json().get("message") == "Login realizado com sucesso"
    assert "Bearer" in response.json().get("authorization", "")

@pytest.mark.negative
def test_login_invalid_password(api_client, admin_user):
    # TC-API-AUTH-002
    payload = {"email": admin_user["email"], "password": "wrongpassword"}
    response = api_client.post("/login", payload=payload)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json().get("message") == "Email e/ou senha inválidos"

@pytest.mark.negative
@pytest.mark.edge
def test_login_missing_password(api_client, admin_user):
    # TC-API-AUTH-003
    payload = {"email": admin_user["email"]}
    response = api_client.post("/login", payload=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "password é obrigatório" in response.json().get("password", "") or "password is required" in response.text

@pytest.mark.negative
def test_login_nonexistent_email(api_client):
    # TC-API-AUTH-004
    payload = {
        "email": f"missing_{uuid.uuid4()}@serverest.dev",
        "password": "password123",
    }
    response = api_client.post("/login", payload=payload)

    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    assert response.json().get("message") == "Email e/ou senha inválidos"
