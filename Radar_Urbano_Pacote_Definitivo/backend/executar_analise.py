"""Executa a análise do Módulo 6 e grava resultados reproduzíveis."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backend.analise import agregar_dados, calcular_estatisticas, carregar_dados, obter_resumo, preparar_dados


def main() -> None:
    raiz = Path(__file__).resolve().parent.parent
    saida = raiz / "evidencias" / "ia"
    saida.mkdir(parents=True, exist_ok=True)
    dados = preparar_dados(carregar_dados())
    estatisticas = calcular_estatisticas(dados, "tempo_analise_min")
    categorias = agregar_dados(dados, "categoria_codigo", "id_ocorrencia", "contagem")
    prioridades = agregar_dados(dados, "prioridade", "id_ocorrencia", "contagem")
    resultado = {
        "resumo": obter_resumo(),
        "estatisticas_tempo_analise_min": {chave: round(valor, 4) for chave, valor in estatisticas.items()},
        "ocorrencias_por_categoria": {str(chave): int(valor) for chave, valor in categorias.items()},
        "ocorrencias_por_prioridade": {str(chave): int(valor) for chave, valor in prioridades.items()},
    }
    (saida / "resultados_analise.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    fig, ax = plt.subplots(figsize=(10, 5.5))
    categorias.sort_values().plot(kind="barh", color="#58a934", ax=ax)
    ax.set_title("Radar Urbano — ocorrências por categoria")
    ax.set_xlabel("Quantidade de ocorrências")
    ax.set_ylabel("Categoria")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(saida / "ocorrencias_por_categoria.png", dpi=180)
    plt.close(fig)
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

