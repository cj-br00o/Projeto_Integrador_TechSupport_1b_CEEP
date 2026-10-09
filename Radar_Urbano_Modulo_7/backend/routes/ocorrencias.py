from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..database import get_db
from ..models import Categoria, Usuario, Ocorrencia, StatusOcorrencia, HistoricoStatus
from ..schemas import UsuarioCreate, UsuarioResponse, OcorrenciaCreate, OcorrenciaResponse
from ._utils import persistir, erro_integridade

router = APIRouter(tags=['Gestão de ocorrências'])


@router.post('/usuarios', response_model=UsuarioResponse, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return persistir(db, Usuario(nome=dados.nome, email=dados.email.lower(), perfil='CIDADAO'),
                     'Já existe um usuário com esse e-mail.')


def representar(o):
    return {campo: getattr(o,campo) for campo in Ocorrencia.__table__.columns.keys()} | {
        'categoria_nome': o.categoria.nome if o.categoria else None,
        'status_nome': o.status.nome,
    }


@router.post('/ocorrencias', response_model=OcorrenciaResponse, status_code=201)
def criar_ocorrencia(dados: OcorrenciaCreate, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, dados.id_usuario)
    if usuario is None:
        raise HTTPException(404, 'Usuário não encontrado.')
    if not usuario.ativo:
        raise HTTPException(400, 'Usuário inativo.')
    categoria = db.get(Categoria, dados.id_categoria) if dados.id_categoria else None
    if dados.id_categoria and categoria is None:
        raise HTTPException(404, 'Categoria não encontrada.')
    if categoria is not None and not categoria.ativo:
        raise HTTPException(400, 'Categoria inativa.')
    recebido = db.scalar(select(StatusOcorrencia).where(StatusOcorrencia.codigo == 'RECEBIDA'))
    if recebido is None:
        raise HTTPException(409, 'Configure o status RECEBIDA antes de cadastrar ocorrências.')
    o = Ocorrencia(**dados.model_dump(), id_status=recebido.id_status,
                   protocolo='RU-' + uuid4().hex[:17].upper())
    try:
        db.add(o)
        db.flush()
        db.add(HistoricoStatus(id_ocorrencia=o.id_ocorrencia, id_status=o.id_status,
                              id_usuario_responsavel=o.id_usuario, observacao='Registro inicial da ocorrência.'))
        db.commit()
        db.refresh(o)
    except IntegrityError as erro:
        raise erro_integridade(db, erro, 'Conflito no protocolo. Tente novamente.') from erro
    return representar(o)


@router.get('/ocorrencias', response_model=list[OcorrenciaResponse])
def listar_ocorrencias(db: Session = Depends(get_db), limite: int = Query(100, ge=1, le=500),
                      deslocamento: int = Query(0, ge=0)):
    consulta = select(Ocorrencia).options(joinedload(Ocorrencia.categoria), joinedload(Ocorrencia.status))
    registros = db.scalars(consulta.order_by(Ocorrencia.id_ocorrencia).offset(deslocamento).limit(limite)).all()
    return [representar(o) for o in registros]


@router.get('/ocorrencias/{id_ocorrencia}', response_model=OcorrenciaResponse)
def consultar_ocorrencia(id_ocorrencia: int, db: Session = Depends(get_db)):
    o = db.get(Ocorrencia, id_ocorrencia)
    if o is None:
        raise HTTPException(404, 'Ocorrência não encontrada.')
    return representar(o)
