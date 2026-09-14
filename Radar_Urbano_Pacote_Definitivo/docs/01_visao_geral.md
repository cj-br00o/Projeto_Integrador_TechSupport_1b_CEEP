# Visão Geral do Radar Urbano

## Problema

Relatos sobre buracos, iluminação, drenagem, arborização, limpeza, conservação, saneamento e trânsito podem chegar por canais diferentes e sem um padrão único. A dispersão dificulta identificar o local, classificar a demanda, reconhecer relatos semelhantes, encaminhar a equipe adequada e acompanhar a solução.

## Solução

O Radar Urbano centraliza o registro e o acompanhamento. O cidadão fornece descrição, localização e fotografia. O sistema cria um protocolo e conserva o estado atual. A IA organiza informações para apoiar a triagem. A prefeitura confere a sugestão e decide o encaminhamento. O atendimento e cada mudança de status ficam registrados.

## Pergunta norteadora

**Os dados que o projeto armazena, organiza ou analisa são coerentes e suficientes para que DS e IA entreguem a solução proposta?**

Sim, dentro do escopo acadêmico modelado. O banco registra a ocorrência, a evidência fotográfica referenciada, os domínios de categoria e status, a prioridade, as análises da IA, os atendimentos e o histórico. O DDL implementa esses elementos; a view os transforma nas 16 colunas documentadas do CSV; e a massa de testes permite conferir prioridade e possível duplicidade sem consultar fontes externas. A resposta não comprova implantação municipal nem execução real do Ollama.

## Entregas previstas

- Protocolo de acompanhamento para cada ocorrência.
- Registro estruturado de descrição, coordenadas, categoria, prioridade e status.
- Vínculo de uma ou mais fotografias com a ocorrência.
- Histórico de análises de IA sem sobrescrever resultados anteriores.
- Identificação de uma possível ocorrência duplicada.
- Encaminhamento para equipes e histórico de atendimento.
- Histórico de alterações de status e responsável por cada alteração.
- Base para filtros, indicadores e mapas no painel da prefeitura.

## Papel da Inteligência Artificial

A IA recebe somente os dados necessários para a análise. Ela pode resumir o relato, indicar se a informação é suficiente, sugerir categoria e prioridade e apontar possível duplicidade. O resultado não substitui a decisão administrativa. A prefeitura continua responsável por confirmar a classificação e o encaminhamento.

## Limites desta recuperação

O pacote valida o modelo de dados, o DDL, a correspondência Banco × CSV e uma massa sintética. O teste documentado do Ollama usa dados textuais e estruturados do CSV. As referências de imagem são fictícias e não representam um conjunto real de imagens. A execução real no Ollama e a publicação no GitHub dependem do computador e do repositório da equipe.

## Alinhamento com as ODS

O projeto foi associado às ODS 9 e 11 por utilizar tecnologia e organização de dados para apoiar infraestrutura e gestão urbana participativa. Essa associação descreve a finalidade acadêmica do projeto, não um resultado público já implantado.
