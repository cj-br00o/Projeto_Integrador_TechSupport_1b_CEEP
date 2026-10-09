"""Conexão com o PostgreSQL/Supabase por SQLAlchemy."""

from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from fastapi import HTTPException

load_dotenv(Path(__file__).resolve().parents[1] / '.env')


class Base(DeclarativeBase):
    """Classe-base dos modelos ORM."""


def _database_url() -> str:
    url = os.getenv("DATABASE_URL", "").strip()
    if not url:
        raise RuntimeError(
            "DATABASE_URL não foi definida. Copie .env.example para .env e "
            "informe a conexão do projeto Supabase."
        )
    return url


def criar_engine(url: str | None = None):
    """Cria a engine; testes podem informar uma URL isolada."""
    endereco = url or _database_url()
    for prefixo in ('postgresql://', 'postgres://'):
        if endereco.startswith(prefixo):
            endereco = 'postgresql+psycopg://' + endereco[len(prefixo):]
    nova_engine = create_engine(endereco, pool_pre_ping=True)
    if nova_engine.dialect.name == 'sqlite':
        @event.listens_for(nova_engine, 'connect')
        def ativar_fk(conexao, _):
            conexao.execute('PRAGMA foreign_keys=ON')
    return nova_engine


engine = None
SessionLocal = None


def configurar_banco(url: str | None = None) -> None:
    """Inicializa engine e fábrica de sessões sem recriar as tabelas."""
    global engine, SessionLocal
    engine = criar_engine(url)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Fornece uma sessão por requisição e sempre a fecha."""
    global SessionLocal
    if SessionLocal is None:
        try:
            configurar_banco()
        except RuntimeError as erro:
            raise HTTPException(503, 'Banco não configurado. Defina DATABASE_URL localmente.') from erro
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

