# Radar Urbano — Serviços Urbanos e Manutenção

Projeto de análise de ocorrências urbanas com Python e CSV.

## Estrutura
- `database/dados.csv`: base com 1000 ocorrências simuladas.
- `backend/analise.py`: funções de leitura e análise.
- `backend/main.py`: execução das análises e geração de gráficos.
- `documentacao/`: gráficos e arquivo de saída.

## Instalação e execução (Linux)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python backend/main.py
```

A base CSV é tratada como dado de teste. Confirme a origem e a qualidade
dos registros antes de usar resultados como informação real da cidade.
