-- Radar Urbano
-- DDL PostgreSQL gerado a partir de docs/modelo_canonico.json
-- Os nomes físicos deste arquivo são a referência dos demais artefatos.

BEGIN;

CREATE TABLE usuario (
    id_usuario BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL,
    perfil VARCHAR(20) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_usuario_email UNIQUE (email),
    CONSTRAINT ck_usuario_perfil CHECK (perfil IN ('CIDADAO', 'PREFEITURA', 'EQUIPE', 'ADMINISTRADOR'))
);

CREATE TABLE categoria (
    id_categoria SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo VARCHAR(40) NOT NULL,
    nome VARCHAR(80) NOT NULL,
    descricao VARCHAR(255),
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_categoria_codigo UNIQUE (codigo),
    CONSTRAINT uq_categoria_nome UNIQUE (nome),
    CONSTRAINT ck_categoria_codigo CHECK (codigo ~ '^[A-Z][A-Z0-9_]*$')
);

CREATE TABLE status_ocorrencia (
    id_status SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    codigo VARCHAR(30) NOT NULL,
    nome VARCHAR(50) NOT NULL,
    ordem SMALLINT NOT NULL,
    status_final BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT uq_status_codigo UNIQUE (codigo),
    CONSTRAINT uq_status_nome UNIQUE (nome),
    CONSTRAINT uq_status_ordem UNIQUE (ordem),
    CONSTRAINT ck_status_codigo CHECK (codigo ~ '^[A-Z][A-Z0-9_]*$'),
    CONSTRAINT ck_status_ordem CHECK (ordem > 0)
);

CREATE TABLE equipe (
    id_equipe BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    ativa BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_equipe_nome UNIQUE (nome)
);

