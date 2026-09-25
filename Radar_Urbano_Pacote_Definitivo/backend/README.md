# Backend

API FastAPI do Módulo 6. As rotas iniciais trabalham somente com tabelas de chave primária simples e sem chave estrangeira: `categoria`, `status_ocorrencia` e `equipe`.

```bash
uvicorn backend.main:app --reload
```

- Swagger: `http://127.0.0.1:8000/docs`
- Testes: `pytest -q`
- Análise de IA: `python -m backend.executar_analise`

O banco deve existir previamente no Supabase. A API lê `DATABASE_URL` do arquivo local `.env`, que não pode ser publicado.
