from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def persistir(db: Session, objeto, mensagem_duplicidade: str):
    """Persiste um registro e converte violação de unicidade em HTTP 409."""
    try:
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto
    except IntegrityError as erro:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=mensagem_duplicidade,
        ) from erro

