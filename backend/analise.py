"""Leitura, validação e consultas descritivas do Radar Urbano."""
from pathlib import Path
import pandas as pd

CAMINHO_CSV = Path(__file__).resolve().parent.parent / "database" / "radar_urbano_base_completa_1000.csv"
COLUNAS_OBRIGATORIAS = [
    "id_ocorrencia", "tipo_problema", "endereco", "bairro", "latitude", "longitude",
    "data_registro", "hora_registro", "descricao_problema", "caminho_foto", "gravidade",
    "orgao_responsavel", "responsavel_atendimento", "prazo_atendimento_dias", "status",
    "data_inicio_atendimento", "solucao_ocorrencia", "data_resolucao",
    "tempo_resolucao_dias", "observacoes",
]


def ler_dados() -> pd.DataFrame:
    """Carrega o CSV e valida estrutura, identificadores, datas e campos numéricos."""
    if not CAMINHO_CSV.exists():
        raise FileNotFoundError(f"CSV não encontrado: {CAMINHO_CSV}")

    try:
        df = pd.read_csv(CAMINHO_CSV, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(CAMINHO_CSV, encoding="latin-1")

    faltantes = sorted(set(COLUNAS_OBRIGATORIAS) - set(df.columns))
    if faltantes:
        raise ValueError("Colunas ausentes no CSV: " + ", ".join(faltantes))
    df = df[COLUNAS_OBRIGATORIAS].copy()
    if df.empty:
        raise ValueError("O CSV de ocorrências está vazio.")

    if df["id_ocorrencia"].isna().any():
        raise ValueError("Existem identificadores de ocorrência vazios.")
    df["id_ocorrencia"] = pd.to_numeric(df["id_ocorrencia"], errors="raise").astype("int64")
    if df["id_ocorrencia"].duplicated().any():
        raise ValueError("Existem identificadores de ocorrência duplicados.")

    df["data_registro"] = pd.to_datetime(df["data_registro"], format="%Y-%m-%d", errors="raise")
    numericos = ["prazo_atendimento_dias", "tempo_resolucao_dias", "latitude", "longitude"]
    for coluna in numericos:
        df[coluna] = pd.to_numeric(df[coluna], errors="raise")

    for coluna in ["tipo_problema", "bairro", "gravidade", "orgao_responsavel", "status"]:
        if df[coluna].isna().any() or df[coluna].astype(str).str.strip().eq("").any():
            raise ValueError(f"Existem valores vazios na coluna {coluna}.")
    return df


def resumo(df: pd.DataFrame | None = None) -> dict:
    """Indicadores gerais do conjunto de ocorrências."""
    df = ler_dados() if df is None else df
    tempos = df["tempo_resolucao_dias"].dropna()
    return {
        "total_ocorrencias": int(df["id_ocorrencia"].nunique()),
        "bairros_atendidos": int(df["bairro"].nunique()),
        "orgaos_responsaveis": int(df["orgao_responsavel"].nunique()),
        "media_tempo_resolucao_dias": round(float(tempos.mean()), 2) if not tempos.empty else None,
        "mediana_tempo_resolucao_dias": round(float(tempos.median()), 2) if not tempos.empty else None,
        "data_inicial": df["data_registro"].min().strftime("%Y-%m-%d"),
        "data_final": df["data_registro"].max().strftime("%Y-%m-%d"),
        "total_status": int(df["status"].nunique()),
    }


def por_problema(df: pd.DataFrame | None = None) -> list[dict]:
    df = ler_dados() if df is None else df
    tabela = df.groupby("tipo_problema", as_index=False).agg(
        total_ocorrencias=("id_ocorrencia", "nunique"),
        media_tempo_resolucao_dias=("tempo_resolucao_dias", "mean"),
    )
    tabela["media_tempo_resolucao_dias"] = tabela["media_tempo_resolucao_dias"].round(2)
    return tabela.sort_values(["total_ocorrencias", "tipo_problema"], ascending=[False, True]).to_dict("records")


def por_bairro(df: pd.DataFrame | None = None) -> list[dict]:
    df = ler_dados() if df is None else df
    tabela = df.groupby("bairro", as_index=False).agg(
        total_ocorrencias=("id_ocorrencia", "nunique"),
        tempo_medio_resolucao_dias=("tempo_resolucao_dias", "mean"),
    )
    tabela["tempo_medio_resolucao_dias"] = tabela["tempo_medio_resolucao_dias"].round(2)
    return tabela.sort_values(["total_ocorrencias", "bairro"], ascending=[False, True]).to_dict("records")
