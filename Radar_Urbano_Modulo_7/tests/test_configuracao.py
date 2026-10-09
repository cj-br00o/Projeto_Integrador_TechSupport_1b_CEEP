from fastapi.testclient import TestClient
from backend import database
from backend.main import app


def test_gestao_sem_configuracao_e_analise_independente(monkeypatch):
    monkeypatch.setenv('DATABASE_URL','')
    monkeypatch.setattr(database,'SessionLocal',None)
    with TestClient(app) as client:
        assert client.get('/saude/banco').status_code == 503
        assert client.get('/analises/resumo').status_code == 200
