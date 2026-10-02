from analise import (
    carregar_dados,
    resumo_geral,
    contar_por_coluna,
    estatisticas_tempo_resolucao,
    tempo_medio_por_tipo,
    ocorrencias_por_bairro_e_tipo,
    salvar_grafico,
    preparar_prioridade,
)


def main():
    dados = carregar_dados()
    resumo_geral(dados)

    por_tipo = contar_por_coluna(dados, "tipo_problema")
    por_bairro = contar_por_coluna(dados, "bairro")
    por_status = contar_por_coluna(dados, "status")
    por_gravidade = contar_por_coluna(dados, "gravidade")
    por_orgao = contar_por_coluna(dados, "orgao_responsavel")

    estatisticas_tempo_resolucao(dados)
    tempo_medio = tempo_medio_por_tipo(dados)
    ocorrencias_por_bairro_e_tipo(dados)

    salvar_grafico(
        por_tipo, "Ocorrências por tipo de problema",
        "ocorrencias_por_tipo.png", "Tipo de problema"
    )
    salvar_grafico(
        por_bairro, "Ocorrências por bairro",
        "ocorrencias_por_bairro.png", "Bairro"
    )
    salvar_grafico(
        por_status, "Ocorrências por status",
        "ocorrencias_por_status.png", "Status"
    )
    salvar_grafico(
        por_gravidade, "Ocorrências por gravidade",
        "ocorrencias_por_gravidade.png", "Gravidade"
    )
    salvar_grafico(
        por_orgao, "Ocorrências por órgão responsável",
        "ocorrencias_por_orgao.png", "Órgão responsável"
    )
    salvar_grafico(
        tempo_medio, "Tempo médio de resolução por tipo de problema",
        "tempo_medio_por_tipo.png", "Tipo de problema", "Dias"
    )

    dados_classificados = preparar_prioridade(dados)
    saida = (
        __import__("pathlib").Path(__file__).resolve().parent.parent
        / "documentacao" / "ocorrencias_com_gravidade_padronizada.csv"
    )
    dados_classificados.to_csv(saida, index=False)
    print(f"\nArquivo de análise salvo em: {saida}")
    print("\nAnálise do Radar Urbano concluída!")


if __name__ == "__main__":
    main()
