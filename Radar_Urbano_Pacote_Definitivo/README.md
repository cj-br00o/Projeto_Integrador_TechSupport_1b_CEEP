# Radar Urbano — Módulo 6

Entrega integrada de Desenvolvimento de Sistemas e Inteligência Artificial. O banco validado no Módulo 5 passa a atender uma API FastAPI, uma interface administrativa e uma camada analítica reproduzível baseada no CSV do próprio projeto.

Os dados são fictícios e servem somente para avaliação acadêmica. O projeto não afirma implantação oficial pela Prefeitura de Maringá.

## Desenvolvimento de Sistemas

- ambiente Python reproduzível em `requirements.txt`;
- conexão PostgreSQL/Supabase em `backend/database.py`;
- modelos coerentes com o DDL em `backend/models.py`;
- schemas de entrada e saída em `backend/schemas.py`;
- GET e POST para `categoria`, `status_ocorrencia` e `equipe`;
- coleção Postman em `postman/`;
- testes automatizados em `tests/`;
- interface de cadastro e consulta em `frontend/gestao.html`;
- documentação e matriz de rastreabilidade em `documentacao/`.

As três tabelas foram escolhidas porque possuem chave primária simples e nenhuma chave estrangeira, exatamente como pede o guia do módulo.

## Inteligência Artificial

- fonte oficial em `database/dados.csv`;
- carregamento, preparação, estatística, agregação e classificação em `backend/analise.py`;
- execução reproduzível em `backend/executar_analise.py`;
- resultado JSON e gráfico em `evidencias/ia/`;
- perguntas, resultados, interpretação e limites em `documentacao/analise_dados.md`;
- endpoint integrado `GET /analises/resumo` para uso futuro pelo dashboard.

## Preparar o ambiente

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows CMD:

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Conectar ao Supabase

1. Copie `.env.example` para `.env`.
2. Preencha `DATABASE_URL` com a conexão do projeto acadêmico.
3. Não execute `Base.metadata.create_all()`: as tabelas já existem pelo DDL.
4. Nunca envie `.env`, senha, token ou string real ao GitHub.

## Executar e testar a API

```bash
uvicorn backend.main:app --reload
pytest -q
```

Abra `http://127.0.0.1:8000/docs` para conferir os endpoints. Importe a coleção em `postman/`, faça o GET inicial, o POST, um novo GET e confirme a persistência no Supabase.

| Método | Rota | Finalidade |
| --- | --- | --- |
| GET | `/categorias` | Consultar categorias |
| POST | `/categorias` | Cadastrar categoria |
| GET | `/status-ocorrencia` | Consultar etapas do fluxo |
| POST | `/status-ocorrencia` | Cadastrar etapa |
| GET | `/equipes` | Consultar equipes |
| POST | `/equipes` | Cadastrar equipe |
| GET | `/analises/resumo` | Consultar indicadores do CSV |

## Executar a análise

```bash
python -m backend.executar_analise
```

Resultados esperados para a massa de 20 registros:

- tempo médio e mediano até a análise: 1 minuto;
- 5 ocorrências classificadas como urgentes;
- `INFRAESTRUTURA` como categoria mais frequente, com 4 registros;
- 1 possível duplicidade, ocorrência 20 relacionada à 5.

Esses resultados comprovam o processamento da massa fictícia. O pequeno recorte de uma manhã não sustenta conclusões sobre a cidade real.

## Interface

```bash
python -m http.server 5500 --directory frontend
```

Acesse `http://127.0.0.1:5500/gestao.html`. A API precisa estar ativa em `http://127.0.0.1:8000`.

## Estrutura principal

```text
radar-urbano/
├── backend/
│   ├── routes/
│   ├── analise.py
│   ├── database.py
│   ├── executar_analise.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── database/
│   ├── dados.csv
│   ├── script_ddl.sql
│   ├── script_seed.sql
│   └── script_dql.sql
├── documentacao/
├── evidencias/
├── frontend/
├── postman/
├── tests/
├── .env.example
├── .gitignore
└── requirements.txt
```

Os dois cadernos DOCX usados como orientação não fazem parte da entrega e não devem ser enviados ao GitHub nem ao Classroom.

