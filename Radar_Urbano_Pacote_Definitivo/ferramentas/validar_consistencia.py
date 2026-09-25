from pathlib import Path
import csv, hashlib, json, re, sys, zipfile

root = Path(__file__).resolve().parents[1]
model = json.loads((root / 'docs/modelo_canonico.json').read_text(encoding='utf-8'))
schema = (root / 'database/script_ddl.sql').read_text(encoding='utf-8')
dictionary = (root / 'docs/dicionario_dados.md').read_text(encoding='utf-8')
der = (root / 'docs/der/der_radar_urbano.mmd').read_text(encoding='utf-8')
matrix = (root / 'docs/07_matriz_banco_csv.md').read_text(encoding='utf-8')
csv_path = root / 'data/original/radar_urbano_ocorrencias_teste.csv'
csv_database_path = root / 'database/dados.csv'
errors = []

required_paths = [
    root / 'backend/main.py',
    root / 'backend/database.py',
    root / 'backend/models.py',
    root / 'backend/schemas.py',
    root / 'backend/analise.py',
    root / 'backend/executar_analise.py',
    root / 'frontend/gestao.html',
    root / 'frontend/gestao.css',
    root / 'frontend/gestao.js',
    root / 'database/dados.csv',
    root / 'database/script_ddl.sql',
    root / 'database/script_seed.sql',
    root / 'database/script_dql.sql',
    root / 'data/original/radar_urbano_ocorrencias_teste.csv',
    root / 'postman/Radar_Urbano_Modulo_6.postman_collection.json',
    root / 'tests/test_api.py',
    root / 'documentacao/backend_rotas.md',
    root / 'documentacao/analise_dados.md',
    root / 'evidencias/postman/resultado_pytest.txt',
    root / 'evidencias/ia/resultados_analise.json',
    root / 'evidencias/ia/ocorrencias_por_categoria.png',
    root / 'docs/problema.md',
    root / 'docs/regras_negocio.md',
    root / 'docs/dicionario_dados.md',
    root / 'docs/dicionario.xlsx',
    root / 'docs/DER.png',
]
for required_path in required_paths:
    if not required_path.is_file():
        errors.append(f'Arquivo obrigatório ausente: {required_path.relative_to(root)}')

xlsx_path = root / 'docs/dicionario.xlsx'
if xlsx_path.exists() and not zipfile.is_zipfile(xlsx_path):
    errors.append('docs/dicionario.xlsx não é um arquivo XLSX válido')

der_png_path = root / 'docs/DER.png'
if der_png_path.exists() and der_png_path.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n':
    errors.append('docs/DER.png não é um arquivo PNG válido')

if csv_path.exists() and csv_database_path.exists():
    hash_data = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    hash_database = hashlib.sha256(csv_database_path.read_bytes()).hexdigest()
    if hash_data != hash_database:
        errors.append('As cópias do CSV em data/original e database são diferentes')

def table_block(name):
    m = re.search(rf'CREATE TABLE\s+{re.escape(name)}\s*\((.*?)\n\);', schema, re.I | re.S)
    return m.group(1) if m else None

for table in model['tables']:
    block = table_block(table['name'])
    if block is None:
        errors.append(f"Tabela ausente no DDL: {table['name']}")
        continue
    for field in table['fields']:
        if not re.search(rf'^\s*{re.escape(field["name"])}\s+', block, re.M):
            errors.append(f"Campo ausente no DDL: {table['name']}.{field['name']}")
        for label, content in [('dicionário', dictionary), ('DER', der)]:
            if field['name'] not in content:
                errors.append(f"Campo ausente no {label}: {table['name']}.{field['name']}")
    if table['name'] not in dictionary or table['name'].upper() not in der:
        errors.append(f"Tabela não rastreada no dicionário e no DER: {table['name']}")

rows = list(csv.DictReader(csv_path.open(encoding='utf-8')))
expected_columns = [c['name'] for c in model['csv_columns']]
if list(rows[0].keys()) != expected_columns:
    errors.append('Cabeçalho do CSV diverge do modelo canônico')
for column in expected_columns:
    if column not in matrix:
        errors.append(f'Coluna ausente na matriz Banco × CSV: {column}')
view_match = re.search(r'CREATE VIEW\s+vw_ocorrencia_exportacao_ia\s+AS\s+SELECT(.*?)\nFROM\s+ocorrencia', schema, re.I | re.S)
if not view_match:
    errors.append('View de exportação ausente no DDL')
else:
    view_columns = []
    for raw in view_match.group(1).split(',\n'):
        line = raw.strip()
        alias = re.search(r'\s+AS\s+(\w+)\s*$', line, re.I)
        direct = re.search(r'\.(\w+)\s*$', line)
        name = alias.group(1) if alias else (direct.group(1) if direct else None)
        if name:
            view_columns.append(name)
    if view_columns != expected_columns:
        errors.append(f'Colunas da view divergem do CSV: {view_columns}')
