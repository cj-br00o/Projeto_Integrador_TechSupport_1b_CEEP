from pathlib import Path
import json
import pandas as pd
import pytest
from backend import analise


def test_totais_conferidos_e_reconciliacao(client):
    r = client.get('/analises/resumo')
    assert r.status_code == 200
    s = r.json()
    assert s['linhas_csv'] == s['total_ocorrencias'] == 20
    assert s['tempo_analise_soma_min'] == 20
    assert s['tempo_analise_media_min'] == s['tempo_analise_mediana_min'] == 1
    assert s['ocorrencias_urgentes'] == 5 and s['percentual_urgentes'] == 25
    assert s['possiveis_duplicidades'] == 1
    c = client.get('/analises/categorias').json()
    d = client.get('/analises/datas').json()
    assert sum(x['total_ocorrencias'] for x in c) == sum(x['total_ocorrencias'] for x in d) == 20
    assert sum(x['urgentes'] for x in c) == sum(x['urgentes'] for x in d) == 5
    assert c[0]['categoria_codigo'] == 'INFRAESTRUTURA' and c[0]['total_ocorrencias'] == 4
    json.dumps(s,allow_nan=False)


@pytest.mark.parametrize('coluna,valor',[('prioridade','URGENTE'),('latitude',200),('longitude',-200),
                                      ('criado_em','data inválida'),('id_ocorrencia',1.5),
                                      ('valido','talvez'),('id_ocorrencia_duplicada',9999),
                                      ('analisado_em','2026-08-01T00:00:00-03:00'),
                                      ('id_categoria_sugerida',999),('descricao','')])
def test_rejeita_fonte_inconsistente(tmp_path,coluna,valor):
    df = pd.read_csv(analise.CSV_PADRAO,dtype='string')
    df.loc[0,coluna] = str(valor)
    p = tmp_path/'invalido.csv';df.to_csv(p,index=False)
    with pytest.raises(ValueError):
        analise.ler_dados(p)


def test_rejeita_id_repetido(tmp_path):
    df = pd.read_csv(analise.CSV_PADRAO)
    df.loc[1,'id_ocorrencia'] = 1
    p = tmp_path/'repetido.csv';df.to_csv(p,index=False)
    with pytest.raises(ValueError):
        analise.ler_dados(p)


def test_categoria_ausente_nao_some_do_total(tmp_path):
    df = pd.read_csv(analise.CSV_PADRAO,dtype='string');df.loc[0,'categoria_codigo'] = pd.NA
    p = tmp_path/'sem_categoria.csv';df.to_csv(p,index=False)
    dados = analise.ler_dados(p)
    grupos = analise.por_categoria(dados)
    assert sum(x['total_ocorrencias'] for x in grupos) == 20
    assert any(x['categoria_codigo']=='SEM_CATEGORIA' for x in grupos)


def test_sem_analise_media_sem_nan(tmp_path):
    df = pd.read_csv(analise.CSV_PADRAO,dtype='string')
    for c in ['resumo','valido','id_categoria_sugerida','prioridade_sugerida','id_ocorrencia_duplicada','analisado_em']:
        df[c] = pd.NA
    p = tmp_path/'sem_analise.csv';df.to_csv(p,index=False)
    r = analise.resumo(analise.ler_dados(p))
    assert r['tempo_analise_media_min'] is None and r['sem_analise'] == 20
    json.dumps(r,allow_nan=False)


def test_csv_inacessivel_resposta_503(client,monkeypatch,tmp_path):
    monkeypatch.setattr(analise,'CSV_PADRAO',tmp_path/'nao_existe.csv')
    assert client.get('/analises/resumo').status_code == 503


def test_csv_malformado_resposta_422(client,monkeypatch,tmp_path):
    p=tmp_path/'ruim.csv';p.write_text('x,y\n1,2\n')
    monkeypatch.setattr(analise,'CSV_PADRAO',p)
    assert client.get('/analises/categorias').status_code == 422


def test_fuso_dia_local(tmp_path):
    df=pd.read_csv(analise.CSV_PADRAO,dtype='string')
    df.loc[0,'criado_em']='2026-09-02T01:00:00Z'
    df.loc[0,'analisado_em']='2026-09-02T01:01:00Z'
    p=tmp_path/'fuso.csv';df.to_csv(p,index=False)
    assert analise.ler_dados(p).loc[0,'dia_local']=='2026-09-01'
