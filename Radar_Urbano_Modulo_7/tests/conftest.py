from pathlib import Path
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(RAIZ))
from backend.database import Base, get_db, criar_engine
from backend.main import app
from backend.models import Usuario, Categoria, StatusOcorrencia


@pytest.fixture
def ambiente(tmp_path):
    engine = criar_engine('sqlite:///' + str(tmp_path/'teste.db'))
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine,expire_on_commit=False)
    with factory() as db:
        db.add_all([Usuario(nome='Cidadão teste',email='teste@example.invalid',perfil='CIDADAO'),
                    Categoria(codigo='INFRAESTRUTURA',nome='Infraestrutura'),
                    StatusOcorrencia(codigo='RECEBIDA',nome='Recebida',ordem=1)])
        db.commit()
    def sessao():
        with factory() as db:
            yield db
    app.dependency_overrides[get_db] = sessao
    with TestClient(app) as client:
        yield client,factory
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture
def client(ambiente):
    return ambiente[0]


@pytest.fixture
def entrada():
    return {'id_usuario':1,'id_categoria':1,'descricao':'Buraco na rua de demonstração.',
            'latitude':-23.42,'longitude':-51.93,'prioridade':'ALTA'}
