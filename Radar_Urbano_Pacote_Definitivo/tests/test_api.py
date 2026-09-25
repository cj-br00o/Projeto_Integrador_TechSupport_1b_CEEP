def test_saude(client):
    resposta = client.get("/saude")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_get_e_post_categoria(client):
    dados = {"codigo": "ACESSIBILIDADE", "nome": "Acessibilidade", "descricao": "Barreiras em espaços públicos", "ativo": True}
    criada = client.post("/categorias", json=dados)
    assert criada.status_code == 201
    assert criada.json()["id_categoria"] == 1
    assert client.get("/categorias").json() == [criada.json()]


def test_rejeita_categoria_duplicada(client):
    dados = {"codigo": "TESTE", "nome": "Teste", "ativo": True}
    assert client.post("/categorias", json=dados).status_code == 201
    assert client.post("/categorias", json=dados).status_code == 409


def test_get_e_post_status(client):
    dados = {"codigo": "AGUARDANDO", "nome": "Aguardando", "ordem": 1, "status_final": False}
    criada = client.post("/status-ocorrencia", json=dados)
    assert criada.status_code == 201
    assert client.get("/status-ocorrencia").json() == [criada.json()]


def test_get_e_post_equipe(client):
    dados = {"nome": "Equipe de Teste", "especialidade": "Manutenção urbana", "ativa": True}
    criada = client.post("/equipes", json=dados)
    assert criada.status_code == 201
    assert criada.json()["criado_em"]
    assert client.get("/equipes").json() == [criada.json()]


def test_validacao_de_schema(client):
    resposta = client.post("/categorias", json={"codigo": "código inválido", "nome": "X"})
    assert resposta.status_code == 422


def test_resumo_analitico(client):
    resposta = client.get("/analises/resumo")
    assert resposta.status_code == 200
    assert resposta.json()["registros"] == 20
    assert resposta.json()["ocorrencias_urgentes"] == 5

