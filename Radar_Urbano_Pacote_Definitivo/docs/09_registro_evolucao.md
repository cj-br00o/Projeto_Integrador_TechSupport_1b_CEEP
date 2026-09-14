# Registro de Evolução

| Antes | Descoberta | Decisão | Evidência |
| --- | --- | --- | --- |
| Nomes diferentes entre documentos e SQL. | A integração ficava ambígua. | Criar `modelo_canonico.json` e gerar os artefatos a partir dele. | Modelo canônico, validador e relatório. |
| Categoria e status tratados como texto livre. | Eram domínios controlados. | Usar tabelas próprias, códigos únicos e FKs. | categoria, status_ocorrencia e DDL. |
| Prioridade com e sem acento. | A comparação textual podia falhar. | Usar códigos `BAIXA`, `MEDIA`, `ALTA`, `CRITICA` em banco e CSV. | CHECK, CSV e matriz Banco × CSV. |
| Fotografia como campo isolado. | Uma ocorrência pode ter mais de uma foto. | Criar `foto_ocorrencia` com relação 1:N. | DER, DDL e dicionário. |
| Resultados de IA dentro da ocorrência. | Uma nova execução apagaria o histórico. | Criar `analise_ia` com relação 1:N. | DER, DDL e relatório. |
| CSV duplicado em duas pastas. | O guia pede evitar duplicações desnecessárias. | Manter apenas `data/radar_urbano_ocorrencias_teste.csv`. | Inventário final do pacote. |
| Teste genérico. | A resposta não era facilmente conferível. | Exigir total, IDs, categoria, prioridade e status. | Prompt e gabarito verificável. |
| Resposta simulada tratada como execução. | Simulação não é evidência real do Ollama. | Separar gabarito simulado de execução real. | ia/teste_ollama.md e checklist. |
