# Regras de Negócio

| ID | Regra |
| --- | --- |
| RN-01 | Cada ocorrência possui um `id_ocorrencia` interno e um `protocolo` público único. |
| RN-02 | A descrição precisa conter entre 10 e 2000 caracteres. |
| RN-03 | `latitude` deve estar entre -90 e 90 e `longitude` entre -180 e 180. |
| RN-04 | `prioridade` e `prioridade_sugerida` usam somente `BAIXA`, `MEDIA`, `ALTA` ou `CRITICA`. |
| RN-05 | A categoria confirmada da ocorrência pode ficar vazia antes da triagem, mas toda categoria preenchida deve existir em `categoria`. |
| RN-06 | O status atual é obrigatório e deve existir em `status_ocorrencia`. |
| RN-07 | Uma ocorrência pode possuir várias fotografias; excluir a ocorrência exclui seus vínculos de foto. |
| RN-08 | Uma ocorrência pode possuir várias análises de IA; análises anteriores não são sobrescritas. |
| RN-09 | A categoria e a prioridade sugeridas pela IA não alteram automaticamente os campos confirmados da ocorrência. |
| RN-10 | Uma análise pode referenciar outra ocorrência como possível duplicada, mas não pode apontar para a própria ocorrência. |
| RN-11 | Uma ocorrência pode receber vários atendimentos e uma equipe pode executar vários atendimentos. |
| RN-12 | Quando `fim_em` existir, ele não pode ser anterior a `inicio_em`. |
| RN-13 | Cada alteração de status gera um registro em `historico_status` com status, responsável e data. |
| RN-14 | Registros históricos e análises relevantes devem ser preservados para auditoria. |
| RN-15 | Dados pessoais reais não devem ser usados na massa acadêmica. |
| RN-16 | Códigos internos não usam acentos; nomes de apresentação podem usá-los. |
| RN-17 | A resposta do teste de IA deve ser conferível diretamente no CSV. |
| RN-18 | A validação e a decisão de encaminhamento permanecem humanas. |

## Observação sobre implementação

Parte das regras é garantida diretamente por `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL` e `CHECK`. Regras de processo, como a validação humana, dependem também da API e da interface e não podem ser garantidas somente pelo banco.
