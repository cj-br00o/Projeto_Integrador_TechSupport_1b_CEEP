from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def erro_integridade(db, erro, mensagem):
    db.rollback()
    codigo = getattr(erro.orig, 'sqlstate', None)
    unica = codigo == '23505' or 'UNIQUE constraint failed' in str(erro.orig)
    return HTTPException(status_code=409 if unica else 422,
                         detail=mensagem if unica else 'Os dados violam uma regra de integridade do banco.')


def persistir(db, objeto, mensagem_duplicidade):
    try:
        db.add(objeto)
        db.commit()
        db.refresh(objeto)
        return objeto
    except IntegrityError as erro:
        raise erro_integridade(db, erro, mensagem_duplicidade) from erro
