"""Aplicação FastAPI do Radar Urbano. Execute na raiz com backend.main:app."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .controller.resumo import router as resumo_router
from .controller.dashboard import router as dashboard_router
from .controller.chat import router as chat_router

app = FastAPI(
    title="Radar Urbano - API de Dados",
    description="Indicadores e consultas descritivas das ocorrências urbanas.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:5502",
        "http://localhost:5502",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(resumo_router)
app.include_router(dashboard_router)
app.include_router(chat_router)


@app.get("/", tags=["Saúde"])
def home():
    return {"status": "ok", "mensagem": "API Radar Urbano funcionando.", "documentacao": "/docs"}


@app.get("/health", tags=["Saúde"])
def health():
    return {"status": "healthy"}


@app.exception_handler(FileNotFoundError)
async def arquivo_nao_encontrado(request: Request, erro: FileNotFoundError):
    return JSONResponse(status_code=503, content={"detail": "Arquivo CSV não encontrado na pasta database."})


@app.exception_handler(ValueError)
async def dados_invalidos(request: Request, erro: ValueError):
    return JSONResponse(status_code=503, content={"detail": f"Não foi possível analisar o CSV: {erro}"})
