"""Rotas de dados agregados usados nos gráficos."""
from fastapi import APIRouter
from ..analise_dashboard import ocorrencias_por_mes, por_gravidade, por_status

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/ocorrencias-por-mes")
def consultar_ocorrencias_por_mes():
    return ocorrencias_por_mes()


@router.get("/gravidade")
def consultar_gravidade():
    return por_gravidade()


@router.get("/status")
def consultar_status():
    return por_status()
