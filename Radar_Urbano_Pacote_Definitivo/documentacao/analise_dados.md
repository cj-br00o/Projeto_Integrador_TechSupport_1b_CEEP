# Análise de dados do Radar Urbano — Módulo 6

## Fonte

O arquivo `database/dados.csv` contém 20 ocorrências fictícias exportadas no mesmo formato da view `vw_ocorrencia_exportacao_ia`. Uma linha representa uma ocorrência com sua categoria, prioridade, status e resultado mais recente da análise de IA. O recorte cobre somente a manhã de 1º de setembro de 2026 e não representa dados reais da Prefeitura de Maringá.

## Estatística

**Coluna analisada:** `tempo_analise_min`, calculada pela diferença entre `analisado_em` e `criado_em`.

**Pergunta:** quanto tempo a massa de teste leva entre o registro e a análise inicial?

**Resultados:** média, mediana, moda, mínimo e máximo são 1 minuto; amplitude, variância e desvio padrão são 0.

**Interpretação:** a massa foi construída com intervalo constante de um minuto. O resultado comprova o cálculo, mas não mede o desempenho real do serviço e não deve ser usado como promessa operacional.

## Agregação

**Pergunta:** quantas ocorrências há em cada categoria?

**Técnica:** `groupby("categoria_codigo")["id_ocorrencia"].count()`.

**Resultado principal:** `INFRAESTRUTURA` aparece 4 vezes e é a categoria mais frequente nesta massa. O gráfico `evidencias/ia/ocorrencias_por_categoria.png` comunica a distribuição completa.

**Interpretação:** a massa testa diferentes áreas urbanas. Com apenas 20 registros fictícios de uma manhã, a diferença não permite concluir que infraestrutura seja o maior problema real da cidade.

## Classificação por regras

**Regra:** prioridades `ALTA` e `CRITICA` recebem a classe `URGENTE`; `BAIXA` e `MEDIA` recebem `ROTINA`.

**Justificativa:** a classificação reutiliza o domínio oficial de prioridade do banco e cria um agrupamento transparente para apoiar a triagem. Há 5 ocorrências urgentes (IDs 3, 7, 11, 14 e 18). A decisão final continua humana.

## Duplicidade

Uma ocorrência possui `id_ocorrencia_duplicada`: o registro 20 referencia o registro 5. Esse campo sinaliza possível duplicidade; não autoriza exclusão automática.

## Reprodução

```bash
python -m pip install -r requirements.txt
python -m backend.executar_analise
```

O comando recria `evidencias/ia/resultados_analise.json` e `evidencias/ia/ocorrencias_por_categoria.png`.

