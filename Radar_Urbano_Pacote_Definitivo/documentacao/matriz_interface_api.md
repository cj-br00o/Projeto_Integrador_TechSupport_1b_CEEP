# Matriz interface, API e banco

| Funcionalidade | Campo da interface | JSON | Tabela.campo |
| --- | --- | --- | --- |
| Cadastrar categoria | Código | `codigo` | `categoria.codigo` |
| Cadastrar categoria | Nome | `nome` | `categoria.nome` |
| Cadastrar categoria | Descrição | `descricao` | `categoria.descricao` |
| Cadastrar categoria | Ativa | `ativo` | `categoria.ativo` |
| Cadastrar status | Código | `codigo` | `status_ocorrencia.codigo` |
| Cadastrar status | Nome | `nome` | `status_ocorrencia.nome` |
| Cadastrar status | Ordem | `ordem` | `status_ocorrencia.ordem` |
| Cadastrar status | Status final | `status_final` | `status_ocorrencia.status_final` |
| Cadastrar equipe | Nome | `nome` | `equipe.nome` |
| Cadastrar equipe | Especialidade | `especialidade` | `equipe.especialidade` |
| Cadastrar equipe | Ativa | `ativa` | `equipe.ativa` |

As listas de consulta usam os mesmos campos e exibem os IDs gerados pelo banco.

