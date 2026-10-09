-- Radar Urbano - massa de testes do Módulo 7
-- PostgreSQL / Supabase
-- Execute somente no banco acadêmico de testes, depois de script_ddl.sql.

BEGIN;

DO $$ BEGIN
    IF EXISTS (SELECT 1 FROM usuario) OR EXISTS (SELECT 1 FROM categoria) OR EXISTS (SELECT 1 FROM status_ocorrencia) THEN
        RAISE EXCEPTION 'Seed permitido somente em banco acadêmico vazio. Use os registros existentes ou outro banco de testes.';
    END IF;
END $$;

INSERT INTO usuario
    (id_usuario, nome, email, perfil, ativo, criado_em)
OVERRIDING SYSTEM VALUE
VALUES
    (1, 'Cidadão Teste', 'cidadao01@example.invalid', 'CIDADAO', TRUE, '2026-09-01T07:30:00-03:00'),
    (2, 'Servidor Teste', 'servidor01@example.invalid', 'PREFEITURA', TRUE, '2026-09-01T07:30:00-03:00'),
    (3, 'Responsável de Equipe', 'equipe01@example.invalid', 'EQUIPE', TRUE, '2026-09-01T07:30:00-03:00'),
    (4, 'Administrador Teste', 'admin01@example.invalid', 'ADMINISTRADOR', TRUE, '2026-09-01T07:30:00-03:00');

INSERT INTO categoria
    (id_categoria, codigo, nome, descricao, ativo)
OVERRIDING SYSTEM VALUE
VALUES
    (1, 'INFRAESTRUTURA', 'Infraestrutura', 'Problemas em vias e estruturas públicas', TRUE),
    (2, 'ILUMINACAO', 'Iluminação', 'Falhas de iluminação pública', TRUE),
    (3, 'TRANSITO', 'Trânsito', 'Sinalização e circulação viária', TRUE),
    (4, 'ARBORIZACAO', 'Arborização', 'Árvores e manejo em espaços públicos', TRUE),
    (5, 'DRENAGEM', 'Drenagem', 'Escoamento e alagamentos', TRUE),
    (6, 'CONSERVACAO', 'Conservação', 'Conservação de equipamentos e espaços', TRUE),
    (7, 'LIMPEZA_URBANA', 'Limpeza urbana', 'Resíduos, entulho e vegetação', TRUE),
    (8, 'SANEAMENTO', 'Saneamento', 'Ocorrências relacionadas a água e saneamento', TRUE);

INSERT INTO status_ocorrencia
    (id_status, codigo, nome, ordem, status_final)
OVERRIDING SYSTEM VALUE
VALUES
    (1, 'RECEBIDA', 'Recebida', 1, FALSE),
    (2, 'EM_ANALISE', 'Em análise', 2, FALSE),
    (3, 'ENCAMINHADA', 'Encaminhada', 3, FALSE),
    (4, 'EM_ATENDIMENTO', 'Em atendimento', 4, FALSE),
    (5, 'RESOLVIDA', 'Resolvida', 5, TRUE);

INSERT INTO equipe
    (id_equipe, nome, especialidade, ativa, criado_em)
OVERRIDING SYSTEM VALUE
VALUES
    (1, 'Equipe de Vias', 'Infraestrutura, trânsito e drenagem', TRUE, '2026-09-01T07:30:00-03:00'),
    (2, 'Equipe de Iluminação', 'Iluminação pública', TRUE, '2026-09-01T07:30:00-03:00'),
    (3, 'Equipe Ambiental', 'Arborização, limpeza e saneamento', TRUE, '2026-09-01T07:30:00-03:00'),
    (4, 'Equipe de Conservação', 'Equipamentos e espaços públicos', TRUE, '2026-09-01T07:30:00-03:00');

INSERT INTO ocorrencia
    (id_ocorrencia, protocolo, id_usuario, id_categoria, id_status, descricao,
     latitude, longitude, prioridade, criado_em, atualizado_em)
