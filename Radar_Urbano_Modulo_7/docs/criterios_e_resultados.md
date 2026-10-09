# Verificação dos objetivos

| Objetivo | Entrega verificável | Situação |
|---|---|---|
| Ambiente e dependências | requirements.txt e comandos do README | Preparado; testes executados com dependências disponíveis |
| Conexão e modelos | database.py, models.py e schemas.py | Implementado; PostgreSQL pendente de acesso |
| Entidade com PK | POST e GET /categorias | Testado localmente |
| Segunda entidade com FK | POST e GET /ocorrencias | Testado localmente |
| Referência inexistente | 404 sem ocorrência ou histórico gravados | Testado localmente |
| Informação relacionada | categoria_nome e status_nome no JSON | Testado localmente |
| Erros de entrada e unicidade | 400, 404, 409 e 422 | Testado localmente |
| CSV desnormalizado | database/dados.csv e dicionário analítico | Fonte anterior preservada |
| Qualidade e temporalidade | ler_dados e /analises/qualidade | Testado localmente |
| Contagens, soma, média e mediana | resumo.json e conferência independente | Totais reconciliados |
| Agrupamento por dimensão e data | categorias.json e datas.json | Totais reconciliados |
| JSON para dashboard | Três respostas principais e OpenAPI | Produzido pela API |
| Capturas de /docs ou Postman | evidencias/capturas | Pendente de execução na sessão do estudante |
| Backend no Supabase | /saude/banco e registros persistidos | Não executado nesta sessão |
| Código no GitHub | Pasta Radar_Urbano_Modulo_7 no repositório da equipe | Publicado pela interface do GitHub em 09/10/2026 (UTC) |
| Autonomia e participação | Roteiro de início, parada e ficha da equipe | Demonstração pessoal pendente |

35 testes automatizados foram aprovados. O log e o XML detalham as execuções. A conferência do modelo verifica nomes, PK, FK e nulabilidade de seis tabelas mapeadas, sem executar o DDL PostgreSQL. As outras três tabelas permanecem no DDL; não receberam rotas nesta avaliação.
