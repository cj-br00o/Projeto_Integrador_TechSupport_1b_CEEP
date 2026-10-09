from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
import pandas as pd
from . import analise
from .database import get_db
from .routes.categorias import router as categorias
from .routes.status_ocorrencia import router as status
from .routes.equipes import router as equipes
from .routes.ocorrencias import router as ocorrencias

app = FastAPI(title='Radar Urbano API',version='7.0.0',
              description='Gestão com PostgreSQL e análise independente do CSV acadêmico.')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5500','http://127.0.0.1:5500'],
                   allow_methods=['GET','POST'], allow_headers=['Content-Type'])
for router in [categorias,status,equipes,ocorrencias]:
    app.include_router(router)


@app.exception_handler(OperationalError)
async def banco_indisponivel(request: Request, erro):
    return JSONResponse(status_code=503, content={'detail':'Banco indisponível. Confira a conexão local.'})


@app.get('/',tags=['Sistema'])
def inicio():
    return {'projeto':'Radar Urbano','modulo':7,'status':'online'}


@app.get('/saude',tags=['Sistema'])
def saude():
    return {'status':'ok'}


@app.get('/saude/banco',tags=['Sistema'])
def saude_banco(db: Session = Depends(get_db)):
    db.execute(text('SELECT 1'))
    return {'status':'ok','banco':db.bind.dialect.name}


def carregar_dados():
    try:
        return analise.ler_dados()
    except (OSError,UnicodeError) as erro:
        raise HTTPException(503,'Não foi possível ler database/dados.csv.') from erro
    except (ValueError,pd.errors.ParserError) as erro:
        raise HTTPException(422,'CSV inválido. '+str(erro)) from erro


@app.get('/analises/resumo',tags=['Análise de dados'])
def consultar_resumo():
    return analise.resumo(carregar_dados())


@app.get('/analises/categorias',tags=['Análise de dados'])
def consultar_categorias():
    return analise.por_categoria(carregar_dados())


@app.get('/analises/datas',tags=['Análise de dados'])
def consultar_datas():
    return analise.por_data(carregar_dados())


@app.get('/analises/qualidade',tags=['Análise de dados'])
def consultar_qualidade():
    return analise.qualidade(carregar_dados())
