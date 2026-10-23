# Matriz de Rastreabilidade

Esta matriz relaciona os cenários automatizados atualmente implementados. Na execução mais recente, a suíte completa passou (22 testes), em 22/10/2026. Esse resultado descreve apenas aquela execução: os testes dependem da disponibilidade da instância ServeRest configurada e podem falhar por lentidão ou indisponibilidade da rede/API.

| ID Test Plan (Original) | Endpoint | ID Teste Automatizado | Tipo | Status Implementação | Status Execução |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-API-AUTH-001 | POST /login | `test_login_success` | Positive | Concluído | Passou na última execução |
| TC-API-AUTH-002 | POST /login | `test_login_invalid_password` | Negative | Concluído | Passou na última execução |
| TC-API-AUTH-003 | POST /login | `test_login_missing_password` | Boundary | Concluído | Passou na última execução |
| TC-API-AUTH-004 | POST /login | `test_login_nonexistent_email` | Negative | Concluído | Passou na última execução |
| TC-API-USR-001 | POST /usuarios | `test_create_user_success` | Positive | Concluído | Passou na última execução |
| TC-API-USR-002 | POST /usuarios | `test_create_user_duplicate_email` | Negative | Concluído | Passou na última execução |
| TC-API-USR-003 | GET /usuarios/{id} | `test_get_nonexistent_user` | Negative | Concluído | Passou na última execução |
| N/A (cenário adicional) | GET /usuarios/{id} | `test_get_existing_user` | Positive | Concluído | Passou na última execução |
| TC-API-USR-004 | DELETE /usuarios/{id} | `test_delete_user_idempotency` | Positive/Edge | Concluído | Passou na última execução |
| TC-API-USR-005 | POST /usuarios | `test_create_user_missing_name` | Negative/Boundary | Concluído | Passou na última execução |
| TC-API-PROD-001 | POST /produtos | `test_create_product_admin` | Positive | Concluído | Passou na última execução |
| TC-API-PROD-002 | POST /produtos | `test_create_product_common_user` | Negative | Concluído | Passou na última execução |
| TC-API-PROD-003 | POST /produtos | `test_create_product_no_token` | Negative | Concluído | Passou na última execução |
| TC-API-PROD-004 | POST /produtos | `test_create_product_negative_price` | Boundary | Concluído | Passou na última execução |
| TC-API-PROD-005 | GET /produtos/{id} | `test_get_existing_product` | Positive | Concluído | Passou na última execução |
| TC-API-PROD-006 | PUT /produtos/{id} | `test_update_product_admin` | Positive | Concluído | Passou na última execução |
| TC-API-CART-001 | POST /carrinhos | `test_create_cart_success` | Positive | Concluído | Passou na última execução |
| TC-API-CART-002 | POST /carrinhos | `test_create_cart_duplicate` | Negative | Concluído | Passou na última execução |
| TC-API-CART-003 | POST /carrinhos | `test_create_cart_insufficient_stock` | Negative | Concluído | Passou na última execução |
| TC-API-CART-006 | POST /carrinhos | `test_create_cart_with_exact_available_stock` | Positive/Boundary | Concluído | Passou na última execução |
| TC-API-CART-004 | DELETE /carrinhos/cancelar-compra | `test_cancel_purchase_restores_stock` | Positive | Concluído | Passou na última execução |
| TC-API-CART-005 | DELETE /carrinhos/concluir-compra | `test_complete_purchase` | Positive | Concluído | Passou na última execução |
