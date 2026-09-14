# Dicionário do CSV

| Coluna | Origem | Tipo | Obrigatória | Finalidade |
| --- | --- | --- | --- | --- |
| id_ocorrencia | ocorrencia.id_ocorrencia | inteiro | Sim | Identificação verificável do registro. |
| protocolo | ocorrencia.protocolo | texto | Sim | Código público de acompanhamento. |
| descricao | ocorrencia.descricao | texto | Sim | Entrada textual para análise. |
| latitude | ocorrencia.latitude | decimal | Sim | Localização da ocorrência. |
| longitude | ocorrencia.longitude | decimal | Sim | Localização da ocorrência. |
| prioridade | ocorrencia.prioridade | texto categórico | Sim | Prioridade atual confirmada. |
| criado_em | ocorrencia.criado_em | data e hora ISO 8601 | Sim | Ordem temporal e auditoria. |
| categoria_codigo | categoria.codigo | texto categórico | Sim | Categoria atual em formato legível por máquina. |
| status_codigo | status_ocorrencia.codigo | texto categórico | Sim | Status atual em formato legível por máquina. |
| foto_url | foto_ocorrencia.url_arquivo | texto | Não | Referência da primeira foto; o teste textual não abre o arquivo. |
| resumo | analise_ia.resumo | texto | Sim | Resultado textual da análise simulada. |
| valido | analise_ia.valido | booleano | Sim | Resultado de validação da entrada. |
| id_categoria_sugerida | analise_ia.id_categoria_sugerida | inteiro | Sim | Categoria sugerida pela IA. |
| prioridade_sugerida | analise_ia.prioridade_sugerida | texto categórico | Sim | Prioridade sugerida pela IA. |
| id_ocorrencia_duplicada | analise_ia.id_ocorrencia_duplicada | inteiro | Não | Possível duplicidade indicada pela IA. |
| analisado_em | analise_ia.analisado_em | data e hora ISO 8601 | Sim | Data da análise registrada. |

## Observações

O arquivo contém uma linha por ocorrência. Para impedir duplicação de linhas, a view seleciona uma fotografia e a análise mais recente. O histórico completo continua preservado nas tabelas normalizadas. `foto_url` é somente uma referência textual nesta massa; não existe afirmação de que os arquivos apontados estejam disponíveis.
