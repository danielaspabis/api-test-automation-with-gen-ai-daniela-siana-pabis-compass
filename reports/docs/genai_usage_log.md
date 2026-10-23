# Log de Uso da GenAI (Desenvolvimento Assistido)

| Componente | Problema/Necessidade | Sugestão GenAI | Decisão Humana | Ação Realizada |
| :--- | :--- | :--- | :--- | :--- |
| Projeto | Estruturação de fixtures de autenticação e dados de teste. | Separar tokens de admin e usuário comum; usar nomes gerados pelo Faker e UUID para reduzir colisões de dados. | Aceita e ajustada para usar escopo de teste p/ evitar conflito no ServeRest. | Criadas fixtures `admin_user`, `admin_token`, `common_user` em `conftest.py`. Faker gera nomes; o módulo padrão `uuid` gera identificadores usados nos e-mails. |
| Asserts | Validar criação de carrinho. | Sugeriu apenas checar Status 201. | Rejeitada (Muito fraco). Solicitei que a assert validasse a integridade do estoque após reserva. | Incluída chamada GET ao produto para validar decremento em `test_cart.py`. |
| Arquitetura | Wrapper de chamadas HTTP (DRY). | Criar classe `APIClient` usando `requests.Session()`. | Aceita. Centraliza host, session state e simplifica headers nas requisições do Pytest. | Criado `clients/api_client.py`. |
| Depuração | Investigar timeouts e validar os testes. | Diferenciar falhas de asserção de falhas de conexão e reproduzir a execução. | Registrar o resultado observado sem presumir disponibilidade permanente da API. | A execução de `python -m pytest -q` passou com 17 testes em 22/10/2026; também houve relato de `ReadTimeout` em execução anterior contra a API remota. |
