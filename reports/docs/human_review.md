# Relatório de Revisão Humana

## Escopo revisado

Revisão dos testes de autenticação, usuários, produtos e carrinhos, das fixtures compartilhadas e do cliente HTTP.

## Observações

1. **Assertions:** O teste `test_create_product_negative_price` verifica a rejeição do preço negativo e aceita variações de mensagem de validação. As mensagens da API podem depender da implementação/idioma do serviço.
2. **Preparação e limpeza:** As fixtures usam `yield` e enviam requisições `DELETE` para tentar remover usuários e produtos criados. O teste de carrinho também possui fixture de limpeza para cenários que a utilizam. Essas requisições de teardown não verificam todas o status da resposta; portanto, a limpeza é tentada, mas não é garantido que os dados tenham sido removidos com sucesso.
3. **Execução:** Em 22/10/2026, a suíte completa foi executada com `python -m pytest -q`: **17 testes passaram**. Uma execução anterior também registrou `ReadTimeout` ao acessar `compassuol.serverest.dev`. Como os testes usam uma API remota e o cliente tem timeout de 10 segundos, resultados podem variar conforme disponibilidade e latência da rede/API.

## Pontos a considerar

- Executar novamente a suíte antes de usar o resultado como evidência atual de qualidade.
- Considerar verificar as respostas das requisições de teardown para detectar falhas de limpeza.
- Considerar aumentar ou tornar configurável o timeout HTTP caso a instância apresente lentidão recorrente.
