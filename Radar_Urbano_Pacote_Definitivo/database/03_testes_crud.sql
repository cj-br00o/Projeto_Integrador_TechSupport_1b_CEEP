-- Teste CRUD transacional. O ROLLBACK evita manter dados de teste.
-- Pré-requisitos: executar 01_schema.sql e 02_dados_referencia.sql.

BEGIN;

-- CREATE
INSERT INTO usuario (nome, email, perfil)
VALUES ('Usuário CRUD', 'crud@radar.invalid', 'CIDADAO');

INSERT INTO ocorrencia (
    protocolo, id_usuario, id_categoria, id_status, descricao,
    latitude, longitude, prioridade
)
SELECT
    'RU-TESTE-CRUD', u.id_usuario, c.id_categoria, s.id_status,
    'Ocorrência fictícia criada exclusivamente para o teste CRUD.',
    -23.420000, -51.930000, 'MEDIA'
FROM usuario u
JOIN categoria c ON c.codigo = 'INFRAESTRUTURA'
JOIN status_ocorrencia s ON s.codigo = 'RECEBIDA'
WHERE u.email = 'crud@radar.invalid';

-- READ
SELECT o.id_ocorrencia, o.protocolo, o.descricao, o.prioridade, s.codigo AS status_codigo
FROM ocorrencia o
JOIN status_ocorrencia s ON s.id_status = o.id_status
WHERE o.protocolo = 'RU-TESTE-CRUD';

-- UPDATE e histórico
UPDATE ocorrencia
SET id_status = (SELECT id_status FROM status_ocorrencia WHERE codigo = 'EM_ANALISE')
WHERE protocolo = 'RU-TESTE-CRUD';

INSERT INTO historico_status (id_ocorrencia, id_status, id_usuario_responsavel, observacao)
SELECT o.id_ocorrencia, o.id_status, u.id_usuario, 'Atualização fictícia do teste CRUD.'
FROM ocorrencia o
JOIN usuario u ON u.email = 'crud@radar.invalid'
WHERE o.protocolo = 'RU-TESTE-CRUD';

-- DELETE; históricos vinculados são removidos por CASCADE
DELETE FROM ocorrencia WHERE protocolo = 'RU-TESTE-CRUD';
DELETE FROM usuario WHERE email = 'crud@radar.invalid';

ROLLBACK;
