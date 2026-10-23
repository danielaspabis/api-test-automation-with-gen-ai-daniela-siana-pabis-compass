import pytest

@pytest.mark.positive
def test_create_user_success(api_client, generate_user_data):
    # TC-API-USR-001
    payload = generate_user_data(admin="true")
    response = api_client.post("/usuarios", payload=payload)
    user_id = response.json().get("_id")
    try:
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert response.json().get("message") == "Cadastro realizado com sucesso"
        assert user_id, f"Expected created user ID, got {response.text}"
    finally:
        if user_id:
            api_client.delete(f"/usuarios/{user_id}")


@pytest.mark.positive
def test_get_existing_user(api_client, common_user):
    response = api_client.get(f"/usuarios/{common_user['_id']}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    user = response.json()
    assert user.get("_id") == common_user["_id"]
    assert user.get("email") == common_user["email"]
    assert user.get("administrador") == "false"

@pytest.mark.negative
def test_create_user_duplicate_email(api_client, admin_user):
    # TC-API-USR-002
    payload = admin_user
    response = api_client.post("/usuarios", payload=payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert response.json().get("message") == "Este email já está sendo usado"

@pytest.mark.negative
@pytest.mark.edge
def test_create_user_missing_name(api_client, generate_user_data):
    # TC-API-USR-005
    payload = generate_user_data()
    payload.pop("nome")
    response = api_client.post("/usuarios", payload=payload)

    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert "nome é obrigatório" in response.json().get("nome", "")

@pytest.mark.negative
def test_get_nonexistent_user(api_client):
    # TC-API-USR-003
    response = api_client.get("/usuarios/A1B2C3D4E5F6G7H8")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    assert response.json().get("message") == "Usuário não encontrado"

@pytest.mark.positive
def test_delete_user_idempotency(api_client, generate_user_data):
    # TC-API-USR-004
    payload = generate_user_data()
    resp_create = api_client.post("/usuarios", payload=payload)
    user_id = resp_create.json().get("_id")
    
    # First delete
    resp_del1 = api_client.delete(f"/usuarios/{user_id}")
    assert resp_del1.status_code == 200, f"Expected 200, got {resp_del1.status_code}"
    assert resp_del1.json().get("message") == "Registro excluído com sucesso"
    
    # Second delete
    resp_del2 = api_client.delete(f"/usuarios/{user_id}")
    assert resp_del2.status_code == 200, f"Expected 200, got {resp_del2.status_code}"
    assert resp_del2.json().get("message") == "Nenhum registro excluído"
