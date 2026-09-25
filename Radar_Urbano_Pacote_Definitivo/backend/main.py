"""Aplicação FastAPI do Radar Urbano."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .analise import obter_resumo
from .routes.categorias import router as categorias_router
from .routes.equipes import router as equipes_router
from .routes.status_ocorrencia import router as status_router
from .schemas import AnaliseResumoResponse

app = FastAPI(
    title="Radar Urbano API",
    description="Rotas iniciais de gestão e resumo analítico do projeto acadêmico.",
    version="6.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(categorias_router)
app.include_router(status_router)
app.include_router(equipes_router)


@app.get("/", tags=["Sistema"])
def inicio():
    return {"projeto": "Radar Urbano", "modulo": 6, "status": "online"}


@app.get("/saude", tags=["Sistema"])
def saude():
    return {"status": "ok"}


@app.get("/analises/resumo", response_model=AnaliseResumoResponse, tags=["Inteligência"])
def resumo_analitico():
    return obter_resumo()
