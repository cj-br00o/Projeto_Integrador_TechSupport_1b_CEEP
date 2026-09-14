# DER do Radar Urbano

O diagrama abaixo é editável e renderizado pelo GitHub. Os nomes de entidades e atributos são os mesmos do DDL e do dicionário.

```mermaid
erDiagram
    USUARIO {
        BIGINT id_usuario PK
        VARCHAR_120 nome
        VARCHAR_160 email UQ
        VARCHAR_20 perfil CK
        BOOLEAN ativo
        TIMESTAMPTZ criado_em
    }
    CATEGORIA {
        SMALLINT id_categoria PK
        VARCHAR_40 codigo UQ
        VARCHAR_80 nome UQ
        VARCHAR_255 descricao
        BOOLEAN ativo
    }
    STATUS_OCORRENCIA {
        SMALLINT id_status PK
        VARCHAR_30 codigo UQ
        VARCHAR_50 nome UQ
        SMALLINT ordem UQ
        BOOLEAN status_final
    }
    EQUIPE {
        BIGINT id_equipe PK
        VARCHAR_100 nome UQ
        VARCHAR_100 especialidade
        BOOLEAN ativa
        TIMESTAMPTZ criado_em
    }
    OCORRENCIA {
        BIGINT id_ocorrencia PK
        VARCHAR_20 protocolo UQ
        BIGINT id_usuario FK
        SMALLINT id_categoria FK
        SMALLINT id_status FK
        TEXT descricao CK
        NUMERIC_9_6 latitude CK
        NUMERIC_9_6 longitude CK
        VARCHAR_10 prioridade CK
        TIMESTAMPTZ criado_em
        TIMESTAMPTZ atualizado_em
    }
    FOTO_OCORRENCIA {
        BIGINT id_foto PK
        BIGINT id_ocorrencia FK
        TEXT url_arquivo
        TIMESTAMPTZ criado_em
    }
    ANALISE_IA {
        BIGINT id_analise PK
        BIGINT id_ocorrencia FK
        TEXT resumo
        BOOLEAN valido
        SMALLINT id_categoria_sugerida FK
        VARCHAR_10 prioridade_sugerida CK
        BIGINT id_ocorrencia_duplicada FK
        TIMESTAMPTZ analisado_em
    }
    ATENDIMENTO {
        BIGINT id_atendimento PK
        BIGINT id_ocorrencia FK
        BIGINT id_equipe FK
        TIMESTAMPTZ inicio_em
        TIMESTAMPTZ fim_em CK
        TEXT observacao
    }
    HISTORICO_STATUS {
        BIGINT id_historico PK
        BIGINT id_ocorrencia FK
        SMALLINT id_status FK
        BIGINT id_usuario_responsavel FK
        TEXT observacao
        TIMESTAMPTZ alterado_em
    }
    USUARIO ||--o{ OCORRENCIA : relaciona
    CATEGORIA ||--o{ OCORRENCIA : relaciona
    STATUS_OCORRENCIA ||--o{ OCORRENCIA : relaciona
    OCORRENCIA ||--o{ FOTO_OCORRENCIA : relaciona
    OCORRENCIA ||--o{ ANALISE_IA : relaciona
    CATEGORIA ||--o{ ANALISE_IA : relaciona
    OCORRENCIA ||--o{ ANALISE_IA : relaciona
    OCORRENCIA ||--o{ ATENDIMENTO : relaciona
    EQUIPE ||--o{ ATENDIMENTO : relaciona
    OCORRENCIA ||--o{ HISTORICO_STATUS : relaciona
    STATUS_OCORRENCIA ||--o{ HISTORICO_STATUS : relaciona
    USUARIO ||--o{ HISTORICO_STATUS : relaciona
```

## Relacionamentos

| Origem | Destino | Cardinalidade | Exclusão | Significado |
| --- | --- | --- | --- | --- |
| usuario.id_usuario | ocorrencia.id_usuario | 1:N | RESTRICT | Um usuário pode registrar várias ocorrências. |
| categoria.id_categoria | ocorrencia.id_categoria | 1:N | RESTRICT | Uma categoria pode classificar várias ocorrências. |
| status_ocorrencia.id_status | ocorrencia.id_status | 1:N | RESTRICT | Um status pode ser o estado atual de várias ocorrências. |
| ocorrencia.id_ocorrencia | foto_ocorrencia.id_ocorrencia | 1:N | CASCADE | Uma ocorrência pode possuir várias fotografias. |
| ocorrencia.id_ocorrencia | analise_ia.id_ocorrencia | 1:N | CASCADE | Uma ocorrência pode ser analisada mais de uma vez. |
| categoria.id_categoria | analise_ia.id_categoria_sugerida | 1:N | RESTRICT | Uma categoria pode ser sugerida em várias análises. |
| ocorrencia.id_ocorrencia | analise_ia.id_ocorrencia_duplicada | 1:N | RESTRICT | Uma ocorrência existente pode ser indicada como semelhante por várias análises. |
| ocorrencia.id_ocorrencia | atendimento.id_ocorrencia | 1:N | CASCADE | Uma ocorrência pode receber vários atendimentos. |
| equipe.id_equipe | atendimento.id_equipe | 1:N | RESTRICT | Uma equipe pode executar vários atendimentos. |
| ocorrencia.id_ocorrencia | historico_status.id_ocorrencia | 1:N | CASCADE | Uma ocorrência possui vários eventos de status. |
| status_ocorrencia.id_status | historico_status.id_status | 1:N | RESTRICT | Um status pode aparecer em vários eventos históricos. |
| usuario.id_usuario | historico_status.id_usuario_responsavel | 1:N | RESTRICT | Um usuário pode registrar várias alterações de status. |
