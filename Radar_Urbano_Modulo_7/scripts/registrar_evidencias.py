"""Registra respostas reais da API em TestClient com banco SQLite temporário."""
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime,timezone
import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from backend.database import Base, criar_engine, get_db
from backend.main import app
from backend.models import Usuario,StatusOcorrencia

RAIZ=Path(__file__).resolve().parents[1]
SAIDA=RAIZ/'evidencias'
SAIDA.mkdir(exist_ok=True)


def salvar(nome,conteudo):
    (SAIDA/'json'/nome).write_text(json.dumps(conteudo,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')


with TemporaryDirectory() as pasta:
    engine=criar_engine('sqlite:///'+str(Path(pasta)/'evidencias.db'))
    Base.metadata.create_all(engine)
    factory=sessionmaker(bind=engine,expire_on_commit=False)
    with factory() as db:
        db.add_all([Usuario(nome='Cidadão fictício',email='ficticio@example.invalid',perfil='CIDADAO'),
                    StatusOcorrencia(codigo='RECEBIDA',nome='Recebida',ordem=1)])
        db.commit()
    def sessao():
        with factory() as db:
            yield db
    app.dependency_overrides[get_db]=sessao
    trilha=[]
    with TestClient(app) as cliente:
        def executar(metodo,rota,corpo=None):
            resposta=cliente.request(metodo,rota,json=corpo)
            trilha.append({'metodo':metodo,'rota':rota,'entrada':corpo,'status':resposta.status_code,'resposta':resposta.json()})
            return resposta
        c=executar('POST','/categorias',{'codigo':'INFRAESTRUTURA','nome':'Infraestrutura'})
        executar('GET','/categorias')
        entrada={'id_usuario':1,'id_categoria':c.json()['id_categoria'],'descricao':'Buraco em via de demonstração.',
                 'latitude':-23.42,'longitude':-51.93,'prioridade':'ALTA'}
        executar('POST','/ocorrencias',entrada)
        executar('GET','/ocorrencias')
        executar('POST','/ocorrencias',entrada|{'id_categoria':30000})
        executar('POST','/ocorrencias',entrada|{'latitude':91})
        executar('POST','/categorias',{'codigo':'INFRAESTRUTURA','nome':'Infraestrutura'})
        for nome in ['resumo','categorias','datas','qualidade']:
            r=executar('GET','/analises/'+nome)
            assert r.status_code==200
            salvar(nome+'.json',r.json())
        salvar('openapi.json',cliente.get('/openapi.json').json())
    salvar('requisicoes_ds_ia.json',{'executado_em_utc':datetime.now(timezone.utc).isoformat(),
           'ambiente':'FastAPI TestClient com SQLite temporário; não é Supabase ou Postman',
           'requisicoes':trilha})
    app.dependency_overrides.clear()
    engine.dispose()
print('Respostas reais da API registradas em evidencias/json. Ambiente: SQLite temporário.')
