# Radar Urbano

Pacote acadêmico da recuperação de Desenvolvimento de Sistemas e Inteligência Artificial. O conteúdo demonstra a cadeia de validação exigida no guia: problema, solução, dados necessários, dicionário, DER, DDL, CSV, massa de teste, teste de IA e evidência.

## Escopo confirmado

O Radar Urbano é uma proposta acadêmica para Maringá - PR. O cidadão registra uma ocorrência com descrição, fotografia e localização. A prefeitura valida e encaminha o atendimento. As equipes atualizam o andamento. A inteligência artificial apoia a validação, o resumo, a classificação, a priorização e a identificação de possíveis duplicidades.

Este pacote não afirma que o sistema está implantado pela prefeitura nem utiliza dados municipais reais. A massa de testes é totalmente fictícia.

## Fonte oficial dos nomes

O arquivo `docs/modelo_canonico.json` é a fonte técnica oficial deste pacote. O DDL, o dicionário, o DER, o CSV, as matrizes e o relatório final foram construídos com base nele. Os códigos internos usam letras maiúsculas, sem acentos e com sublinhado, por exemplo `EM_ANALISE` e `LIMPEZA_URBANA`. Os nomes apresentados ao usuário podem conter acentos.

## Arquivos principais

| Caminho | Finalidade |
|---|---|
| `Relatorio_Final_Radar_Urbano_Definitivo.docx` | Relatório acadêmico completo |
| `frontend/index.html` | Página principal do protótipo visual |
| `frontend/styles.css` | Estilos responsivos da página principal |
| `backend/README.md` | Delimitação honesta da etapa futura de API |
| `docs/modelo_canonico.json` | Fonte oficial de tabelas, campos, domínios e relações |
| `docs/01_visao_geral.md` | Problema, solução, escopo e limites |
| `docs/02_dicionario_dados.md` | Dicionário detalhado e idêntico ao DDL |
| `docs/der/der_radar_urbano.md` | DER editável em Mermaid |
| `docs/der/der_radar_urbano.svg` | Versão visual do DER |
| `database/01_schema.sql` | DDL PostgreSQL |
| `database/02_dados_referencia.sql` | Categorias e status utilizados pelo modelo |
| `database/03_testes_crud.sql` | Teste transacional de cadastro, leitura, atualização e exclusão |
| `database/04_testes_integridade.sql` | Testes de restrições e relacionamentos |
| `database/05_consultas_validacao.sql` | Consultas de conferência e exportação |
| `data/radar_urbano_ocorrencias_teste.csv` | Massa única com 20 registros fictícios |
| `ia/teste_ollama.md` | Prompt, gabarito e roteiro de evidência |
| `evidencias/relatorio_validacao_automatica.txt` | Resultado das verificações automáticas do pacote |

## Ordem de uso

1. Executar `database/01_schema.sql` em um banco PostgreSQL vazio.
2. Executar `database/02_dados_referencia.sql`.
3. Consultar o dicionário e o DER durante a conferência.
4. Usar o CSV no teste textual de IA.
5. Executar os testes SQL em ambiente de desenvolvimento.
6. Registrar a execução real do Ollama em `ia/teste_ollama.md` e guardar a evidência na pasta `evidencias`.
7. Enviar o pacote ao GitHub com commits identificáveis.

## Estrutura para o GitHub

Envie os arquivos e as pastas descompactados, preservando esta organização:

```text
radar-urbano/
├── backend/
│   └── README.md
├── frontend/
│   ├── index.html
│   └── styles.css
├── database/
├── docs/
├── data/
├── evidencias/
├── ferramentas/
├── ia/
├── README.md
└── Relatorio_Final_Radar_Urbano_Definitivo.docx
```

O arquivo ZIP serve somente para transporte e não deve ser enviado como um único arquivo dentro do repositório.
