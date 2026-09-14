# Dicionário de Dados

Este dicionário deriva do mesmo modelo canônico utilizado na geração do DDL. Portanto, cada tabela e campo abaixo deve existir em `database/01_schema.sql` com o mesmo nome.

## usuario

Armazena os usuários que registram ocorrências ou atuam na validação e no atendimento.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_usuario | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno gerado pelo banco. | 1 |
| nome | VARCHAR(120) | Sim | — | — | Nome usado para identificação no sistema. | Usuário Teste 01 |
| email | VARCHAR(160) | Sim | UQ | — | E-mail único; dados reais não devem ser usados na massa acadêmica. | usuario01@example.invalid |
| perfil | VARCHAR(20) | Sim | CK | — | Código do domínio perfil. | CIDADAO |
| ativo | BOOLEAN | Sim | — | — | Indica se o acesso está habilitado. | TRUE |
| criado_em | TIMESTAMPTZ | Sim | — | — | Data e hora da criação do registro. | 2026-09-01T10:00:00-03:00 |

## categoria

Controla as categorias utilizadas na classificação das ocorrências.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_categoria | SMALLINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno da categoria. | 1 |
| codigo | VARCHAR(40) | Sim | UQ | — | Código técnico em letras maiúsculas e sem acentos. | INFRAESTRUTURA |
| nome | VARCHAR(80) | Sim | UQ | — | Nome legível apresentado na interface. | Infraestrutura |
| descricao | VARCHAR(255) | Não | — | — | Descrição curta da finalidade da categoria. | Problemas em vias e estruturas públicas |
| ativo | BOOLEAN | Sim | — | — | Permite desativar a categoria sem excluir o histórico. | TRUE |

## status_ocorrencia

Controla as etapas possíveis do ciclo de atendimento de uma ocorrência.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_status | SMALLINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno do status. | 1 |
| codigo | VARCHAR(30) | Sim | UQ | — | Código técnico em letras maiúsculas e sem acentos. | EM_ANALISE |
| nome | VARCHAR(50) | Sim | UQ | — | Nome legível apresentado na interface. | Em análise |
| ordem | SMALLINT | Sim | UQ, CK | — | Ordem positiva do fluxo padrão. | 2 |
| status_final | BOOLEAN | Sim | — | — | Indica se o status encerra o fluxo. | FALSE |

## equipe

Armazena as equipes que podem receber e executar atendimentos.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_equipe | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno da equipe. | 1 |
| nome | VARCHAR(100) | Sim | UQ | — | Nome da equipe no sistema. | Equipe de Infraestrutura |
| especialidade | VARCHAR(100) | Sim | — | — | Área principal de atuação. | Manutenção de vias |
| ativa | BOOLEAN | Sim | — | — | Indica se a equipe pode receber novos atendimentos. | TRUE |
| criado_em | TIMESTAMPTZ | Sim | — | — | Data e hora da criação do registro. | 2026-09-01T10:00:00-03:00 |

## ocorrencia

Armazena o relato principal enviado pelo cidadão e seu estado operacional atual.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_ocorrencia | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno da ocorrência. | 3 |
| protocolo | VARCHAR(20) | Sim | UQ | — | Código público de acompanhamento. | RU-2026-000003 |
| id_usuario | BIGINT | Sim | FK | usuario.id_usuario | Usuário que registrou a ocorrência. | 1 |
| id_categoria | SMALLINT | Não | FK | categoria.id_categoria | Categoria atual confirmada pela prefeitura; pode ficar vazia antes da triagem. | 3 |
| id_status | SMALLINT | Sim | FK | status_ocorrencia.id_status | Status operacional atual. | 4 |
| descricao | TEXT | Sim | CK | — | Relato entre 10 e 2000 caracteres. | Semáforo sem funcionar em cruzamento movimentado |
| latitude | NUMERIC(9,6) | Sim | CK | — | Valor entre -90 e 90. | -23.419800 |
| longitude | NUMERIC(9,6) | Sim | CK | — | Valor entre -180 e 180. | -51.932500 |
| prioridade | VARCHAR(10) | Sim | CK | — | Código do domínio prioridade. | CRITICA |
| criado_em | TIMESTAMPTZ | Sim | — | — | Data e hora do registro. | 2026-09-01T08:20:00-03:00 |
| atualizado_em | TIMESTAMPTZ | Sim | — | — | Data e hora da última alteração persistida. | 2026-09-01T09:10:00-03:00 |

