"""Mapeamento das tabelas simples já existentes no PostgreSQL."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Identity, Integer, SmallInteger, String, text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

small_pk = SmallInteger().with_variant(Integer, "sqlite")
big_pk = BigInteger().with_variant(Integer, "sqlite")


class Categoria(Base):
    __tablename__ = "categoria"

    id_categoria: Mapped[int] = mapped_column(
        small_pk, Identity(always=True), primary_key=True
    )
    codigo: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255))
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))


class StatusOcorrencia(Base):
    __tablename__ = "status_ocorrencia"

    id_status: Mapped[int] = mapped_column(
        small_pk, Identity(always=True), primary_key=True
    )
    codigo: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    ordem: Mapped[int] = mapped_column(SmallInteger, unique=True, nullable=False)
    status_final: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))


class Equipe(Base):
    __tablename__ = "equipe"

    id_equipe: Mapped[int] = mapped_column(
        big_pk, Identity(always=True), primary_key=True
    )
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    criado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
