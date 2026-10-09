from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Equipe
from ..schemas import EquipeCreate, EquipeResponse
from ._utils import persistir

router = APIRouter(prefix="/equipes", tags=["Equipes"])


@router.get("", response_model=list[EquipeResponse])
def listar_equipes(db: Session = Depends(get_db)):
    return db.scalars(select(Equipe).order_by(Equipe.nome)).all()


@router.post("", response_model=EquipeResponse, status_code=status.HTTP_201_CREATED)
def criar_equipe(dados: EquipeCreate, db: Session = Depends(get_db)):
    return persistir(
        db,
        Equipe(**dados.model_dump()),
        "Já existe uma equipe com esse nome.",
    )