## foto_ocorrencia

Armazena as referências das fotografias vinculadas a cada ocorrência.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_foto | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno da fotografia. | 1 |
| id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia | Ocorrência à qual a fotografia pertence. | 3 |
| url_arquivo | TEXT | Sim | — | — | Referência do arquivo armazenado pelo sistema. | arquivos_teste/ocorrencia_003.jpg |
| criado_em | TIMESTAMPTZ | Sim | — | — | Data e hora do vínculo da fotografia. | 2026-09-01T08:20:00-03:00 |

## analise_ia

Registra cada análise de IA sem sobrescrever resultados anteriores.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_analise | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno da análise. | 1 |
| id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia | Ocorrência analisada. | 3 |
| resumo | TEXT | Sim | — | — | Resumo estruturado produzido para apoiar a triagem. | Falha de semáforo em cruzamento com risco imediato |
| valido | BOOLEAN | Sim | — | — | Indicação técnica de que o relato possui informação suficiente para análise. | TRUE |
| id_categoria_sugerida | SMALLINT | Não | FK | categoria.id_categoria | Categoria sugerida pela IA. | 3 |
| prioridade_sugerida | VARCHAR(10) | Não | CK | — | Prioridade sugerida usando o mesmo domínio da ocorrência. | CRITICA |
| id_ocorrencia_duplicada | BIGINT | Não | FK | ocorrencia.id_ocorrencia | Referência a uma possível ocorrência duplicada. | 5 |
| analisado_em | TIMESTAMPTZ | Sim | — | — | Data e hora da análise. | 2026-09-01T08:21:00-03:00 |

## atendimento

Registra os trabalhos atribuídos às equipes para tratar uma ocorrência.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_atendimento | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno do atendimento. | 1 |
| id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia | Ocorrência atendida. | 3 |
| id_equipe | BIGINT | Sim | FK | equipe.id_equipe | Equipe responsável pelo atendimento. | 1 |
| inicio_em | TIMESTAMPTZ | Não | — | — | Data e hora do início do trabalho. | 2026-09-01T09:00:00-03:00 |
| fim_em | TIMESTAMPTZ | Não | CK | — | Quando preenchida, não pode ser anterior ao início. | 2026-09-01T11:30:00-03:00 |
| observacao | TEXT | Não | — | — | Registro operacional do atendimento. | Sinalização provisória instalada |

## historico_status

Preserva cada mudança de status para rastreabilidade e auditoria.

| Campo | Tipo SQL | Obrigatório | Chave | Referência | Regra | Exemplo |
| --- | --- | --- | --- | --- | --- | --- |
| id_historico | BIGINT GENERATED ALWAYS AS IDENTITY | Sim | PK | — | Identificador interno do evento. | 1 |
| id_ocorrencia | BIGINT | Sim | FK | ocorrencia.id_ocorrencia | Ocorrência alterada. | 3 |
| id_status | SMALLINT | Sim | FK | status_ocorrencia.id_status | Novo status registrado. | 4 |
| id_usuario_responsavel | BIGINT | Sim | FK | usuario.id_usuario | Usuário responsável pela alteração. | 2 |
| observacao | TEXT | Não | — | — | Justificativa ou informação complementar. | Ocorrência encaminhada para atendimento |
| alterado_em | TIMESTAMPTZ | Sim | — | — | Data e hora da alteração. | 2026-09-01T08:45:00-03:00 |
