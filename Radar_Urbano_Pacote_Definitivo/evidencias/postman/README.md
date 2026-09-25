# Evidências dos testes HTTP

A coleção `postman/Radar_Urbano_Modulo_6.postman_collection.json` contém os GETs e POSTs do módulo. Execute-a com a API conectada ao banco acadêmico da equipe.

Sequência de comprovação:

1. `GET` inicial e status 200.
2. `POST` com o JSON da coleção e status 201.
3. Novo `GET` mostrando o ID criado.
4. Conferência do mesmo registro no Supabase.

Os testes automatizados em `tests/` verificam o comportamento HTTP sem inserir dados no Supabase. O arquivo `resultado_pytest.txt` registra essa revisão local.

