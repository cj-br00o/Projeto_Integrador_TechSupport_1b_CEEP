# Qualidade Segurança e Privacidade

## Qualidade dos dados

- Identificadores e protocolos devem ser únicos.
- Campos obrigatórios não podem ficar vazios.
- Coordenadas devem permanecer dentro das faixas geográficas matematicamente válidas.
- Códigos de domínio devem corresponder aos valores cadastrados ou às restrições do DDL.
- Datas de encerramento não podem anteceder datas de início.
- Referências de duplicidade precisam apontar para outra ocorrência existente.
- A view de exportação escolhe a análise mais recente e uma referência de foto para evitar multiplicar linhas.

## Privacidade

A massa usa descrições de situações urbanas fictícias, protocolos fictícios e endereços de arquivo inexistentes. Não contém nome, telefone, documento, endereço residencial ou e-mail real de cidadão. O DDL possui a tabela `usuario` porque o sistema precisa controlar autoria e permissões, mas esses dados não fazem parte do CSV de teste da IA.

## Segurança

O repositório não deve armazenar senha, token, chave de API nem string de conexão com credenciais. Configurações locais devem usar variáveis de ambiente e arquivos ignorados pelo Git. O escopo desta documentação não define um mecanismo específico de autenticação, pois esse detalhe não foi fornecido no material original.

## Responsabilidade humana

O campo `valido` representa uma indicação técnica da análise. Ele não substitui a verificação da prefeitura. Da mesma forma, `id_categoria_sugerida`, `prioridade_sugerida` e `id_ocorrencia_duplicada` são sugestões preservadas em `analise_ia`; os campos confirmados continuam em `ocorrencia`.
