"""Executa Uvicorn de verdade com SQLite isolado, testa HTTP e encerra o servidor."""
from pathlib import Path
from tempfile import TemporaryDirectory
from subprocess import Popen
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
import os,sys,json,time,socket
from sqlalchemy.orm import Session
from backend.database import Base,criar_engine
from backend.models import Usuario,StatusOcorrencia

RAIZ=Path(__file__).resolve().parents[1]
EVID=RAIZ/'evidencias'


def pedido(url,metodo='GET',dados=None):
    req=Request(url,method=metodo,data=json.dumps(dados).encode() if dados else None,
                headers={'Content-Type':'application/json'})
    try:
        resposta=urlopen(req,timeout=5)
    except HTTPError as erro:
        resposta=erro
    with resposta:
        return resposta.status,json.load(resposta)


with TemporaryDirectory() as p:
    endereco='sqlite:///'+str(Path(p)/'http.db')
    engine=criar_engine(endereco)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add_all([Usuario(nome='Cidadão fictício',email='http@example.invalid',perfil='CIDADAO'),
                    StatusOcorrencia(codigo='RECEBIDA',nome='Recebida',ordem=1)])
        db.commit()
    engine.dispose()
    with socket.socket() as s:
        s.bind(('127.0.0.1',0));porta=s.getsockname()[1]
    base='http://127.0.0.1:'+str(porta)
    with (EVID/'uvicorn_http_local.txt').open('w') as log:
        proc=Popen([sys.executable,'-m','uvicorn','backend.main:app','--host','127.0.0.1','--port',str(porta)],
                   cwd=RAIZ,env=os.environ|{'DATABASE_URL':endereco},stdout=log,stderr=log)
        try:
            for _ in range(50):
                try:
                    codigo,_=pedido(base+'/saude');break
                except URLError:
                    time.sleep(.1)
            else:
                raise RuntimeError('Uvicorn não iniciou.')
            registros=[]
            def executar(rota,metodo='GET',corpo=None,esperado=200):
                c,r=pedido(base+rota,metodo,corpo)
                assert c==esperado,(rota,c,r)
                registros.append({'metodo':metodo,'rota':rota,'status':c,'resposta':r})
                return r
            executar('/saude/banco')
            cat=executar('/categorias','POST',{'codigo':'INFRAESTRUTURA','nome':'Infraestrutura'},201)
            entrada={'id_usuario':1,'id_categoria':cat['id_categoria'],'descricao':'Buraco no exemplo HTTP local.',
                     'latitude':-23.42,'longitude':-51.93,'prioridade':'ALTA'}
            executar('/ocorrencias','POST',entrada,201)
            ocorrencias=executar('/ocorrencias')
            assert ocorrencias[0]['categoria_nome']=='Infraestrutura'
            executar('/ocorrencias','POST',entrada|{'id_categoria':30000},404)
            for n in ['resumo','categorias','datas']:
                executar('/analises/'+n)
            (EVID/'json/http_local.json').write_text(json.dumps({'ambiente':'Uvicorn real via HTTP; SQLite temporário, não Supabase',
                             'iniciou_e_encerrou':True,'requisicoes':registros},ensure_ascii=False,indent=2))
        finally:
            proc.terminate()
            proc.wait(timeout=10)
print('8 requisições HTTP conferidas; Uvicorn iniciado e encerrado; banco SQLite temporário.')
