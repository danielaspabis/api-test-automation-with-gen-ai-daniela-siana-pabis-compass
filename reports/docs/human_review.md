# Relatório de Revisão Humana

## Escopo revisado

Revisão dos testes de autenticação, usuários, produtos e carrinhos, incluindo os cinco cenários adicionados, das fixtures compartilhadas e do cliente HTTP.

## Observações

1. **Assertions:** O teste `test_create_product_negative_price` verifica a rejeição do preço negativo e aceita variações de mensagem de validação. As mensagens da API podem depender da implementação/idioma do serviço.
2. **Preparação e limpeza:** As fixtures usam `yield` e enviam requisições `DELETE` para tentar remover usuários e produtos criados. O teste de carrinho também possui fixture de limpeza para cenários que a utilizam. Essas requisições de teardown não verificam todas o status da resposta; portanto, a limpeza é tentada, mas não é garantido que os dados tenham sido removidos com sucesso.
3. **Novos cenários:** Foram adicionados testes para login com e-mail inexistente, criação de usuário sem nome, consulta de produto, atualização de produto por administrador e criação de carrinho com todo o estoque disponível. A execução confirmou as respostas e os dados persistidos esperados na instância configurada.
4. **Execução:** Em 22/10/2026, a suíte completa foi executada com `python -m pytest`: **22 testes passaram**. Durante uma execução focada houve `ReadTimeout` ao acessar `compassuol.serverest.dev`; a nova tentativa do cenário passou e a execução completa também passou. Como os testes usam uma API remota e o cliente tem timeout de 10 segundos, resultados podem variar conforme disponibilidade e latência da rede/API.

## Status da revisão humana

Este registro documenta a inspeção e a validação realizadas após a ampliação da suíte; representando aprovação formal humana.

## Pontos a considerar

- Executar novamente a suíte antes de usar o resultado como evidência atual de qualidade.
- Considerar verificar as respostas das requisições de teardown para detectar falhas de limpeza.
- Considerar aumentar ou tornar configurável o timeout HTTP caso a instância apresente lentidão recorrente.
