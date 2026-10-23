# Automação de Testes de API - ServeRest

Projeto de testes automatizados para a API ServeRest, usando Python, Pytest e Requests. Os testes chamam a API configurada pela URL base e criam dados de teste durante a execução.

## Tecnologias

- **Python 3.11 ou superior**
- **Pytest** para execução e organização dos testes
- **Requests** para chamadas HTTP
- **Faker** para gerar nomes de usuários
- **UUID** para reduzir colisões nos e-mails e nomes de produtos usados nos testes
- **pytest-html** para gerar relatórios HTML

## Estrutura

```text
.
├── pytest.ini
├── requirements.txt
├── reports/
│   └── docs/
│       ├── genai_usage_log.md
│       ├── human_review.md
│       └── traceability_matrix.md
└── tests/
    ├── clients/
    │   └── api_client.py
    ├── utils/
    │   └── config.py
    ├── conftest.py
    ├── test_auth.py
    ├── test_cart.py
    ├── test_products.py
    └── test_users.py
```

- `tests/clients/api_client.py`: cliente HTTP compartilhado; as chamadas têm timeout de 10 segundos.
- `tests/conftest.py`: fixtures de cliente, geração de dados e preparação/limpeza de usuários e produtos.
- `tests/utils/config.py`: URL base da API.
- `pytest.ini`: marcadores de classificação dos testes.
- `reports/docs/`: documentação de revisão, uso de GenAI e rastreabilidade dos casos.

## Cenários cobertos

A suíte contém 22 testes organizados por recurso:

- **Autenticação** (`test_auth.py`): login válido, senha inválida ou ausente e e-mail inexistente.
- **Usuários** (`test_users.py`): criação, validação de campo obrigatório, consulta existente e inexistente, e-mail duplicado e exclusão idempotente.
- **Produtos** (`test_products.py`): criação e atualização por administrador, consulta por ID, tentativas por usuário comum ou sem token e preço negativo.
- **Carrinhos** (`test_cart.py`): criação, carrinho duplicado, limites de estoque (insuficiente e exato), cancelamento com reposição de estoque e conclusão da compra.

Os testes usam os marcadores `smoke`, `positive`, `negative` e `edge`, definidos em `pytest.ini`.

## Instalação

No Windows, a partir da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configuração da API

Por padrão, os testes usam `https://compassuol.serverest.dev`. Para apontar para outra instância, defina a variável `SERVEREST_BASE_URL` antes de executar os testes.

No PowerShell:

```powershell
$env:SERVEREST_BASE_URL = "https://sua-instancia"
```

## Executar os testes

Executar toda a suíte com detalhes:

```powershell
python -m pytest -v
```

Executar um arquivo específico:

```powershell
python -m pytest tests/test_users.py -v
```

Executar por marcador:

```powershell
python -m pytest -m smoke -v
python -m pytest -m negative -v
```

Gerar um relatório HTML:

```powershell
python -m pytest -v --html=reports/report.html --self-contained-html
```

## Observações

- Os testes dependem da disponibilidade da instância ServeRest e de acesso à rede. Lentidão ou indisponibilidade da API pode causar falhas de conexão ou `ReadTimeout`.
- O cliente HTTP usa timeout de 10 segundos. O erro `ReadTimeout` significa que a API não respondeu dentro desse período; não indica, por si só, que uma asserção do teste falhou.
- Os testes criam dados na API. Fixtures removem usuários e produtos de teste e limpam o carrinho nos cenários que o utilizam. Como o serviço padrão é remoto e compartilhado, execute os testes com cuidado.
- A matriz de casos está em [`reports/docs/traceability_matrix.md`](reports/docs/traceability_matrix.md).
