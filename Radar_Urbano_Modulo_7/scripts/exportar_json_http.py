"""Salva respostas da instância HTTP realmente iniciada pelo estudante."""
import argparse,json
from pathlib import Path
from urllib.request import urlopen

p=argparse.ArgumentParser()
p.add_argument('--url',default='http://127.0.0.1:8000')
args=p.parse_args()
saida=Path(__file__).resolve().parents[1]/'evidencias/http'
saida.mkdir(parents=True,exist_ok=True)
for rota,nome in [('/saude/banco','banco'),('/categorias','categorias_ds'),('/ocorrencias','ocorrencias_ds'),
                  ('/analises/resumo','resumo'),('/analises/categorias','categorias_ia'),('/analises/datas','datas')]:
    with urlopen(args.url.rstrip('/')+rota,timeout=20) as r:
        dados=json.load(r)
    (saida/(nome+'.json')).write_text(json.dumps(dados,ensure_ascii=False,indent=2,allow_nan=False))
    print(rota,'200',nome+'.json')
