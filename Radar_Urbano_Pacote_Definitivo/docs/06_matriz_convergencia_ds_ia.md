# Matriz de Convergência DS e IA

| Questão | DS | IA | Decisão comum | Situação |
| --- | --- | --- | --- | --- |
| Qual problema resolvemos? | Centralizar relatos urbanos e permitir acompanhamento. | Apoiar classificação, priorização e reconhecimento de semelhança. | A ocorrência é a unidade central do fluxo. | Convergente |
| O que precisamos controlar ou conhecer? | Usuários, ocorrências, categorias, fotos, localização, status, equipes, atendimentos e histórico. | Descrição, validade, resumo, categoria sugerida, prioridade sugerida e possível duplicidade. | Dados confirmados e sugestões permanecem separados. | Convergente |
| Quais dados são necessários? | Descrição, foto referenciada, coordenadas, datas, categoria, status, prioridade e responsáveis. | Descrição, referência da foto, localização e histórico de análises ou ocorrências. | Somente dados vinculados à ocorrência alimentam o teste. | Convergente |
| Onde os dados são obtidos? | Cadastro do cidadão e atualizações da prefeitura e das equipes. | Entrada da ocorrência e registros já existentes no sistema. | Cada origem está ligada a uma etapa do fluxo. | Convergente |
| Onde são armazenados? | PostgreSQL nas nove tabelas do modelo canônico. | Cada execução relevante gera uma linha em `analise_ia`. | O histórico não é sobrescrito. | Convergente |
| Quais dados alimentam a IA? | A view disponibiliza descrição, coordenadas, categoria, status, prioridade, foto referenciada e análise recente. | O teste usa as 16 colunas documentadas do CSV. | Não exportar dados pessoais desnecessários. | Convergente |
| O que a IA produz? | DS recebe uma saída estruturada para persistência e consulta. | Resumo, validade, categoria sugerida, prioridade sugerida e possível duplicidade. | A saída é vinculada à ocorrência em `analise_ia`. | Convergente |
| O resultado retorna ao banco? | Sim, quando possui valor operacional ou de auditoria. | Sim, como nova análise; não como substituição silenciosa. | Campos confirmados de `ocorrencia` só mudam após validação humana. | Convergente |
| O que o usuário recebe? | Protocolo, status confirmado e acompanhamento. | Organização interna do relato para apoiar a triagem. | Sugestão automática não é apresentada como decisão pública. | Convergente |
| Isso atende à proposta inicial? | O modelo sustenta cadastro, consulta, filtros, mapa e histórico previstos. | Os dados permitem teste verificável de prioridade e duplicidade. | Atende ao escopo modelado e mantém a decisão final humana. | Convergente |
