-- Dados de referência coerentes com os códigos do modelo canônico.
BEGIN;

INSERT INTO status_ocorrencia (codigo, nome, ordem, status_final) VALUES
    ('RECEBIDA', 'Recebida', 1, FALSE),
    ('EM_ANALISE', 'Em análise', 2, FALSE),
    ('ENCAMINHADA', 'Encaminhada', 3, FALSE),
    ('EM_ATENDIMENTO', 'Em atendimento', 4, FALSE),
    ('RESOLVIDA', 'Resolvida', 5, TRUE);

INSERT INTO categoria (codigo, nome, descricao, ativo) VALUES
    ('INFRAESTRUTURA', 'Infraestrutura', 'Problemas em vias e estruturas públicas', TRUE),
    ('ILUMINACAO', 'Iluminação', 'Falhas de iluminação pública', TRUE),
    ('TRANSITO', 'Trânsito', 'Sinalização e circulação viária', TRUE),
    ('ARBORIZACAO', 'Arborização', 'Árvores e manejo em espaços públicos', TRUE),
    ('DRENAGEM', 'Drenagem', 'Escoamento e alagamentos', TRUE),
    ('CONSERVACAO', 'Conservação', 'Conservação de equipamentos e espaços', TRUE),
    ('LIMPEZA_URBANA', 'Limpeza urbana', 'Resíduos, entulho e vegetação', TRUE),
    ('SANEAMENTO', 'Saneamento', 'Ocorrências relacionadas a água e saneamento', TRUE);

COMMIT;
