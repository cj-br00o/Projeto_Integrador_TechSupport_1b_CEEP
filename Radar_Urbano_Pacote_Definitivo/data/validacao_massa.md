# Validação da Massa de Testes

## Resultado geral

| Verificação | Resultado |
| --- | --- |
| Quantidade de registros | 20 |
| Quantidade de colunas | 16 |
| IDs únicos | 20 |
| Protocolos únicos | 20 |
| Coordenadas fora da faixa | 0 |
| Dados pessoais reais | Nenhum |
| Referências de duplicidade | 1 |

## Distribuição por prioridade

| Prioridade | Quantidade |
| --- | --- |
| BAIXA | 5 |
| MEDIA | 10 |
| ALTA | 2 |
| CRITICA | 3 |

## Distribuição por status

| Status | Quantidade |
| --- | --- |
| RECEBIDA | 4 |
| EM_ANALISE | 6 |
| ENCAMINHADA | 5 |
| EM_ATENDIMENTO | 4 |
| RESOLVIDA | 1 |

## Distribuição por categoria

| Categoria | Quantidade |
| --- | --- |
| INFRAESTRUTURA | 4 |
| ILUMINACAO | 2 |
| TRANSITO | 3 |
| ARBORIZACAO | 2 |
| DRENAGEM | 3 |
| CONSERVACAO | 2 |
| LIMPEZA_URBANA | 3 |
| SANEAMENTO | 1 |

## Gabarito principal

Existem **5** ocorrências com `prioridade` igual a `ALTA` ou `CRITICA`: IDs **3, 7, 11, 14, 18**.

## Caso de possível duplicidade

O registro **20** referencia o registro **5** em `id_ocorrencia_duplicada`. Ambos são dados fictícios da categoria `DRENAGEM`, possuem coordenadas próximas e descrições relacionadas ao mesmo ponto de escoamento.
