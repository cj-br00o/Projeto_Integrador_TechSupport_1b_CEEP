"""Análise reproduzível de uma linha por ocorrência, sem conexão ao banco."""
from pathlib import Path
import json
import pandas as pd

CSV_PADRAO = Path(__file__).resolve().parents[1] / 'database' / 'dados.csv'
COLUNAS = ['id_ocorrencia','protocolo','descricao','latitude','longitude','prioridade','criado_em',
           'categoria_codigo','status_codigo','foto_url','resumo','valido','id_categoria_sugerida',
           'prioridade_sugerida','id_ocorrencia_duplicada','analisado_em']
CATEGORIAS = {1: ('INFRAESTRUTURA','Infraestrutura'), 2: ('ILUMINACAO','Iluminação'),
              3: ('TRANSITO','Trânsito'), 4: ('ARBORIZACAO','Arborização'), 5: ('DRENAGEM','Drenagem'),
              6: ('CONSERVACAO','Conservação'), 7: ('LIMPEZA_URBANA','Limpeza urbana'), 8: ('SANEAMENTO','Saneamento')}
NOMES = dict(CATEGORIAS.values())
STATUS = {'RECEBIDA','EM_ANALISE','ENCAMINHADA','EM_ATENDIMENTO','RESOLVIDA'}
PRIORIDADES = {'BAIXA','MEDIA','ALTA','CRITICA'}


def exigir(condicao, mensagem):
    if not condicao:
        raise ValueError(mensagem)


def ler_dados(caminho=None):
    df = pd.read_csv(caminho or CSV_PADRAO, dtype='string')
    exigir(set(COLUNAS).issubset(df.columns), 'Confira as 16 colunas do CSV.')
    df = df[COLUNAS].copy()
    exigir(not df.empty, 'O CSV está vazio.')
    for c in COLUNAS:
        df[c] = df[c].str.strip().replace('', pd.NA)
    ausentes = {c: int(df[c].isna().sum()) for c in COLUNAS}
    exigir(not df.duplicated().any(), 'Há linhas idênticas no CSV.')
    obrigatorias = ['id_ocorrencia','protocolo','descricao','latitude','longitude','prioridade','criado_em','status_codigo']
    exigir(not df[obrigatorias].isna().any().any(), 'Há valores ausentes em campos obrigatórios.')
    exigir(df['protocolo'].is_unique, 'Há protocolos repetidos.')
    exigir(df['descricao'].str.len().between(10,2000).all(), 'Descrição fora de 10 a 2000 caracteres.')
    exigir(df['protocolo'].str.len().between(1,20).all(), 'Protocolo fora de 1 a 20 caracteres.')
    for c in ['id_ocorrencia','latitude','longitude','id_categoria_sugerida','id_ocorrencia_duplicada']:
        df[c] = pd.to_numeric(df[c], errors='raise')
        exigir(not df[c].isin([float('inf'),-float('inf')]).any(), 'Número infinito no CSV.')
    for c in ['id_ocorrencia','id_categoria_sugerida','id_ocorrencia_duplicada']:
        numeros = df[c].dropna()
        exigir(((numeros > 0) & (numeros % 1 == 0) & (numeros <= 9223372036854775807)).all(), 'IDs devem ser inteiros positivos.')
        df[c] = df[c].astype('Int64')
    exigir(df['id_ocorrencia'].is_unique, 'Cada ocorrência deve aparecer uma única vez no CSV.')
    exigir(df['latitude'].between(-90,90).all(), 'Latitude inválida.')
    exigir(df['longitude'].between(-180,180).all(), 'Longitude inválida.')
    exigir(df['prioridade'].isin(PRIORIDADES).all(), 'Prioridade inválida.')
    exigir(df['status_codigo'].isin(STATUS).all(), 'Status inválido.')
    exigir(df['categoria_codigo'].dropna().isin(NOMES).all(), 'Categoria desconhecida na fonte de referência.')
    exigir(df['prioridade_sugerida'].dropna().isin(PRIORIDADES).all(), 'Prioridade sugerida inválida.')
    exigir(df['id_categoria_sugerida'].dropna().isin(CATEGORIAS).all(), 'Categoria sugerida desconhecida.')
    df['valido'] = df['valido'].str.lower()
    exigir(df['valido'].dropna().isin(['true','false']).all(), 'valido deve ser true ou false.')
    for c in ['criado_em','analisado_em']:
        textos = df[c].dropna()
        exigir(textos.str.contains(r'(?:Z|[+-]\d{2}:\d{2})$',regex=True).all(), 'Data deve informar o fuso horário.')
        df[c] = pd.to_datetime(df[c], utc=True, errors='raise', format='ISO8601')
    analisadas = df['analisado_em'].notna()
    exigir(not df.loc[analisadas,['resumo','valido']].isna().any().any(), 'Análise registrada precisa de resumo e valido.')
    campos_analise = ['resumo','valido','id_categoria_sugerida','prioridade_sugerida','id_ocorrencia_duplicada']
    exigir(not df.loc[~analisadas,campos_analise].notna().any().any(), 'Campos de análise sem analisado_em.')
    exigir((df.loc[analisadas,'analisado_em'] >= df.loc[analisadas,'criado_em']).all(), 'Análise anterior à criação.')
    duplicadas = df['id_ocorrencia_duplicada'].dropna()
    exigir(duplicadas.isin(df['id_ocorrencia']).all(), 'Duplicidade referencia ocorrência ausente na fonte.')
    exigir(not (df['id_ocorrencia_duplicada'] == df['id_ocorrencia']).fillna(False).any(), 'Duplicidade não pode referenciar a própria ocorrência.')
    df['tempo_analise_min'] = (df['analisado_em']-df['criado_em']).dt.total_seconds()/60
    df['grupo_atencao'] = df['prioridade'].map(lambda p: 'URGENTE' if p in {'ALTA','CRITICA'} else 'ROTINA')
    df['dia_local'] = df['criado_em'].dt.tz_convert('America/Sao_Paulo').dt.strftime('%Y-%m-%d')
    df.attrs['ausentes'] = ausentes
    return df


