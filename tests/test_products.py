import pytest
import uuid

@pytest.mark.positive
def test_create_product_admin(api_client, admin_token):
    # TC-API-PROD-001
    payload = {
        "nome": f"Prod QA {uuid.uuid4()}",
        "preco": 250,
        "descricao": "Teste Prod",
        "quantidade": 50
    }
    headers = {"Authorization": admin_token}
    resp = api_client.post("/produtos", payload=payload, headers=headers)
    product_id = resp.json().get("_id")
    try:
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
        assert resp.json().get("message") == "Cadastro realizado com sucesso"
        assert product_id, f"Expected created product ID, got {resp.text}"
    finally:
        if product_id:
            api_client.delete(f"/produtos/{product_id}", headers=headers)

@pytest.mark.negative
def test_create_product_common_user(api_client, common_token):
    # TC-API-PROD-002
    payload = {
        "nome": f"Prod QA {uuid.uuid4()}",
        "preco": 100,
        "descricao": "Teste Prod",
        "quantidade": 10
    }
    headers = {"Authorization": common_token}
    resp = api_client.post("/produtos", payload=payload, headers=headers)
    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}"
    assert resp.json().get("message") == "Rota exclusiva para administradores"

@pytest.mark.negative
def test_create_product_no_token(api_client):
    # TC-API-PROD-003
    payload = {
        "nome": f"Prod QA {uuid.uuid4()}",
        "preco": 100,
        "descricao": "Teste Prod",
        "quantidade": 10
    }
    resp = api_client.post("/produtos", payload=payload)
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"
    # Fixed failure string matching - sometimes ServeRest returns "ou usuário do token não existe mais"
    msg = resp.json().get("message", "")
    assert "Token de acesso ausente, inválido, expirado" in msg
    assert "inválido" in msg or "usuário" in msg or "não existe" in msg

@pytest.mark.negative
@pytest.mark.edge
def test_create_product_negative_price(api_client, admin_token):
    # TC-API-PROD-004
    payload = {
        "nome": f"Prod QA {uuid.uuid4()}",
        "preco": -10,
        "descricao": "Teste Prod",
        "quantidade": 10
    }
    headers = {"Authorization": admin_token}
    resp = api_client.post("/produtos", payload=payload, headers=headers)
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    assert "preco deve ser um número positivo" in resp.json().get("preco", "") or "must be a positive number" in resp.text

@pytest.mark.positive
def test_get_existing_product(api_client, test_product):
    # TC-API-PROD-005
    response = api_client.get(f"/produtos/{test_product['id']}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    product = response.json()
    assert product.get("_id") == test_product["id"]
    assert product.get("nome") == test_product["payload"]["nome"]
    assert product.get("preco") == test_product["payload"]["preco"]
    assert product.get("quantidade") == test_product["payload"]["quantidade"]

@pytest.mark.positive
def test_update_product_admin(api_client, admin_token, test_product):
    # TC-API-PROD-006
    headers = {"Authorization": admin_token}
    updated_payload = {
        **test_product["payload"],
        "nome": f"Produto atualizado {uuid.uuid4()}",
        "preco": 200,
        "descricao": "Produto atualizado por teste",
        "quantidade": 75,
    }

    response = api_client.put(
        f"/produtos/{test_product['id']}",
        payload=updated_payload,
        headers=headers,
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json().get("message") == "Registro alterado com sucesso"

    product_response = api_client.get(f"/produtos/{test_product['id']}")
    assert product_response.status_code == 200, (
        f"Expected 200, got {product_response.status_code}: {product_response.text}"
    )
    product = product_response.json()
    assert product.get("nome") == updated_payload["nome"]
    assert product.get("preco") == updated_payload["preco"]
    assert product.get("descricao") == updated_payload["descricao"]
    assert product.get("quantidade") == updated_payload["quantidade"]
