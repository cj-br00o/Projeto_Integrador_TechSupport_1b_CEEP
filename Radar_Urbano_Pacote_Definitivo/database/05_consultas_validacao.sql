-- Consultas de conferência do modelo.

-- Contagem por prioridade
SELECT prioridade, COUNT(*) AS quantidade
FROM ocorrencia
GROUP BY prioridade
ORDER BY prioridade;

-- Ocorrências altas ou críticas
SELECT id_ocorrencia, protocolo, prioridade
FROM ocorrencia
WHERE prioridade IN ('ALTA', 'CRITICA')
ORDER BY id_ocorrencia;

-- Histórico de uma ocorrência
SELECT hs.id_ocorrencia, so.codigo AS status_codigo,
       hs.id_usuario_responsavel, hs.observacao, hs.alterado_em
FROM historico_status hs
JOIN status_ocorrencia so ON so.id_status = hs.id_status
WHERE hs.id_ocorrencia = :id_ocorrencia
ORDER BY hs.alterado_em;

-- Exportação com as mesmas colunas do CSV
SELECT *
FROM vw_ocorrencia_exportacao_ia
ORDER BY id_ocorrencia;
