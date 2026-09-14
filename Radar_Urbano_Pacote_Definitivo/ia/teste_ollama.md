# Registro do Teste no Ollama

## Arquivo utilizado

`data/radar_urbano_ocorrencias_teste.csv`

## Prompt

Analise somente o arquivo CSV fornecido. Considere os códigos exatamente como aparecem nas colunas. Conte as ocorrências em que a coluna prioridade seja ALTA ou CRITICA. Informe o total e, para cada ocorrência encontrada, apresente id_ocorrencia, categoria_codigo, prioridade e status_codigo. Depois informe quais registros possuem id_ocorrencia_duplicada preenchido e para qual ID apontam. Não use fontes externas e não invente dados.

## Resposta simulada e conferida

Foram identificadas 5 ocorrências com prioridade ALTA ou CRITICA:

- ID 3 — TRANSITO — CRITICA — EM_ATENDIMENTO
- ID 7 — ARBORIZACAO — ALTA — ENCAMINHADA
- ID 11 — DRENAGEM — CRITICA — EM_ATENDIMENTO
- ID 14 — INFRAESTRUTURA — ALTA — EM_ANALISE
- ID 18 — INFRAESTRUTURA — CRITICA — ENCAMINHADA

O registro 20 possui `id_ocorrencia_duplicada` preenchido com o valor 5.

## Execução real

Esta seção deve receber a evidência produzida no computador da equipe.

- Modelo do Ollama: [PREENCHER APÓS EXECUTAR]
- Data e hora: [PREENCHER APÓS EXECUTAR]
- Resposta completa: [COLAR A RESPOSTA]
- Conferência: [CORRETA / PARCIALMENTE CORRETA / INCORRETA]
- Evidência: [INFORMAR O NOME DO PRINT OU ARQUIVO]

A resposta acima é um gabarito simulado. Ela não deve ser apresentada como execução real do Ollama.
