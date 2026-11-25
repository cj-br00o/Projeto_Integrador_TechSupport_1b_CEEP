"""Consultas em linguagem natural sobre o CSV do Radar Urbano."""
from __future__ import annotations
import json
import os
import urllib.request
import urllib.error
import unicodedata
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..analise import ler_dados, resumo, por_problema, por_bairro

router = APIRouter(prefix="/chat", tags=["Radar IA - Chat"])


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
OLLAMA_NUM_GPU = int(os.getenv("OLLAMA_NUM_GPU", "0"))


PROMPT_SISTEMA = """
Você é o Radar IA, um assistente especializado em análise de dados urbanos.
Seu trabalho é explicar resultados produzidos pelo Python/Pandas.

REGRAS:
1. Responda em português brasileiro, de forma objetiva e simples.
2. Utilize exclusivamente os dados fornecidos no JSON.
3. Nunca invente informações, números, bairros ou órgãos.
4. Não faça novos cálculos nem altere os valores recebidos.
5. Se o resultado estiver vazio ou zerado, apenas informe isso sem supor motivos.
6. Explique brevemente o significado dos resultados sem repetir toda a estrutura técnica.
""".strip()

PERGUNTAS_SUGERIDAS = [
    "Quantas ocorrências foram registradas?",
    "Qual bairro tem mais ocorrências?",
    "Qual é o problema urbano mais frequente?",
    "Quais são os órgãos responsáveis?",
    "Qual é o tempo médio de resolução?",
    "Quantas ocorrências estão resolvidas?",
    "Quantas ocorrências estão pendentes?",
    "Como estão distribuídas as ocorrências por gravidade?",
]


class Consulta(BaseModel):
    pergunta: str = Field(min_length=3, max_length=500)


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.casefold())
    return "".join(c for c in texto if not unicodedata.combining(c))


def calcular(pergunta: str) -> dict:
    df = ler_dados()
    q = normalizar(pergunta)

    if any(t in q for t in ("bairro", "regiao", "regioes")):
        dados = por_bairro(df)
        return {
            "titulo": "Ocorrências por bairro",
            "total_bairros": int(df["bairro"].nunique()),
            "bairro_com_mais_ocorrencias": dados[0] if dados else None,
            "ranking": dados[:10],
        }

    if any(t in q for t in ("problema", "tipo", "frequente", "comum", "mais acontece")):
        dados = por_problema(df)
        return {
            "titulo": "Ocorrências por tipo de problema",
            "tipo_mais_frequente": dados[0] if dados else None,
            "ranking": dados[:10],
        }

    if any(t in q for t in ("orgao", "responsavel", "secretaria")):
        dados = df.groupby("orgao_responsavel")["id_ocorrencia"].nunique().sort_values(ascending=False)
        return {
            "titulo": "Ocorrências por órgão responsável",
            "total_orgaos": int(df["orgao_responsavel"].nunique()),
            "ranking": [{"orgao": str(k), "total_ocorrencias": int(v)} for k, v in dados.items()],
        }

    if any(t in q for t in ("gravidade", "grave", "prioridade")):
        dados = df.groupby("gravidade")["id_ocorrencia"].nunique().sort_values(ascending=False)
        return {
            "titulo": "Ocorrências por gravidade",
            "ranking": [{"gravidade": str(k), "total_ocorrencias": int(v)} for k, v in dados.items()],
        }

    if any(t in q for t in ("tempo", "media", "demora", "resolucao", "resolver")):
        dados = resumo(df)
        return {
            "titulo": "Tempo de resolução",
            "media_tempo_resolucao_dias": dados["media_tempo_resolucao_dias"],
            "mediana_tempo_resolucao_dias": dados["mediana_tempo_resolucao_dias"],
            "registros_com_tempo": int(df["tempo_resolucao_dias"].notna().sum()),
        }

    if any(t in q for t in ("pendente", "aberta", "aberto", "resolvida", "resolvido", "status", "andamento")):
        dados = df.groupby("status")["id_ocorrencia"].nunique().sort_values(ascending=False)
        ranking = [{"status": str(k), "total_ocorrencias": int(v)} for k, v in dados.items()]
        total = int(df["id_ocorrencia"].nunique())

        if "pendente" in q or "aberta" in q or "aberto" in q:
            filtrado = [
                item for item in ranking
                if "pend" in normalizar(item["status"]) or "abert" in normalizar(item["status"])
            ]
            return {
                "titulo": "Ocorrências pendentes ou abertas",
                "total_ocorrencias": sum(x["total_ocorrencias"] for x in filtrado),
                "detalhamento": filtrado or ranking,
            }

        if "resolvid" in q:
            filtrado = [item for item in ranking if "resolvid" in normalizar(item["status"])]
            return {
                "titulo": "Ocorrências resolvidas",
                "total_ocorrencias": sum(x["total_ocorrencias"] for x in filtrado),
                "detalhamento": filtrado or ranking,
            }

        return {"titulo": "Ocorrências por status", "total_geral": total, "ranking": ranking}

    if any(t in q for t in ("solucao", "solucion", "atendida", "atendimento")):
        coluna = df["solucao_ocorrencia"].fillna("").astype(str).str.strip()
        return {
            "titulo": "Informações sobre soluções registradas",
            "ocorrencias_com_solucao": int(coluna.ne("").sum()),
            "ocorrencias_sem_solucao_registrada": int(coluna.eq("").sum()),
        }

    return {
        "titulo": "Panorama geral das ocorrências",
        **resumo(df),
        "distribuicao_por_status": [
            {"status": str(k), "total": int(v)}
            for k, v in df.groupby("status")["id_ocorrencia"].nunique().items()
        ],
    }


