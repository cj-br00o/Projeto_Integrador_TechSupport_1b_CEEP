"""Mapeamento das tabelas simples já existentes no PostgreSQL."""

from __future__ import annotations

from datetime import datetime

from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, CheckConstraint, DateTime, ForeignKey, Identity, Integer, Numeric, SmallInteger, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class Usuario(Base):
    __tablename__ = 'usuario'
    id_usuario: Mapped[int] = mapped_column(big_pk, Identity(always=True), primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    perfil: Mapped[str] = mapped_column(String(20), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text('true'))
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    __table_args__ = (CheckConstraint("perfil IN ('CIDADAO','PREFEITURA','EQUIPE','ADMINISTRADOR')"),)


class Ocorrencia(Base):
    __tablename__ = 'ocorrencia'
    id_ocorrencia: Mapped[int] = mapped_column(big_pk, Identity(always=True), primary_key=True)
    protocolo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario', ondelete='RESTRICT'), nullable=False)
    id_categoria: Mapped[int | None] = mapped_column(ForeignKey('categoria.id_categoria', ondelete='RESTRICT'))
    id_status: Mapped[int] = mapped_column(ForeignKey('status_ocorrencia.id_status', ondelete='RESTRICT'), nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[Decimal] = mapped_column(Numeric(9,6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(9,6), nullable=False)
    prioridade: Mapped[str] = mapped_column(String(10), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    categoria: Mapped[Categoria | None] = relationship()
    usuario: Mapped[Usuario] = relationship()
    status: Mapped[StatusOcorrencia] = relationship()
    __table_args__ = (
        CheckConstraint('length(trim(descricao)) BETWEEN 10 AND 2000'),
        CheckConstraint('latitude BETWEEN -90 AND 90'),
        CheckConstraint('longitude BETWEEN -180 AND 180'),
        CheckConstraint("prioridade IN ('BAIXA','MEDIA','ALTA','CRITICA')"),
        CheckConstraint('atualizado_em >= criado_em'),
    )


class HistoricoStatus(Base):
    __tablename__ = 'historico_status'
    id_historico: Mapped[int] = mapped_column(big_pk, Identity(always=True), primary_key=True)
    id_ocorrencia: Mapped[int] = mapped_column(ForeignKey('ocorrencia.id_ocorrencia', ondelete='CASCADE'), nullable=False)
    id_status: Mapped[int] = mapped_column(ForeignKey('status_ocorrencia.id_status', ondelete='RESTRICT'), nullable=False)
    id_usuario_responsavel: Mapped[int] = mapped_column(ForeignKey('usuario.id_usuario', ondelete='RESTRICT'), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text)
    alterado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
