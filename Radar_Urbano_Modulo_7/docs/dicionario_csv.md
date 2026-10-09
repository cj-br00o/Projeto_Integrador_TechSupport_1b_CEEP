# Dicionário analítico do CSV

| Coluna | Tipo na análise | Origem no banco | Significado |
| --- | --- | --- | --- |
| `id_ocorrencia` | inteiro | `ocorrencia.id_ocorrencia` | Identificador único da ocorrência. |
| `protocolo` | texto | `ocorrencia.protocolo` | Código público único de acompanhamento. |
| `descricao` | texto | `ocorrencia.descricao` | Relato enviado pelo cidadão. |
| `latitude` | decimal | `ocorrencia.latitude` | Coordenada entre -90 e 90. |
| `longitude` | decimal | `ocorrencia.longitude` | Coordenada entre -180 e 180. |
| `prioridade` | categoria | `ocorrencia.prioridade` | Prioridade confirmada: `BAIXA`, `MEDIA`, `ALTA` ou `CRITICA`. |
| `criado_em` | data/hora | `ocorrencia.criado_em` | Momento do registro da ocorrência. |
| `categoria_codigo` | categoria | `categoria.codigo` | Código da categoria confirmada. |
| `status_codigo` | categoria ordinal | `status_ocorrencia.codigo` | Etapa atual do fluxo. |
| `foto_url` | texto opcional | `foto_ocorrencia.url_arquivo` | Referência textual da primeira fotografia. |
| `resumo` | texto | `analise_ia.resumo` | Síntese registrada pela análise simulada. |
| `valido` | booleano | `analise_ia.valido` | Indica se o relato contém informação suficiente para análise. |
| `id_categoria_sugerida` | inteiro | `analise_ia.id_categoria_sugerida` | Categoria sugerida pela IA. |
| `prioridade_sugerida` | categoria | `analise_ia.prioridade_sugerida` | Prioridade sugerida pela IA. |
| `id_ocorrencia_duplicada` | inteiro opcional | `analise_ia.id_ocorrencia_duplicada` | Ocorrência indicada como possível duplicada. |
| `analisado_em` | data/hora | `analise_ia.analisado_em` | Momento em que a análise foi registrada. |

## Colunas produzidas pelo script

| Coluna | Regra | Finalidade |
| --- | --- | --- |
| `tempo_analise_min` | diferença em minutos entre `analisado_em` e `criado_em` | Medir o intervalo registrado na massa. |
| `grupo_atencao` | `URGENTE` para prioridade `ALTA` ou `CRITICA`; `ROTINA` nos demais casos | Criar uma classificação simples e verificável. |
| `possivel_duplicata` | verdadeiro quando `id_ocorrencia_duplicada` está preenchido | Separar relatos que precisam de conferência de duplicidade. |


## Validação e unidade

Uma linha corresponde a uma ocorrência distinta. Latitude e longitude são graus. Datas informam um fuso explícito. Intervalos de análise são minutos. Ausências opcionais são preservadas e contabilizadas; campos obrigatórios não podem estar vazios. Consulte contrato_dashboard.md para premissas, nulabilidade e efeitos sobre cada indicador.
