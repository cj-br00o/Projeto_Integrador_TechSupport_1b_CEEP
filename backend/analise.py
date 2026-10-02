from pathlib import Path
import pandas as pd


def caminho_projeto():
    return Path(__file__).resolve().parent.parent


def carregar_dados():
    """Carrega os registros do CSV do Radar Urbano."""
    arquivo = caminho_projeto() / "database" / "dados.csv"
    if not arquivo.exists():
        raise FileNotFoundError(f"CSV não encontrado: {arquivo}")

    dados = pd.read_csv(arquivo)
    dados.columns = dados.columns.str.strip()

    if dados.empty:
        raise ValueError("O CSV está vazio.")

    return dados


def verificar_colunas(dados, colunas):
    ausentes = [c for c in colunas if c not in dados.columns]
    if ausentes:
        raise ValueError(
            f"Colunas ausentes: {ausentes}. "
            f"Colunas disponíveis: {list(dados.columns)}"
        )


def resumo_geral(dados):
    print("\n=== RADAR URBANO: RESUMO GERAL ===")
    print(f"Total de ocorrências: {len(dados)}")
    print(f"Total de colunas: {len(dados.columns)}")
    print("\nPrimeiras ocorrências:")
    print(dados.head())
    print("\nValores ausentes por coluna:")
    print(dados.isna().sum())


def contar_por_coluna(dados, coluna):
    verificar_colunas(dados, [coluna])
    resultado = dados[coluna].fillna("Não informado").value_counts()
    print(f"\n=== CONTAGEM POR {coluna.upper()} ===")
    print(resultado.to_string())
    return resultado


def estatisticas_tempo_resolucao(dados):
    verificar_colunas(dados, ["tempo_resolucao_dias"])
    valores = pd.to_numeric(dados["tempo_resolucao_dias"], errors="coerce").dropna()

    if valores.empty:
        print("\nNão há tempos de resolução numéricos para analisar.")
        return None

    resultado = {
        "média": valores.mean(),
        "mediana": valores.median(),
        "mínimo": valores.min(),
        "máximo": valores.max(),
        "desvio padrão": valores.std(),
    }

    print("\n=== TEMPO DE RESOLUÇÃO (DIAS) ===")
    for nome, valor in resultado.items():
        print(f"{nome}: {valor:.2f}")
    return resultado


def tempo_medio_por_tipo(dados):
    verificar_colunas(dados, ["tipo_problema", "tempo_resolucao_dias"])
    copia = dados.copy()
    copia["tempo_resolucao_dias"] = pd.to_numeric(
        copia["tempo_resolucao_dias"], errors="coerce"
    )
    resultado = (
        copia.groupby("tipo_problema")["tempo_resolucao_dias"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
    )
    print("\n=== TEMPO MÉDIO DE RESOLUÇÃO POR TIPO DE PROBLEMA ===")
    print(resultado.round(2).to_string())
    return resultado


def ocorrencias_por_bairro_e_tipo(dados):
    verificar_colunas(dados, ["bairro", "tipo_problema"])
    tabela = pd.crosstab(dados["bairro"], dados["tipo_problema"])
    print("\n=== OCORRÊNCIAS POR BAIRRO E TIPO ===")
    print(tabela.to_string())
    return tabela


def salvar_grafico(resultado, titulo, nome_arquivo, rotulo_x, rotulo_y="Quantidade"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    if resultado is None or resultado.empty:
        print(f"Sem dados para gerar o gráfico: {titulo}")
        return

    pasta = caminho_projeto() / "documentacao"
    pasta.mkdir(parents=True, exist_ok=True)

    ax = resultado.plot(kind="bar", figsize=(10, 5))
    ax.set_title(titulo)
    ax.set_xlabel(rotulo_x)
    ax.set_ylabel(rotulo_y)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    destino = pasta / nome_arquivo
    plt.savefig(destino, dpi=150)
    plt.close()
    print(f"Gráfico salvo: {destino}")


def preparar_prioridade(dados):
    """Padroniza a gravidade registrada; não prevê gravidade automaticamente."""
    verificar_colunas(dados, ["gravidade"])
    copia = dados.copy()
    copia["gravidade_classificada"] = (
        copia["gravidade"].astype("string").str.strip().str.capitalize()
        .fillna("Não informada")
    )
    return copia
