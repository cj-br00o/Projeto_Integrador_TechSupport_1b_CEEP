"""Compara os mapeamentos ORM usados nesta etapa com o modelo canônico."""
from pathlib import Path
import json,re
from backend.database import Base
from backend import models

RAIZ=Path(__file__).resolve().parents[1]
fonte=json.loads((RAIZ/'docs/modelo_canonico.json').read_text())
canon={t['name']:t for t in fonte['tables']}
ddl=(RAIZ/'database/script_ddl.sql').read_text()
resultado=[]
for nome,t in Base.metadata.tables.items():
    registro=canon[nome]
    assert set(t.columns.keys())=={f['name'] for f in registro['fields']},nome
    for f in registro['fields']:
        coluna=t.c[f['name']]
        assert coluna.nullable==f['nullable'],(nome,f['name'],'nullable')
        assert coluna.primary_key==(f['key']=='PK'),(nome,f['name'],'PK')
        if f['references']:
            destino=f['references'].replace('(','.').replace(')','')
            assert {fk.target_fullname for fk in coluna.foreign_keys}=={destino},(nome,f['name'],'FK')
    assert re.search(r'CREATE TABLE '+nome+r'\s*\(',ddl)
    resultado.append({'tabela':nome,'nomes_pk_fk_nulabilidade':'conferidos'})
print(json.dumps({'tabelas_mapeadas':len(resultado),'tabelas_no_ddl':len(canon),'resultado':resultado,
                  'escopo':'comparação estática de nomes, PK, FK e nulabilidade; não executa PostgreSQL'},ensure_ascii=False,indent=2))