CREATE TABLE ocorrencia (
    id_ocorrencia BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    protocolo VARCHAR(20) NOT NULL,
    id_usuario BIGINT NOT NULL,
    id_categoria SMALLINT,
    id_status SMALLINT NOT NULL,
    descricao TEXT NOT NULL,
    latitude NUMERIC(9,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    prioridade VARCHAR(10) NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_ocorrencia_protocolo UNIQUE (protocolo),
    CONSTRAINT fk_ocorrencia_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE RESTRICT,
    CONSTRAINT fk_ocorrencia_categoria FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria) ON DELETE RESTRICT,
    CONSTRAINT fk_ocorrencia_status FOREIGN KEY (id_status) REFERENCES status_ocorrencia(id_status) ON DELETE RESTRICT,
    CONSTRAINT ck_ocorrencia_descricao CHECK (char_length(btrim(descricao)) BETWEEN 10 AND 2000),
    CONSTRAINT ck_ocorrencia_latitude CHECK (latitude BETWEEN -90 AND 90),
    CONSTRAINT ck_ocorrencia_longitude CHECK (longitude BETWEEN -180 AND 180),
    CONSTRAINT ck_ocorrencia_prioridade CHECK (prioridade IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')),
    CONSTRAINT ck_ocorrencia_datas CHECK (atualizado_em >= criado_em)
);

CREATE TABLE foto_ocorrencia (
    id_foto BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_ocorrencia BIGINT NOT NULL,
    url_arquivo TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_foto_ocorrencia FOREIGN KEY (id_ocorrencia) REFERENCES ocorrencia(id_ocorrencia) ON DELETE CASCADE,
    CONSTRAINT ck_foto_url CHECK (char_length(btrim(url_arquivo)) > 0)
);

CREATE TABLE analise_ia (
    id_analise BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_ocorrencia BIGINT NOT NULL,
    resumo TEXT NOT NULL,
    valido BOOLEAN NOT NULL,
    id_categoria_sugerida SMALLINT,
    prioridade_sugerida VARCHAR(10),
    id_ocorrencia_duplicada BIGINT,
    analisado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_analise_ocorrencia FOREIGN KEY (id_ocorrencia) REFERENCES ocorrencia(id_ocorrencia) ON DELETE CASCADE,
    CONSTRAINT fk_analise_categoria FOREIGN KEY (id_categoria_sugerida) REFERENCES categoria(id_categoria) ON DELETE RESTRICT,
    CONSTRAINT fk_analise_duplicada FOREIGN KEY (id_ocorrencia_duplicada) REFERENCES ocorrencia(id_ocorrencia) ON DELETE RESTRICT,
    CONSTRAINT ck_analise_resumo CHECK (char_length(btrim(resumo)) > 0),
    CONSTRAINT ck_analise_prioridade CHECK (prioridade_sugerida IS NULL OR prioridade_sugerida IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')),
    CONSTRAINT ck_analise_nao_autorreferencia CHECK (id_ocorrencia_duplicada IS NULL OR id_ocorrencia_duplicada <> id_ocorrencia)
);

CREATE TABLE atendimento (
    id_atendimento BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_ocorrencia BIGINT NOT NULL,
    id_equipe BIGINT NOT NULL,
    inicio_em TIMESTAMPTZ,
    fim_em TIMESTAMPTZ,
    observacao TEXT,
    CONSTRAINT fk_atendimento_ocorrencia FOREIGN KEY (id_ocorrencia) REFERENCES ocorrencia(id_ocorrencia) ON DELETE CASCADE,
    CONSTRAINT fk_atendimento_equipe FOREIGN KEY (id_equipe) REFERENCES equipe(id_equipe) ON DELETE RESTRICT,
    CONSTRAINT ck_atendimento_datas CHECK (fim_em IS NULL OR inicio_em IS NULL OR fim_em >= inicio_em)
);

CREATE TABLE historico_status (
    id_historico BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_ocorrencia BIGINT NOT NULL,
    id_status SMALLINT NOT NULL,
    id_usuario_responsavel BIGINT NOT NULL,
    observacao TEXT,
    alterado_em TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_historico_ocorrencia FOREIGN KEY (id_ocorrencia) REFERENCES ocorrencia(id_ocorrencia) ON DELETE CASCADE,
    CONSTRAINT fk_historico_status FOREIGN KEY (id_status) REFERENCES status_ocorrencia(id_status) ON DELETE RESTRICT,
    CONSTRAINT fk_historico_usuario FOREIGN KEY (id_usuario_responsavel) REFERENCES usuario(id_usuario) ON DELETE RESTRICT
);

CREATE INDEX idx_ocorrencia_categoria ON ocorrencia(id_categoria);
CREATE INDEX idx_ocorrencia_status ON ocorrencia(id_status);
CREATE INDEX idx_ocorrencia_prioridade ON ocorrencia(prioridade);
CREATE INDEX idx_ocorrencia_criado_em ON ocorrencia(criado_em);
CREATE INDEX idx_ocorrencia_localizacao ON ocorrencia(latitude, longitude);
CREATE INDEX idx_foto_ocorrencia ON foto_ocorrencia(id_ocorrencia);
CREATE INDEX idx_analise_ocorrencia_data ON analise_ia(id_ocorrencia, analisado_em DESC);
CREATE INDEX idx_atendimento_ocorrencia ON atendimento(id_ocorrencia);
CREATE INDEX idx_atendimento_equipe ON atendimento(id_equipe);
CREATE INDEX idx_historico_ocorrencia_data ON historico_status(id_ocorrencia, alterado_em DESC);

CREATE OR REPLACE FUNCTION fn_atualizar_ocorrencia_data()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_ocorrencia_atualizado_em
BEFORE UPDATE ON ocorrencia
FOR EACH ROW EXECUTE FUNCTION fn_atualizar_ocorrencia_data();

CREATE VIEW vw_ocorrencia_exportacao_ia AS
SELECT
    o.id_ocorrencia,
    o.protocolo,
    o.descricao,
    o.latitude,
    o.longitude,
    o.prioridade,
    o.criado_em,
    c.codigo AS categoria_codigo,
    s.codigo AS status_codigo,
    f.url_arquivo AS foto_url,
    a.resumo,
    a.valido,
    a.id_categoria_sugerida,
    a.prioridade_sugerida,
    a.id_ocorrencia_duplicada,
    a.analisado_em
FROM ocorrencia o
LEFT JOIN categoria c ON c.id_categoria = o.id_categoria
JOIN status_ocorrencia s ON s.id_status = o.id_status
LEFT JOIN LATERAL (
    SELECT fo.url_arquivo
    FROM foto_ocorrencia fo
    WHERE fo.id_ocorrencia = o.id_ocorrencia
    ORDER BY fo.criado_em, fo.id_foto
    LIMIT 1
) f ON TRUE
LEFT JOIN LATERAL (
    SELECT ai.resumo, ai.valido, ai.id_categoria_sugerida,
           ai.prioridade_sugerida, ai.id_ocorrencia_duplicada, ai.analisado_em
    FROM analise_ia ai
    WHERE ai.id_ocorrencia = o.id_ocorrencia
    ORDER BY ai.analisado_em DESC, ai.id_analise DESC
    LIMIT 1
) a ON TRUE;

COMMIT;