def resumo(df):
    tempos = df['tempo_analise_min'].dropna()
    return {
        'linhas_csv': int(len(df)), 'total_ocorrencias': int(df['id_ocorrencia'].nunique()),
        'total_analisadas': int(len(tempos)), 'sem_analise': int(df['analisado_em'].isna().sum()),
        'tempo_analise_soma_min': round(float(tempos.sum()),2),
        'tempo_analise_media_min': round(float(tempos.mean()),2) if len(tempos) else None,
        'tempo_analise_mediana_min': round(float(tempos.median()),2) if len(tempos) else None,
        'ocorrencias_urgentes': int((df['grupo_atencao']=='URGENTE').sum()),
        'percentual_urgentes': round(float((df['grupo_atencao']=='URGENTE').mean()*100),2),
        'possiveis_duplicidades': int(df['id_ocorrencia_duplicada'].notna().sum()),
        'relatos_validos': int((df['valido']=='true').sum()),
        'relatos_invalidos': int((df['valido']=='false').sum()),
        'data_inicial': min(df['dia_local']), 'data_final': max(df['dia_local']),
        'fuso_agregacao': 'America/Sao_Paulo', 'fonte': 'massa sintética acadêmica',
    }


def por_categoria(df):
    fonte = df.assign(categoria_codigo=df['categoria_codigo'].fillna('SEM_CATEGORIA'))
    resultado = []
    for codigo,g in fonte.groupby('categoria_codigo',sort=True):
        tempos = g['tempo_analise_min'].dropna()
        resultado.append({'categoria_codigo': str(codigo), 'categoria_nome': NOMES.get(codigo,'Sem categoria'),
                          'total_ocorrencias': int(g['id_ocorrencia'].nunique()),
                          'urgentes': int((g['grupo_atencao']=='URGENTE').sum()),
                          'tempo_analise_media_min': round(float(tempos.mean()),2) if len(tempos) else None})
    return sorted(resultado, key=lambda x: (-x['total_ocorrencias'],x['categoria_codigo']))


def por_data(df):
    return [{'data': str(dia), 'total_ocorrencias': int(g['id_ocorrencia'].nunique()),
             'urgentes': int((g['grupo_atencao']=='URGENTE').sum())}
            for dia,g in df.groupby('dia_local',sort=True)]


def qualidade(df):
    return {'resultado': 'aprovado', 'linhas': int(len(df)), 'ausentes_por_coluna': df.attrs['ausentes'],
            'linhas_identicas': 0, 'ids_repetidos': 0,
            'unidade_da_linha': 'uma ocorrência com primeira foto e última análise registradas',
            'regras': 'Não são removidas linhas silenciosamente; inconsistências interrompem a análise.',
            'temporalidade': 'criado_em define a série diária; analisado_em define o intervalo de análise.'}


if __name__ == '__main__':
    dados = ler_dados()
    print(json.dumps({'resumo':resumo(dados),'categorias':por_categoria(dados),'datas':por_data(dados),
                      'qualidade':qualidade(dados)},ensure_ascii=False,indent=2,allow_nan=False))
