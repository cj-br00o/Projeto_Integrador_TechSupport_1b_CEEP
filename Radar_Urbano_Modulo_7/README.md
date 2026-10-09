# Radar Urbano Módulo 7

Entrega autoral da avaliação Integração do Backend. Uma aplicação FastAPI reúne o backend de gestão e as rotas analíticas. Os três documentos recebidos da escola são guias e não foram preenchidos nem incluídos como respostas.

## O que foi executado

- 35 testes automatizados aprovados com SQLite temporário e chaves estrangeiras habilitadas.
- POST e GET de categoria e ocorrência, referências válidas, nomes relacionados e histórico inicial.
- Leitura e validação do CSV anterior, três rotas analíticas principais e uma rota de qualidade.
- JSONs produzidos pela API, conferência manual dos cálculos e comparação estática de seis modelos com o banco canônico de nove tabelas.

Os testes locais não comprovam conexão ao Supabase. A sessão não tinha DATABASE_URL nem credenciais do projeto. Não há capturas de Supabase, Postman ou Swagger apresentadas como testes já realizados. A publicação do Módulo 7 no GitHub foi realizada em 9 de outubro de 2026 (UTC), em Radar_Urbano_Modulo_7. A demonstração escolar permanece pendente. A conta acessível no Supabase apresentou outro projeto, com tabelas de merenda; esse banco não foi alterado.

## Arquivos principais

| Caminho | Responsabilidade |
|---|---|
| backend/database.py | Conexão, engine, sessões e fechamento |
| backend/models.py | Mapeamento de seis tabelas usadas nesta etapa |
| backend/schemas.py | Validação das entradas e formato das respostas |
| backend/main.py | Única aplicação FastAPI e integração das rotas |
| backend/routes/ocorrencias.py | Cadastro, consulta, validação de FK e histórico |
| backend/analise.py | Validação do CSV e cálculos com Pandas |
| database/dados.csv | Fonte sintética anterior, uma linha por ocorrência |
| database/script_ddl.sql | Estrutura PostgreSQL das nove tabelas existentes |
| database/script_seed.sql | Massa sintética para banco acadêmico vazio |
| postman/Radar_Urbano_Modulo_7.postman_collection.json | Requisições e verificações para executar no Postman |
| evidencias/json | Respostas reais de testes locais e contrato OpenAPI |
| tests | Casos automatizados de sucesso, erro e análise |
| docs | Dicionários, perguntas, cálculos, integração e limites |

## Preparar e iniciar

Abra o terminal na pasta Radar_Urbano_Modulo_7.

```bash
python -m venv .venv
```

Ative somente com o comando do seu terminal:

```text
Windows Prompt de Comando: .venv\Scripts\activate.bat
Windows PowerShell: .venv\Scripts\Activate.ps1
Linux: source .venv/bin/activate
```

Depois execute:

```bash
python -m pip install -r requirements.txt
```

Copie .env.example para .env e informe a conexão PostgreSQL do projeto Supabase. Use os dados do painel do seu próprio projeto e sslmode=require. A URL deve usar postgresql+psycopg://. Senhas com caracteres especiais devem ser codificadas para URL. Não publique .env.

O backend não cria ou altera tabelas ao iniciar. Se o banco existente já possui as nove tabelas, use-o sem reexecutar o DDL. Para um banco novo de teste, execute script_ddl.sql e depois script_seed.sql. O seed recusa bancos com os registros principais já existentes.

```bash
python -m backend.analise
python -m pytest -q
python -m uvicorn backend.main:app --reload
```

Abra http://127.0.0.1:8000/docs. A análise funciona mesmo sem a conexão de gestão; a leitura vem exclusivamente do CSV. Para comprovar Supabase, GET /saude/banco deve retornar banco=postgresql e os cadastros precisam aparecer no projeto correto.

## Teste de gestão no Supabase

1. Consulte GET /categorias e GET /status-ocorrencia. O banco precisa do código RECEBIDA.
2. Cadastre uma categoria de teste ou use uma ativa existente. Anote o ID real devolvido.
3. Cadastre um cidadão fictício em POST /usuarios e anote o ID real.
4. Envie POST /ocorrencias com esses IDs, descrição, coordenadas e prioridade válida.
5. Consulte GET /ocorrencias e confirme categoria_nome e status_nome.
6. Repita o POST com id_categoria=30000, somente se esse ID não existir, para conferir 404. Um ID acima de 32767 é rejeitado como 422 por exceder SMALLINT.
7. Confira o histórico inicial. Teste também categoria duplicada (409) e latitude=91 (422).
8. Salve capturas reais de /docs ou Postman mostrando método, rota, código HTTP e resposta, em evidencias/capturas.

O Postman tem variáveis de coleção base_url, id_categoria e id_usuario. As respostas de cadastro atualizam os IDs para os pedidos seguintes. A requisição de erro deve usar um ID realmente ausente.

## Apenas demonstração local sem Supabase

```bash
python -m scripts.preparar_demo_local
```

Na raiz do projeto, use DATABASE_URL=sqlite:///demo_local.db. Exemplo no Prompt de Comando do Windows: `set DATABASE_URL=sqlite:///demo_local.db`. Exemplo no PowerShell: `$env:DATABASE_URL='sqlite:///demo_local.db'`. Exemplo no Linux: `export DATABASE_URL=sqlite:///demo_local.db`.

Depois inicie Uvicorn. Este modo é SQLite e não substitui a demonstração do PostgreSQL. Remova a variável de demonstração antes de usar .env com Supabase, pois variáveis do terminal têm prioridade.

## Registrar os resultados

```bash
python -m scripts.registrar_evidencias
python -m scripts.verificar_modelo
python -m scripts.exportar_json_http
```

O primeiro comando reproduz os registros locais em SQLite temporário. O último consulta a aplicação HTTP realmente iniciada e grava arquivos em evidencias/http. Ele não simula uma conexão Supabase.

## Encerrar e retomar

Pressione Ctrl+C no terminal do servidor, aguarde o prompt e execute `deactivate`. Para retomar, ative a .venv e inicie Uvicorn novamente. Os registros do banco permanecem salvos.

## Versionar e entregar

Suba os arquivos e pastas extraídos, não apenas o ZIP, ao repositório já usado pelo grupo. Revise o .gitignore e mantenha credenciais e .venv fora do repositório. A pasta backend deve ser integrada à versão anterior com comparação do código, sem manter dois apps conflitantes.

```bash
git add .
git commit -m "modulo 7 backend de ocorrencias e analise CSV"
git push
```

A ficha da escola deve registrar números, turmas, cursos, papéis efetivamente desempenhados e nota do professor. Esses dados não foram presumidos. Entregue os relatórios novos e o código; os cadernos de orientação não foram anexados como respostas.
