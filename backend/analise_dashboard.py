"""Agregações para os gráficos do dashboard do Radar Urbano."""
from .analise import ler_dados


def ocorrencias_por_mes() -> list[dict]:
    dados = ler_dados()
    grupos = dados.assign(mes=dados["data_registro"].dt.to_period("M").astype(str))
    totais = grupos.groupby("mes")["id_ocorrencia"].nunique().sort_index()
    return [{"mes": mes, "total_ocorrencias": int(total)} for mes, total in totais.items()]


def por_gravidade() -> list[dict]:
    dados = ler_dados()
    totais = dados.groupby("gravidade")["id_ocorrencia"].nunique().sort_values(ascending=False)
    return [{"gravidade": nome, "total_ocorrencias": int(total)} for nome, total in totais.items()]


def por_status() -> list[dict]:
    dados = ler_dados()
    totais = dados.groupby("status")["id_ocorrencia"].nunique().sort_values(ascending=False)
    return [{"status": nome, "total_ocorrencias": int(total)} for nome, total in totais.items()]
