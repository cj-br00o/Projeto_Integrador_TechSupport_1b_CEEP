"""Contratos de entrada e saída da API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class CategoriaCreate(SchemaBase):
    codigo: str = Field(min_length=2, max_length=40, pattern=r"^[A-Z][A-Z0-9_]*$")
    nome: str = Field(min_length=2, max_length=80)
    descricao: str | None = Field(default=None, max_length=255)
    ativo: bool = True


class CategoriaResponse(CategoriaCreate):
    id_categoria: int


class StatusCreate(SchemaBase):
    codigo: str = Field(min_length=2, max_length=30, pattern=r"^[A-Z][A-Z0-9_]*$")
    nome: str = Field(min_length=2, max_length=50)
    ordem: int = Field(gt=0, le=32767)
    status_final: bool = False


class StatusResponse(StatusCreate):
    id_status: int


class EquipeCreate(SchemaBase):
    nome: str = Field(min_length=2, max_length=100)
    especialidade: str = Field(min_length=2, max_length=100)
    ativa: bool = True


class EquipeResponse(EquipeCreate):
    id_equipe: int
    criado_em: datetime


class AnaliseResumoResponse(SchemaBase):
    registros: int
    tempo_analise_media_min: float
    tempo_analise_mediana_min: float
    ocorrencias_urgentes: int
    categoria_mais_frequente: str
    possiveis_duplicidades: int

