import pytest
from sqlalchemy import select,func
from sqlalchemy.exc import IntegrityError
from backend.models import HistoricoStatus, Ocorrencia, Categoria, Usuario, StatusOcorrencia


def test_categoria_pk_e_consulta(client):
    criada = client.post('/categorias',json={'codigo':'ACESSIBILIDADE','nome':'Acessibilidade'})
    assert criada.status_code == 201
    assert criada.json()['id_categoria'] > 0
    assert criada.json() in client.get('/categorias').json()


def test_duplicidade_e_recuperacao_da_sessao(client):
    assert client.post('/categorias',json={'codigo':'INFRAESTRUTURA','nome':'Nova'}).status_code == 409
    assert client.post('/categorias',json={'codigo':'TESTE','nome':'Categoria de teste'}).status_code == 201


def test_ocorrencia_fk_nomes_historico(ambiente,entrada):
    client,factory = ambiente
    resposta = client.post('/ocorrencias',json=entrada)
    assert resposta.status_code == 201
    o = resposta.json()
    assert o['categoria_nome'] == 'Infraestrutura' and o['status_nome'] == 'Recebida'
    assert len(o['protocolo']) == 20
    assert client.get('/ocorrencias').json() == [o]
    assert client.get('/ocorrencias/'+str(o['id_ocorrencia'])).json() == o
    with factory() as db:
        h = db.scalar(select(HistoricoStatus))
        assert h.id_ocorrencia == o['id_ocorrencia'] and h.id_usuario_responsavel == 1


@pytest.mark.parametrize('campo',['id_categoria','id_usuario'])
def test_fk_inexistente_nao_persiste(ambiente,entrada,campo):
    client,factory = ambiente
    entrada[campo] = 30000
    assert client.post('/ocorrencias',json=entrada).status_code == 404
    with factory() as db:
        assert db.scalar(select(func.count()).select_from(Ocorrencia)) == 0
        assert db.scalar(select(func.count()).select_from(HistoricoStatus)) == 0


@pytest.mark.parametrize('classe',[Categoria,Usuario])
def test_referencia_inativa(ambiente,entrada,classe):
    client,factory = ambiente
    with factory() as db:
        db.get(classe,1).ativo = False
        db.commit()
    assert client.post('/ocorrencias',json=entrada).status_code == 400


@pytest.mark.parametrize('mudanca',[{'latitude':91},{'longitude':-181},{'descricao':'curta'},
                                  {'prioridade':'URGENTE'},{'id_categoria':0},{'id_usuario':-1}])
def test_entrada_invalida(client,entrada,mudanca):
    entrada.update(mudanca)
    assert client.post('/ocorrencias',json=entrada).status_code == 422


def test_categoria_opcional_coerente_com_ddl(client,entrada):
    entrada['id_categoria'] = None
    resposta = client.post('/ocorrencias',json=entrada)
    assert resposta.status_code == 201 and resposta.json()['categoria_nome'] is None


def test_sem_status_inicial(client,ambiente,entrada):
    with ambiente[1]() as db:
        db.delete(db.get(StatusOcorrencia,1));db.commit()
    assert client.post('/ocorrencias',json=entrada).status_code == 409


def test_integridade_fk_no_banco(ambiente,entrada):
    with ambiente[1]() as db:
        db.add(Ocorrencia(**(entrada | {'id_categoria':99999}),id_status=1,protocolo='RU-TESTE-FK'))
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()


def test_rotas_existentes_preservadas(client):
    assert client.get('/equipes').status_code == 200
    assert client.get('/status-ocorrencia').status_code == 200
    assert client.get('/saude/banco').json()['banco'] == 'sqlite'
    assert client.get('/ocorrencias/9999').status_code == 404
    assert client.get('/ocorrencias?limite=501').status_code == 422