OVERRIDING SYSTEM VALUE
VALUES
    (1, 'RU-2026-000001', 1, 1, 1, 'Buraco profundo em via pública, com risco para veículos.', -23.420100, -51.933200, 'MEDIA', '2026-09-01T08:00:00-03:00', '2026-09-01T08:01:00-03:00'),
    (2, 'RU-2026-000002', 1, 2, 2, 'Luminária apagada há três noites em trecho de circulação de pedestres.', -23.421300, -51.934100, 'BAIXA', '2026-09-01T08:05:00-03:00', '2026-09-01T08:06:00-03:00'),
    (3, 'RU-2026-000003', 1, 3, 4, 'Semáforo sem funcionar em cruzamento movimentado.', -23.419800, -51.932500, 'CRITICA', '2026-09-01T08:10:00-03:00', '2026-09-01T08:11:00-03:00'),
    (4, 'RU-2026-000004', 1, 4, 3, 'Galhos acumulados bloqueando parte da calçada.', -23.417900, -51.930700, 'MEDIA', '2026-09-01T08:15:00-03:00', '2026-09-01T08:16:00-03:00'),
    (5, 'RU-2026-000005', 1, 5, 2, 'Bueiro com escoamento lento após chuva.', -23.423100, -51.936400, 'MEDIA', '2026-09-01T08:20:00-03:00', '2026-09-01T08:21:00-03:00'),
    (6, 'RU-2026-000006', 1, 6, 1, 'Pichação em muro de equipamento público.', -23.425200, -51.938000, 'BAIXA', '2026-09-01T08:25:00-03:00', '2026-09-01T08:26:00-03:00'),
    (7, 'RU-2026-000007', 1, 4, 3, 'Árvore inclinada sobre a rede elétrica.', -23.416500, -51.929900, 'ALTA', '2026-09-01T08:30:00-03:00', '2026-09-01T08:31:00-03:00'),
    (8, 'RU-2026-000008', 1, 3, 1, 'Placa de sinalização caída ao lado da via.', -23.424000, -51.935100, 'MEDIA', '2026-09-01T08:35:00-03:00', '2026-09-01T08:36:00-03:00'),
    (9, 'RU-2026-000009', 1, 7, 4, 'Lixo descartado irregularmente em terreno aberto.', -23.426300, -51.940200, 'MEDIA', '2026-09-01T08:40:00-03:00', '2026-09-01T08:41:00-03:00'),
    (10, 'RU-2026-000010', 1, 1, 2, 'Calçada pública com peças de piso soltas.', -23.418700, -51.931600, 'BAIXA', '2026-09-01T08:45:00-03:00', '2026-09-01T08:46:00-03:00'),
    (11, 'RU-2026-000011', 1, 5, 4, 'Alagamento impedindo a passagem de veículos.', -23.427100, -51.941500, 'CRITICA', '2026-09-01T08:50:00-03:00', '2026-09-01T08:51:00-03:00'),
    (12, 'RU-2026-000012', 1, 2, 5, 'Poste com luminária oscilando durante a noite.', -23.422200, -51.937100, 'MEDIA', '2026-09-01T08:55:00-03:00', '2026-09-01T08:56:00-03:00'),
    (13, 'RU-2026-000013', 1, 3, 3, 'Faixa de pedestres com pintura quase apagada.', -23.415900, -51.928600, 'MEDIA', '2026-09-01T09:00:00-03:00', '2026-09-01T09:01:00-03:00'),
    (14, 'RU-2026-000014', 1, 1, 2, 'Fiação exposta próxima a ponto de ônibus.', -23.414700, -51.927500, 'ALTA', '2026-09-01T09:05:00-03:00', '2026-09-01T09:06:00-03:00'),
    (15, 'RU-2026-000015', 1, 6, 1, 'Banco de praça quebrado e sem condição de uso.', -23.428200, -51.942400, 'BAIXA', '2026-09-01T09:10:00-03:00', '2026-09-01T09:11:00-03:00'),
    (16, 'RU-2026-000016', 1, 7, 3, 'Entulho ocupando parte da via pública.', -23.429000, -51.943100, 'MEDIA', '2026-09-01T09:15:00-03:00', '2026-09-01T09:16:00-03:00'),
    (17, 'RU-2026-000017', 1, 8, 4, 'Vazamento contínuo de água na rua.', -23.413900, -51.926800, 'MEDIA', '2026-09-01T09:20:00-03:00', '2026-09-01T09:21:00-03:00'),
    (18, 'RU-2026-000018', 1, 1, 3, 'Cratera aumentando em via próxima a uma escola.', -23.412600, -51.925900, 'CRITICA', '2026-09-01T09:25:00-03:00', '2026-09-01T09:26:00-03:00'),
    (19, 'RU-2026-000019', 1, 7, 2, 'Mato alto reduzindo a visibilidade em uma esquina.', -23.430100, -51.944300, 'BAIXA', '2026-09-01T09:30:00-03:00', '2026-09-01T09:31:00-03:00'),
    (20, 'RU-2026-000020', 1, 5, 2, 'Novo relato de escoamento lento no mesmo bueiro registrado anteriormente.', -23.423120, -51.936410, 'MEDIA', '2026-09-01T09:35:00-03:00', '2026-09-01T09:36:00-03:00');

INSERT INTO foto_ocorrencia (id_ocorrencia, url_arquivo, criado_em)
SELECT
    id_ocorrencia,
    'arquivos_teste/ocorrencia_' || LPAD(id_ocorrencia::TEXT, 3, '0') || '.jpg',
    criado_em
FROM ocorrencia
ORDER BY id_ocorrencia;

INSERT INTO analise_ia
    (id_ocorrencia, resumo, valido, id_categoria_sugerida,
     prioridade_sugerida, id_ocorrencia_duplicada, analisado_em)
