"""Funções reutilizáveis para transformar o CSV em informação."""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CSV_PADRAO = RAIZ / "database" / "dados.csv"


def carregar_dados(caminho: Path = CSV_PADRAO) -> pd.DataFrame:
    if not caminho.exists():
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")
    return pd.read_csv(caminho)


def preparar_dados(dados: pd.DataFrame) -> pd.DataFrame:
    preparado = dados.copy()
    preparado["criado_em"] = pd.to_datetime(preparado["criado_em"], utc=True)
    preparado["analisado_em"] = pd.to_datetime(preparado["analisado_em"], utc=True)
    preparado["tempo_analise_min"] = (
        preparado["analisado_em"] - preparado["criado_em"]
    ).dt.total_seconds() / 60
    preparado["grupo_atencao"] = preparado["prioridade"].map(
        lambda valor: "URGENTE" if valor in {"ALTA", "CRITICA"} else "ROTINA"
    )
    preparado["possivel_duplicata"] = preparado["id_ocorrencia_duplicada"].notna()
    return preparado


def calcular_estatisticas(dados: pd.DataFrame, coluna: str) -> dict[str, float]:
    serie = pd.to_numeric(dados[coluna], errors="raise")
    return {
        "media": float(serie.mean()),
        "mediana": float(serie.median()),
        "moda": float(serie.mode().iloc[0]),
        "minimo": float(serie.min()),
        "maximo": float(serie.max()),
        "amplitude": float(serie.max() - serie.min()),
        "variancia": float(serie.var()),
        "desvio_padrao": float(serie.std()),
    }


def agregar_dados(dados: pd.DataFrame, coluna_grupo: str, coluna_valor: str, operacao: str = "contagem") -> pd.Series:
    grupo = dados.groupby(coluna_grupo)[coluna_valor]
    operacoes = {"soma": grupo.sum, "contagem": grupo.count, "media": grupo.mean}
    if operacao not in operacoes:
        raise ValueError("Operação deve ser: soma, contagem ou media")
    return operacoes[operacao]().sort_values(ascending=False)


def obter_resumo(caminho: Path = CSV_PADRAO) -> dict:
    dados = preparar_dados(carregar_dados(caminho))
    estatisticas = calcular_estatisticas(dados, "tempo_analise_min")
    categorias = agregar_dados(dados, "categoria_codigo", "id_ocorrencia", "contagem")
    return {
        "registros": int(len(dados)),
        "tempo_analise_media_min": round(estatisticas["media"], 2),
        "tempo_analise_mediana_min": round(estatisticas["mediana"], 2),
        "ocorrencias_urgentes": int((dados["grupo_atencao"] == "URGENTE").sum()),
        "categoria_mais_frequente": str(categorias.index[0]),
        "possiveis_duplicidades": int(dados["possivel_duplicata"].sum()),
    }

