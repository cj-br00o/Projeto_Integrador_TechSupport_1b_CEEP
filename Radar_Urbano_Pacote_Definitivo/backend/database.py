"""Conexão com o PostgreSQL/Supabase por SQLAlchemy."""

from __future__ import annotations

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()


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
    return create_engine(url or _database_url(), pool_pre_ping=True)


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
        configurar_banco()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

