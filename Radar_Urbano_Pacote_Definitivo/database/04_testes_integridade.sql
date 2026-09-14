-- Testes de integridade. Cada bloco espera uma rejeição do banco.
-- Pré-requisitos: executar 01_schema.sql e 02_dados_referencia.sql.

BEGIN;

INSERT INTO usuario (nome, email, perfil)
VALUES ('Usuário Integridade', 'integridade@radar.invalid', 'CIDADAO');

DO $$
BEGIN
    BEGIN
        INSERT INTO ocorrencia (protocolo, id_usuario, id_status, descricao, latitude, longitude, prioridade)
        SELECT 'RU-TESTE-PRIORIDADE', id_usuario,
               (SELECT id_status FROM status_ocorrencia WHERE codigo = 'RECEBIDA'),
               'Descrição válida para testar prioridade inválida.', -23.42, -51.93, 'URGENTE'
        FROM usuario WHERE email = 'integridade@radar.invalid';
        RAISE EXCEPTION 'FALHA: prioridade inválida foi aceita';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE 'OK: prioridade inválida rejeitada';
    END;

    BEGIN
        INSERT INTO ocorrencia (protocolo, id_usuario, id_status, descricao, latitude, longitude, prioridade)
        SELECT 'RU-TESTE-LATITUDE', id_usuario,
               (SELECT id_status FROM status_ocorrencia WHERE codigo = 'RECEBIDA'),
               'Descrição válida para testar latitude inválida.', -123.00, -51.93, 'MEDIA'
        FROM usuario WHERE email = 'integridade@radar.invalid';
        RAISE EXCEPTION 'FALHA: latitude inválida foi aceita';
    EXCEPTION WHEN check_violation THEN
        RAISE NOTICE 'OK: latitude inválida rejeitada';
    END;
END $$;

ROLLBACK;