VALUES
    (1, 'Buraco profundo em via pública com risco de dano a veículos.', TRUE, 1, 'MEDIA', NULL, '2026-09-01T08:01:00-03:00'),
    (2, 'Falha de iluminação em trecho utilizado por pedestres.', TRUE, 2, 'BAIXA', NULL, '2026-09-01T08:06:00-03:00'),
    (3, 'Falha de semáforo em cruzamento com risco imediato ao trânsito.', TRUE, 3, 'CRITICA', NULL, '2026-09-01T08:11:00-03:00'),
    (4, 'Galhos obstruem parcialmente a circulação na calçada.', TRUE, 4, 'MEDIA', NULL, '2026-09-01T08:16:00-03:00'),
    (5, 'Bueiro apresenta escoamento lento após precipitação.', TRUE, 5, 'MEDIA', NULL, '2026-09-01T08:21:00-03:00'),
    (6, 'Pichação registrada em estrutura de equipamento público.', TRUE, 6, 'BAIXA', NULL, '2026-09-01T08:26:00-03:00'),
    (7, 'Árvore inclinada apresenta risco próximo à rede elétrica.', TRUE, 4, 'ALTA', NULL, '2026-09-01T08:31:00-03:00'),
    (8, 'Placa de sinalização caída reduz a orientação no trecho.', TRUE, 3, 'MEDIA', NULL, '2026-09-01T08:36:00-03:00'),
    (9, 'Descarte irregular de resíduos em terreno aberto.', TRUE, 7, 'MEDIA', NULL, '2026-09-01T08:41:00-03:00'),
    (10, 'Piso solto em calçada pública pode dificultar a circulação.', TRUE, 1, 'BAIXA', NULL, '2026-09-01T08:46:00-03:00'),
    (11, 'Alagamento bloqueia a via e exige atendimento imediato.', TRUE, 5, 'CRITICA', NULL, '2026-09-01T08:51:00-03:00'),
    (12, 'Luminária em poste apresenta funcionamento intermitente.', TRUE, 2, 'MEDIA', NULL, '2026-09-01T08:56:00-03:00'),
    (13, 'Sinalização horizontal desgastada reduz a visibilidade da travessia.', TRUE, 3, 'MEDIA', NULL, '2026-09-01T09:01:00-03:00'),
    (14, 'Fiação exposta em área de circulação representa risco elevado.', TRUE, 1, 'ALTA', NULL, '2026-09-01T09:06:00-03:00'),
    (15, 'Mobiliário da praça está danificado e indisponível para uso.', TRUE, 6, 'BAIXA', NULL, '2026-09-01T09:11:00-03:00'),
    (16, 'Entulho reduz a área livre para circulação na via.', TRUE, 7, 'MEDIA', NULL, '2026-09-01T09:16:00-03:00'),
    (17, 'Vazamento contínuo provoca perda de água na via pública.', TRUE, 8, 'MEDIA', NULL, '2026-09-01T09:21:00-03:00'),
    (18, 'Cratera em crescimento próxima a área escolar exige prioridade crítica.', TRUE, 1, 'CRITICA', NULL, '2026-09-01T09:26:00-03:00'),
    (19, 'Vegetação alta prejudica a visibilidade na esquina.', TRUE, 7, 'BAIXA', NULL, '2026-09-01T09:31:00-03:00'),
    (20, 'Relato semelhante ao registro 5 no mesmo ponto de drenagem.', TRUE, 5, 'MEDIA', 5, '2026-09-01T09:36:00-03:00');

INSERT INTO historico_status
    (id_ocorrencia, id_status, id_usuario_responsavel, observacao, alterado_em)
SELECT
    id_ocorrencia,
    id_status,
    2,
    'Carga inicial do Módulo 7',
    atualizado_em
FROM ocorrencia
ORDER BY id_ocorrencia;

INSERT INTO atendimento
    (id_ocorrencia, id_equipe, inicio_em, fim_em, observacao)
VALUES
    (3, 1, '2026-09-01T08:30:00-03:00', NULL, 'Sinalização provisória instalada.'),
    (9, 3, '2026-09-01T09:00:00-03:00', NULL, 'Equipe deslocada para remoção dos resíduos.'),
    (11, 1, '2026-09-01T09:05:00-03:00', NULL, 'Área isolada para avaliação da drenagem.'),
    (12, 2, '2026-09-01T09:10:00-03:00', '2026-09-01T10:00:00-03:00', 'Luminária revisada e testada.'),
    (17, 3, '2026-09-01T09:35:00-03:00', NULL, 'Vazamento em verificação técnica.');

SELECT setval(pg_get_serial_sequence('usuario', 'id_usuario'), (SELECT MAX(id_usuario) FROM usuario), TRUE);
SELECT setval(pg_get_serial_sequence('categoria', 'id_categoria'), (SELECT MAX(id_categoria) FROM categoria), TRUE);
SELECT setval(pg_get_serial_sequence('status_ocorrencia', 'id_status'), (SELECT MAX(id_status) FROM status_ocorrencia), TRUE);
SELECT setval(pg_get_serial_sequence('equipe', 'id_equipe'), (SELECT MAX(id_equipe) FROM equipe), TRUE);
SELECT setval(pg_get_serial_sequence('ocorrencia', 'id_ocorrencia'), (SELECT MAX(id_ocorrencia) FROM ocorrencia), TRUE);

COMMIT;
