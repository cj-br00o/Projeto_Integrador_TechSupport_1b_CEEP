# Matriz Tela Ação CRUD Tabela Campo

Esta matriz relaciona as ações previstas nas telas aos registros controlados pelo banco. Ela não afirma que todas as telas estejam implementadas; descreve a responsabilidade de dados esperada para cada fluxo.

| Tela ou área | Ação | CRUD | Tabela | Campos principais |
| --- | --- | --- | --- | --- |
| Cadastro e acesso | Cadastrar usuário | C | usuario | nome, email, perfil |
| Nova ocorrência | Criar ocorrência | C | ocorrencia | protocolo, id_usuario, descricao, latitude, longitude, prioridade, id_status |
| Nova ocorrência | Vincular fotografia | C | foto_ocorrencia | id_ocorrencia, url_arquivo |
| Acompanhamento | Consultar protocolo e andamento | R | ocorrencia, status_ocorrencia | protocolo, descricao, prioridade, id_status |
| Triagem | Consultar ocorrência completa | R | ocorrencia, foto_ocorrencia, analise_ia | campos da ocorrência, foto e análise mais recente |
| Triagem | Registrar análise da IA | C | analise_ia | resumo, valido, id_categoria_sugerida, prioridade_sugerida, id_ocorrencia_duplicada |
| Triagem | Confirmar categoria e prioridade | U | ocorrencia | id_categoria, prioridade, atualizado_em |
| Encaminhamento | Criar atendimento | C | atendimento | id_ocorrencia, id_equipe, inicio_em, observacao |
| Atendimento | Atualizar dados do serviço | U | atendimento | inicio_em, fim_em, observacao |
| Gestão | Alterar status | U/C | ocorrencia, historico_status | id_status, atualizado_em; novo evento de histórico |
| Painel | Filtrar e contabilizar ocorrências | R | ocorrencia, categoria, status_ocorrencia | categoria, status, prioridade, datas e coordenadas |
| Administração | Ativar ou desativar domínio | U | categoria, equipe, usuario | ativo ou ativa |
