# Contrato para o dashboard

| Pergunta autoral | Rota e campo | Indicador e unidade | Visual previsto |
|---|---|---|---|
| Quantas ocorrências foram registradas e quantas exigem atenção urgente? | /analises/resumo total_ocorrencias, ocorrencias_urgentes e percentual_urgentes | 20 registros; 5 urgentes; 25% | Cartões e barras de prioridade |
| Quais categorias concentram os relatos? | /analises/categorias categoria_nome e total_ocorrencias | Infraestrutura tem 4 relatos; agrupamentos somam 20 | Barras por categoria |
| Como os registros se distribuem no tempo? | /analises/datas data, total_ocorrencias e urgentes | Em 01/09/2026 há 20 relatos e 5 urgentes | Tabela diária; gráfico de linha apenas com mais datas |

## Significado da fonte

Cada linha representa uma ocorrência distinta, com dados do registro, código da categoria e do status, primeira foto e última análise. A desnormalização reúne informações de tabelas diferentes. Repetir a categoria em várias ocorrências é esperado; repetir o id_ocorrencia não é permitido nesta fonte.

O CSV é sintético, construído nos módulos anteriores. Não representa estatísticas reais de Maringá. As 20 linhas são 20 ocorrências e não 20 fotos, atendimentos ou alterações de status. A possível duplicidade declarada não é uma linha duplicada: a ocorrência 20 aponta para a 5. Nenhuma linha foi removida por isso.

## Conferência manual dos cálculos

Na ocorrência 1: criado_em=01/09/2026 08:00−03:00 e analisado_em=08:01−03:00. A diferença é 60 segundos; 60/60=1 minuto. Um registro já é a operação completa da fonte, porque não há itens de compra neste projeto.

Todos os 20 intervalos da massa valem 1 minuto. Soma=20 minutos; média=20/20=1 minuto. A mediana é a média dos valores das posições 10 e 11 após ordenar: (1+1)/2=1 minuto. A soma descreve os intervalos acumulados e não tempo de trabalho da prefeitura.

ALTA e CRITICA formam o grupo URGENTE: 5/20×100=25%. BAIXA e MEDIA formam ROTINA. A classificação usa a prioridade registrada e não prevê risco com aprendizado de máquina.

Por categoria: 4 Infraestrutura + 3 Trânsito + 3 Drenagem + 3 Limpeza urbana + 2 Iluminação + 2 Arborização + 2 Conservação + 1 Saneamento=20. Os totais de urgentes desses grupos somam 5. A única data da fonte também soma 20 ocorrências e 5 urgentes.

## Premissas e limitações

A diferença de análise usa os instantes com fuso convertidos para UTC. A data de agrupamento volta a America/Sao_Paulo. Não há análise de tendência com um único dia e não são criados dias vazios com zero. Não existe fim_em nesta fonte; portanto não se mede tempo de resolução. Os status são uma fotografia do registro, não a evolução histórica.

O script rejeita campos obrigatórios vazios, ID repetido, valores infinitos, datas inconsistentes, referências de duplicidade ausentes e domínios inválidos. Valores opcionais ausentes são registrados no relatório. Uma ocorrência sem categoria permanece em SEM_CATEGORIA. Uma ocorrência sem análise permanece no total, mas não participa da média nem da mediana; se nenhuma foi analisada, as duas medidas são null.

Os nomes e IDs de categoria usados na análise pertencem à massa de referência atual. Se a equipe mudar categorias ou o recorte da fonte, deve atualizar e revisar esse catálogo. A regra de duplicidade exige que o registro referenciado pertença à fonte atual; outro recorte exigiria mudar e documentar essa premissa.

As rotas leem o CSV a cada consulta. Um POST em /ocorrencias não altera o arquivo automaticamente. Para analisar novos registros, exporte a view vw_ocorrencia_exportacao_ia do banco para CSV, anonimize a fonte e confira o catálogo. Os JSONs antigos são evidências da execução, não um cache da rota.

O dashboard deve consumir as rotas GET. O contrato do resumo evoluiu em relação ao Módulo 6: registros foi substituído por linhas_csv e total_ocorrencias, e os tempos podem ser null. O frontend anterior precisa ser adaptado a esse contrato. Coordenadas das rotas de gestão são decimais serializados como texto; o frontend pode convertê-las para uso no mapa.