if len(rows) != 20:
    errors.append(f'Quantidade de registros diferente de 20: {len(rows)}')
ids = [int(r['id_ocorrencia']) for r in rows]
if len(set(ids)) != len(ids): errors.append('IDs duplicados no CSV')
protocols = [r['protocolo'] for r in rows]
if len(set(protocols)) != len(protocols): errors.append('Protocolos duplicados no CSV')
for r in rows:
    if r['prioridade'] not in model['domains']['prioridade']: errors.append(f"Prioridade inválida no ID {r['id_ocorrencia']}")
    if r['prioridade_sugerida'] not in model['domains']['prioridade']: errors.append(f"Prioridade sugerida inválida no ID {r['id_ocorrencia']}")
    if r['categoria_codigo'] not in model['domains']['categoria_codigo']: errors.append(f"Categoria inválida no ID {r['id_ocorrencia']}")
    if r['status_codigo'] not in model['domains']['status_codigo']: errors.append(f"Status inválido no ID {r['id_ocorrencia']}")
    if not -90 <= float(r['latitude']) <= 90 or not -180 <= float(r['longitude']) <= 180: errors.append(f"Coordenadas inválidas no ID {r['id_ocorrencia']}")
    dup = r['id_ocorrencia_duplicada'].strip()
    if dup and (int(dup) not in ids or int(dup) == int(r['id_ocorrencia'])): errors.append(f"Duplicidade inválida no ID {r['id_ocorrencia']}")

high = [int(r['id_ocorrencia']) for r in rows if r['prioridade'] in ('ALTA','CRITICA')]
if high != [3,7,11,14,18]: errors.append(f'Gabarito alta/crítica divergente: {high}')

seed = (root / 'database/script_seed.sql').read_text(encoding='utf-8')
dql = (root / 'database/script_dql.sql').read_text(encoding='utf-8')
for protocol in protocols:
    if protocol not in seed:
        errors.append(f'Protocolo do CSV ausente no seed: {protocol}')
if "COUNT(*) FILTER (WHERE prioridade IN ('ALTA', 'CRITICA'))" not in dql:
    errors.append('Consulta final de urgências ausente no script_dql.sql')

resultado_path = root / 'outputs/resultados/resumo_resultados.json'
if resultado_path.exists():
    resultado = json.loads(resultado_path.read_text(encoding='utf-8'))
    if resultado['estatisticas']['ids_urgentes'] != [3, 7, 11, 14, 18]:
        errors.append('Resultado Python diverge do gabarito de urgências')
    if resultado['estatisticas']['possiveis_duplicidades'] != 1:
        errors.append('Resultado Python diverge da duplicidade esperada')

resultado_modulo6 = root / 'evidencias/ia/resultados_analise.json'
if resultado_modulo6.exists():
    resultado = json.loads(resultado_modulo6.read_text(encoding='utf-8'))
    resumo = resultado['resumo']
    if resumo['registros'] != 20: errors.append('Resumo do Módulo 6 não possui 20 registros')
    if resumo['ocorrencias_urgentes'] != 5: errors.append('Resumo do Módulo 6 diverge em urgências')
    if resumo['possiveis_duplicidades'] != 1: errors.append('Resumo do Módulo 6 diverge em duplicidades')

backend_text = '\n'.join(
    (root / caminho).read_text(encoding='utf-8')
    for caminho in ['backend/models.py', 'backend/schemas.py', 'backend/main.py']
)
for nome in ['categoria', 'status_ocorrencia', 'equipe']:
    if nome not in backend_text:
        errors.append(f'Tabela elegível ausente no backend: {nome}')

if errors:
    print('VALIDAÇÃO COM ERROS')
    for e in errors: print('- ' + e)
    sys.exit(1)
print('VALIDAÇÃO APROVADA')
print(f'Tabelas verificadas: {len(model["tables"])}')
print(f'Campos verificados: {sum(len(t["fields"]) for t in model["tables"])}')
print('Dicionário e DER: nomes rastreados')
print('Estrutura exigida: backend, IA, frontend, database, documentação e evidências conferidos')
print('View de exportação: cabeçalho idêntico ao CSV')
print('CSV original e cópia em database: conteúdo idêntico')
print('Seed: todos os protocolos do CSV localizados')
print('Resultados Python: gabaritos conferidos')
print('Rotas elegíveis: categoria, status_ocorrencia e equipe')
print(f'Colunas CSV: {len(expected_columns)}')
print(f'Registros CSV: {len(rows)}')
print('IDs ALTA/CRITICA: 3, 7, 11, 14 e 18')
print('Duplicidade de teste: ID 20 referencia ID 5')
