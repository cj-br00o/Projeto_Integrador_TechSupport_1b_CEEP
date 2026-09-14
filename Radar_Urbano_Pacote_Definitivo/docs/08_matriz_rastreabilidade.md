# Matriz de Rastreabilidade

| Entrega prometida | Tabelas | Campos | Critério de evidência |
| --- | --- | --- | --- |
| Registrar ocorrência | ocorrencia, foto_ocorrencia | id_usuario, descricao, latitude, longitude, url_arquivo | Cadastro válido e protocolo único |
| Resumir relato | analise_ia | resumo, analisado_em | Resumo ligado à ocorrência e preservado |
| Sugerir categoria | analise_ia, categoria | id_categoria_sugerida | FK garante categoria existente |
| Sugerir prioridade | analise_ia | prioridade_sugerida | CHECK usa o mesmo domínio de ocorrência.prioridade |
| Detectar possível duplicidade | analise_ia, ocorrencia | id_ocorrencia_duplicada | FK e regra contra autorreferência |
| Validar e encaminhar | ocorrencia, atendimento | id_categoria, prioridade, id_status, id_equipe | Decisão humana e equipe vinculada |
| Acompanhar status | historico_status, status_ocorrencia | id_status, id_usuario_responsavel, alterado_em | Histórico auditável |
| Produzir filtros e mapas | ocorrencia, categoria, status_ocorrencia | latitude, longitude, prioridade, categoria, status, datas | Consultas por localização e situação |
