"""Rotas de resumo e detalhamento do Radar Urbano."""
from fastapi import APIRouter
from ..analise import ler_dados, resumo, por_problema, por_bairro

router = APIRouter(prefix="/analise", tags=["Análises"])


@router.get("/resumo")
def consultar_resumo():
    return resumo(ler_dados())


@router.get("/problemas")
def consultar_problemas():
    return por_problema(ler_dados())


@router.get("/bairros")
def consultar_bairros():
    return por_bairro(ler_dados())
