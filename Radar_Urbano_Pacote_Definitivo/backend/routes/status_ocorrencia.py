from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import StatusOcorrencia
from ..schemas import StatusCreate, StatusResponse
from ._utils import persistir

router = APIRouter(prefix="/status-ocorrencia", tags=["Status da ocorrência"])


@router.get("", response_model=list[StatusResponse])
def listar_status(db: Session = Depends(get_db)):
    return db.scalars(select(StatusOcorrencia).order_by(StatusOcorrencia.ordem)).all()


@router.post("", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def criar_status(dados: StatusCreate, db: Session = Depends(get_db)):
    return persistir(
        db,
        StatusOcorrencia(**dados.model_dump()),
        "Já existe um status com esse código, nome ou ordem.",
    )

