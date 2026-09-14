# Padrão de Nomenclatura

## Regra central

Os nomes físicos do banco são a referência para toda a documentação. Tabelas e campos usam `snake_case`. Códigos controlados usam letras maiúsculas sem acento. Nomes de interface podem ter acentos, mas devem ser associados a um código técnico explícito.

## Domínios oficiais

### perfil

`CIDADAO`, `PREFEITURA`, `EQUIPE`, `ADMINISTRADOR`

### prioridade e prioridade_sugerida

`BAIXA`, `MEDIA`, `ALTA`, `CRITICA`

### status_ocorrencia.codigo

`RECEBIDA`, `EM_ANALISE`, `ENCAMINHADA`, `EM_ATENDIMENTO`, `RESOLVIDA`

### categoria.codigo

`INFRAESTRUTURA`, `ILUMINACAO`, `TRANSITO`, `ARBORIZACAO`, `DRENAGEM`, `CONSERVACAO`, `LIMPEZA_URBANA`, `SANEAMENTO`

## Cadastro físico consolidado

| Tabela | Campo | Tipo SQL | Obrigatório | Chave | Referência |
| --- | --- | --- | --- | --- | --- |
| usuario | id_usuario | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| usuario | nome | VARCHAR(120) | Sim | — | — |
| usuario | email | VARCHAR(160) | Sim | UQ | — |
| usuario | perfil | VARCHAR(20) | Sim | CK | — |
| usuario | ativo | BOOLEAN | Sim | — | — |
| usuario | criado_em | TIMESTAMPTZ | Sim | — | — |
| categoria | id_categoria | SMALLINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| categoria | codigo | VARCHAR(40) | Sim | UQ | — |
| categoria | nome | VARCHAR(80) | Sim | UQ | — |
| categoria | descricao | VARCHAR(255) | Não | — | — |
| categoria | ativo | BOOLEAN | Sim | — | — |
| status_ocorrencia | id_status | SMALLINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| status_ocorrencia | codigo | VARCHAR(30) | Sim | UQ | — |
| status_ocorrencia | nome | VARCHAR(50) | Sim | UQ | — |
| status_ocorrencia | ordem | SMALLINT | Sim | UQ, CK | — |
| status_ocorrencia | status_final | BOOLEAN | Sim | — | — |
| equipe | id_equipe | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| equipe | nome | VARCHAR(100) | Sim | UQ | — |
| equipe | especialidade | VARCHAR(100) | Sim | — | — |
| equipe | ativa | BOOLEAN | Sim | — | — |
| equipe | criado_em | TIMESTAMPTZ | Sim | — | — |
| ocorrencia | id_ocorrencia | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| ocorrencia | protocolo | VARCHAR(20) | Sim | UQ | — |
| ocorrencia | id_usuario | BIGINT | Sim | FK | usuario.id_usuario |
| ocorrencia | id_categoria | SMALLINT | Não | FK | categoria.id_categoria |
| ocorrencia | id_status | SMALLINT | Sim | FK | status_ocorrencia.id_status |
| ocorrencia | descricao | TEXT | Sim | CK | — |
| ocorrencia | latitude | NUMERIC(9,6) | Sim | CK | — |
| ocorrencia | longitude | NUMERIC(9,6) | Sim | CK | — |
| ocorrencia | prioridade | VARCHAR(10) | Sim | CK | — |
| ocorrencia | criado_em | TIMESTAMPTZ | Sim | — | — |
| ocorrencia | atualizado_em | TIMESTAMPTZ | Sim | — | — |
| foto_ocorrencia | id_foto | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| foto_ocorrencia | id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia |
| foto_ocorrencia | url_arquivo | TEXT | Sim | — | — |
| foto_ocorrencia | criado_em | TIMESTAMPTZ | Sim | — | — |
| analise_ia | id_analise | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| analise_ia | id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia |
| analise_ia | resumo | TEXT | Sim | — | — |
| analise_ia | valido | BOOLEAN | Sim | — | — |
| analise_ia | id_categoria_sugerida | SMALLINT | Não | FK | categoria.id_categoria |
| analise_ia | prioridade_sugerida | VARCHAR(10) | Não | CK | — |
| analise_ia | id_ocorrencia_duplicada | BIGINT | Não | FK | ocorrencia.id_ocorrencia |
| analise_ia | analisado_em | TIMESTAMPTZ | Sim | — | — |
| atendimento | id_atendimento | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| atendimento | id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia |
| atendimento | id_equipe | BIGINT | Sim | FK | equipe.id_equipe |
| atendimento | inicio_em | TIMESTAMPTZ | Não | — | — |
| atendimento | fim_em | TIMESTAMPTZ | Não | CK | — |
| atendimento | observacao | TEXT | Não | — | — |
| historico_status | id_historico | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — |
| historico_status | id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia |
| historico_status | id_status | SMALLINT | Sim | FK | status_ocorrencia.id_status |
| historico_status | id_usuario_responsavel | BIGINT | Sim | FK | usuario.id_usuario |
| historico_status | observacao | TEXT | Não | — | — |
| historico_status | alterado_em | TIMESTAMPTZ | Sim | — | — |

## Regra para o CSV

As colunas que vêm diretamente de `ocorrencia` mantêm o mesmo nome. Os campos provenientes de tabelas relacionadas usam o nome físico acompanhado do contexto, como `categoria_codigo` e `status_codigo`. Essa diferença é documentada na matriz Banco × CSV e na view `vw_ocorrencia_exportacao_ia`.
