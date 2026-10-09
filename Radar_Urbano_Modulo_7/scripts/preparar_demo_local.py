"""Cria somente banco SQLite local de demonstração; não acessa Supabase."""
from pathlib import Path
from sqlalchemy.orm import Session
from backend.database import Base, criar_engine
from backend.models import Categoria, StatusOcorrencia, Usuario

RAIZ = Path(__file__).resolve().parents[1]
engine = criar_engine('sqlite:///' + str(RAIZ / 'demo_local.db'))
Base.metadata.create_all(engine)
with Session(engine) as db:
    if not db.query(Categoria).count():
        db.add(Categoria(codigo='INFRAESTRUTURA',nome='Infraestrutura',descricao='Problemas em vias públicas'))
    if not db.query(StatusOcorrencia).count():
        db.add(StatusOcorrencia(codigo='RECEBIDA',nome='Recebida',ordem=1))
    if not db.query(Usuario).count():
        db.add(Usuario(nome='Cidadão de teste',email='teste@example.invalid',perfil='CIDADAO'))
    db.commit()
print('Banco SQLite demonstrativo preparado. Defina DATABASE_URL=sqlite:///demo_local.db para a demonstração local.')
