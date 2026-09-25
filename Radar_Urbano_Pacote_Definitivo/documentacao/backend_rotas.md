# Backend e primeiras rotas — Módulo 6

## Tabelas escolhidas

| Tabela | Motivo | GET | POST |
| --- | --- | --- | --- |
| `categoria` | PK simples e nenhuma FK | `/categorias` | `/categorias` |
| `status_ocorrencia` | PK simples e nenhuma FK | `/status-ocorrencia` | `/status-ocorrencia` |
| `equipe` | PK simples e nenhuma FK | `/equipes` | `/equipes` |

Os campos dos modelos e schemas seguem `database/script_ddl.sql` e `docs/03_dicionario_dados.md`. O backend não cria nem altera o banco; ele acessa as tabelas existentes.

## Fluxo do dado

Postman ou interface envia HTTP → FastAPI valida o JSON com Pydantic → SQLAlchemy representa a tabela → Psycopg comunica com PostgreSQL → Supabase persiste ou consulta → a API devolve JSON.

SQLAlchemy organiza o mapeamento e as operações em Python. Psycopg é o driver que efetivamente fala o protocolo do PostgreSQL. Eles trabalham juntos, mas têm funções diferentes.

## Preparar e executar

```bash
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
uvicorn backend.main:app --reload
```

No Windows CMD, a ativação é `venv\Scripts\activate`. No PowerShell, use `.\venv\Scripts\Activate.ps1`.

Preencha `DATABASE_URL` no `.env` com os dados do próprio Supabase. O `.env` está bloqueado no `.gitignore` e nunca deve ser enviado ao GitHub.

## Testar

Importe `postman/Radar_Urbano_Modulo_6.postman_collection.json`, inicie a API e execute primeiro os GETs. Para cada POST, confira o status `201`, repita o GET e verifique o novo registro no Supabase. Um registro repetido retorna `409`; JSON fora do schema retorna `422`.

Testes automatizados locais, sem usar o banco real:

```bash
pytest -q
```

## Persistência

O POST está comprovado quando a resposta retorna `201` com o ID gerado e o registro reaparece em um GET posterior e/ou na tabela correspondente do Supabase.