def explicar_localmente(resultado: dict, pergunta: str) -> str:
    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 400,
            "num_ctx": 2048,
            "num_gpu": OLLAMA_NUM_GPU,
        },
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA},
            {
                "role": "user",
                "content": (
                    f"PERGUNTA ORIGINAL:\n{pergunta}\n\n"
                    f"DADOS CALCULADOS PELO PYTHON:\n{json.dumps(resultado, ensure_ascii=False)}\n\n"
                    "Explique brevemente os dados apresentados sem inventar informações."
                ),
            },
        ],
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("message", {}).get("content", "").strip()


@router.get("/perguntas")
def perguntas_sugeridas():
    """Sugestões mantidas para compatibilidade; o novo chat aceita texto livre."""
    return {
        "perguntas": PERGUNTAS_SUGERIDAS,
        "modelo": OLLAMA_MODEL,
        "provedor": "Ollama Local (sem nuvem)",
    }


@router.get("/status-ollama")
def status_ollama():
    tags_url = OLLAMA_URL.rsplit("/api/", 1)[0] + "/api/tags"
    try:
        with urllib.request.urlopen(tags_url, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
        models = [m.get("name", "") for m in data.get("models", [])]
        modelo_base = OLLAMA_MODEL if ":" in OLLAMA_MODEL else f"{OLLAMA_MODEL}:latest"
        installed = OLLAMA_MODEL in models or modelo_base in models
        return {
            "conectado": True,
            "modelo_configurado": OLLAMA_MODEL,
            "modelo_instalado": installed,
        }
    except Exception:
        return {
            "conectado": False,
            "modelo_configurado": OLLAMA_MODEL,
            "modelo_instalado": False,
        }


@router.post("")
def consultar_chat(consulta: Consulta):
    pergunta = consulta.pergunta.strip()
    if len(pergunta) < 3:
        raise HTTPException(status_code=422, detail="Digite uma pergunta com pelo menos 3 caracteres.")

    try:
        resultado = calcular(pergunta)
    except (FileNotFoundError, ValueError) as erro:
        raise HTTPException(status_code=503, detail=str(erro))

    try:
        explicacao = explicar_localmente(resultado, pergunta)
        aviso = None if explicacao else "O Ollama não retornou uma explicação. O resultado do Python está disponível."
    except Exception as erro:
        explicacao = (
            "O cálculo foi realizado pelo Python usando o CSV. "
            f"Para receber uma explicação automática, inicie o Ollama Local e instale o modelo '{OLLAMA_MODEL}'."
        )
        aviso = f"Ollama indisponível ({type(erro).__name__}: {erro}). O cálculo do Python foi preservado."

    return {
        "pergunta": pergunta,
        "resultado": resultado,
        "explicacao": explicacao,
        "aviso": aviso,
        "provedor": "Ollama Local (opcional)",
        "modelo": OLLAMA_MODEL,
    }