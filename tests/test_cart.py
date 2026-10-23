import pytest

@pytest.fixture
def clear_cart(api_client, common_token):
    yield
    response = api_client.delete(
        "/carrinhos/cancelar-compra",
        headers={"Authorization": common_token},
    )
    assert response.status_code == 200, (
        f"Could not clear test cart: expected 200, got "
        f"{response.status_code}: {response.text}"
    )

@pytest.mark.positive
def test_create_cart_success(api_client, common_token, test_product, clear_cart):
    # TC-API-CART-001
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {"idProduto": test_product["id"], "quantidade": 2}
        ]
    }
    
    resp = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert resp.status_code == 201, f"Expected 201, got {resp.status_code}"
    assert resp.json().get("message") == "Cadastro realizado com sucesso"
    
    prod_resp = api_client.get(f"/produtos/{test_product['id']}")
    assert prod_resp.json().get("quantidade") == test_product["payload"]["quantidade"] - 2

@pytest.mark.negative
def test_create_cart_duplicate(api_client, common_token, test_product, clear_cart):
    # TC-API-CART-002
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {"idProduto": test_product["id"], "quantidade": 1}
        ]
    }
    create_response = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert create_response.status_code == 201, (
        f"Could not create initial cart: expected 201, got "
        f"{create_response.status_code}: {create_response.text}"
    )
    
    resp2 = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert resp2.status_code == 400, f"Expected 400, got {resp2.status_code}"
    assert resp2.json().get("message") == "Não é permitido ter mais de 1 carrinho"

@pytest.mark.negative
@pytest.mark.edge
def test_create_cart_insufficient_stock(api_client, common_token, test_product):
    # TC-API-CART-003
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {"idProduto": test_product["id"], "quantidade": 9999}
        ]
    }
    resp = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert resp.status_code == 400, f"Expected 400, got {resp.status_code}"
    assert resp.json().get("message") == "Produto não possui quantidade suficiente"

@pytest.mark.positive
@pytest.mark.edge
def test_create_cart_with_exact_available_stock(
    api_client, common_token, test_product, clear_cart
):
    # TC-API-CART-006
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {
                "idProduto": test_product["id"],
                "quantidade": test_product["payload"]["quantidade"],
            }
        ]
    }

    response = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert response.status_code == 201, (
        f"Expected 201, got {response.status_code}: {response.text}"
    )
    assert response.json().get("message") == "Cadastro realizado com sucesso"

    product_response = api_client.get(f"/produtos/{test_product['id']}")
    assert product_response.status_code == 200, (
        f"Expected 200, got {product_response.status_code}: {product_response.text}"
    )
    assert product_response.json().get("quantidade") == 0

@pytest.mark.positive
def test_cancel_purchase_restores_stock(api_client, common_token, test_product, clear_cart):
    # TC-API-CART-004
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {"idProduto": test_product["id"], "quantidade": 5}
        ]
    }
    create_response = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert create_response.status_code == 201, (
        f"Could not create cart: expected 201, got "
        f"{create_response.status_code}: {create_response.text}"
    )
    
    resp_cancel = api_client.delete("/carrinhos/cancelar-compra", headers=headers)
    assert resp_cancel.status_code == 200, f"Expected 200, got {resp_cancel.status_code}"
    assert "Estoque dos produtos reabastecido" in resp_cancel.json().get("message", "")
    
    prod_resp = api_client.get(f"/produtos/{test_product['id']}")
    assert prod_resp.json().get("quantidade") == test_product["payload"]["quantidade"]

@pytest.mark.positive
def test_complete_purchase(api_client, common_token, test_product, clear_cart):
    # TC-API-CART-005
    headers = {"Authorization": common_token}
    payload = {
        "produtos": [
            {"idProduto": test_product["id"], "quantidade": 1}
        ]
    }
    create_response = api_client.post("/carrinhos", payload=payload, headers=headers)
    assert create_response.status_code == 201, (
        f"Could not create cart: expected 201, got "
        f"{create_response.status_code}: {create_response.text}"
    )
    
    resp_complete = api_client.delete("/carrinhos/concluir-compra", headers=headers)
    assert resp_complete.status_code == 200, f"Expected 200, got {resp_complete.status_code}"
    assert resp_complete.json().get("message") == "Registro excluído com sucesso"

    prod_resp = api_client.get(f"/produtos/{test_product['id']}")
    assert prod_resp.json().get("quantidade") == test_product["payload"]["quantidade"] - 1
