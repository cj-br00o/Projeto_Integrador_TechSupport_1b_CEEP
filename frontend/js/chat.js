"use strict";

(() => {
  const $ = (selector) => document.querySelector(selector);

  // ---------------------------------------------------------------------------
  // Configuração da API
  // Para forçar uma URL específica, defina antes do script:
  //   <script>window.RADAR_API_URL = "http://127.0.0.1:8000";</script>
  // ---------------------------------------------------------------------------
  const PORTA_API = 8000;
  const TIMEOUT_DESCOBERTA_MS = 2500;
  const TIMEOUT_CONSULTA_MS = 90000; // o Ollama local pode demorar

  function candidatasApi() {
    const lista = [];
    if (window.RADAR_API_URL) lista.push(window.RADAR_API_URL);

    // Se a página já é servida pelo próprio FastAPI, usa a mesma origem.
    if (location.protocol.startsWith("http") && String(location.port) === String(PORTA_API)) {
      lista.push(location.origin);
    }
    // Página servida por outro servidor (Live Server, http.server...): aponta para a porta da API.
    if (location.protocol.startsWith("http") && location.hostname) {
      lista.push(`${location.protocol}//${location.hostname}:${PORTA_API}`);
    }
    lista.push(`http://127.0.0.1:${PORTA_API}`, `http://localhost:${PORTA_API}`);

    return [...new Set(lista.map((u) => u.replace(/\/+$/, "")))];
  }

  // ---------------------------------------------------------------------------
  // Elementos da página
  // ---------------------------------------------------------------------------
  const form = $("#chat-form");
  const campo = $("#chat-pergunta");
  const botao = $("#chat-enviar");
  const statusChat = $("#chat-status");
  const statusApi = $("#chat-status-api");
  const resposta = $("#chat-resposta");
  const enunciado = $("#chat-enunciado");
  const lista = $("#chat-dados");
  const explicacao = $("#chat-explicacao");
  const aviso = $("#chat-aviso");
  const contador = $("#chat-contador");

  let apiAtiva = null;
  let consultando = false;

  // ---------------------------------------------------------------------------
  // Formatação dos resultados
  // ---------------------------------------------------------------------------
  const formatarNumero = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 2 });

  function formatar(valor) {
    if (valor === null || valor === undefined || valor === "") return "Não informado";
    if (typeof valor === "number") return formatarNumero.format(valor);
    if (typeof valor === "boolean") return valor ? "Sim" : "Não";
    return String(valor);
  }

  function nome(chave) {
    return String(chave).replaceAll("_", " ").replace(/^./, (c) => c.toUpperCase());
  }

  function objetoEmTexto(obj) {
    return Object.entries(obj)
      .map(([k, v]) => `${nome(k)}: ${formatar(v)}`)
      .join(" — ");
  }

  function itemEmTexto(item) {
    return item !== null && typeof item === "object" ? objetoEmTexto(item) : formatar(item);
  }

  function linhas(dados) {
    if (dados === null || dados === undefined) return ["Nenhum resultado encontrado."];

    if (Array.isArray(dados)) {
      return dados.length ? dados.map(itemEmTexto) : ["Não há registros."];
    }
    if (typeof dados !== "object") return [formatar(dados)];

    const saida = [];
    for (const [chave, valor] of Object.entries(dados)) {
      if (Array.isArray(valor)) {
        saida.push(`${nome(chave)}:`);
        valor.forEach((item) => saida.push(itemEmTexto(item)));
      } else if (valor !== null && typeof valor === "object") {
        saida.push(`${nome(chave)}: ${objetoEmTexto(valor)}`);
      } else {
        saida.push(`${nome(chave)}: ${formatar(valor)}`);
      }
    }
    return saida;
  }

  // ---------------------------------------------------------------------------
  // Estado da interface
  // ---------------------------------------------------------------------------
  function atualizar() {
    botao.disabled = consultando || campo.value.trim().length < 3;
    contador.textContent = `${campo.value.length}/500`;
  }

  function marcarApi(conectada, texto) {
    statusApi.textContent = texto;
    statusApi.classList.toggle("chat-status-offline", !conectada);
  }

  // ---------------------------------------------------------------------------
  // Descoberta da API
  // Usa GET /chat/status-ollama (existe no chat.py) e, se falhar, GET /health.
  // ---------------------------------------------------------------------------
  async function respondeOk(url) {
    try {
      const r = await fetch(url, { signal: AbortSignal.timeout(TIMEOUT_DESCOBERTA_MS) });
      return r.ok;
    } catch (_) {
      return false;
    }
  }

  async function descobrirApi() {
    for (const base of candidatasApi()) {
      if ((await respondeOk(`${base}/chat/status-ollama`)) || (await respondeOk(`${base}/health`))) {
        return base;
      }
    }
    return null;
  }

  async function verificar() {
    apiAtiva = await descobrirApi();
    marcarApi(Boolean(apiAtiva), apiAtiva ? "API Python conectada" : "API desconectada — inicie iniciar_linux.sh");
  }

  // ---------------------------------------------------------------------------
  // Envio da pergunta
  // ---------------------------------------------------------------------------
  async function enviarPergunta(base, pergunta) {
    const url = `${base}/chat`;
    let r;
    try {
      r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ pergunta }),
        signal: AbortSignal.timeout(TIMEOUT_CONSULTA_MS),
      });
    } catch (err) {
      apiAtiva = null;
      throw new Error(
        err.name === "TimeoutError"
          ? "A consulta demorou demais. Tente novamente."
          : "Falha de conexão com a API Python (verifique se está rodando e se o CORS está habilitado)."
      );
    }

    const bruto = await r.text();
    let dados = null;
    try {
      dados = JSON.parse(bruto);
    } catch (_) {
      /* resposta não-JSON tratada abaixo */
    }

    if (r.status === 405 || r.status === 404) {
      apiAtiva = null; // força nova descoberta na próxima tentativa
      throw new Error(
        `HTTP ${r.status} em POST ${url}. Esse endereço não é a API FastAPI do Radar (ou a rota /chat não foi registrada). Confira http://127.0.0.1:${PORTA_API}/docs.`
      );
    }
    if (!dados) throw new Error(`Resposta inválida da API (HTTP ${r.status}).`);

    if (!r.ok) {
      let detalhe = `Erro HTTP ${r.status}: verifique os dados enviados.`;
      if (typeof dados.detail === "string") {
        detalhe = dados.detail;
      } else if (Array.isArray(dados.detail) && dados.detail[0]?.msg) {
        detalhe = dados.detail[0].msg; // erro 422 do Pydantic
      }
      throw new Error(detalhe);
    }
    return dados;
  }

  function mostrarResposta(dados, pergunta) {
    enunciado.textContent = dados.pergunta || pergunta;

    lista.replaceChildren();
    linhas(dados.resultado).forEach((texto) => {
      const li = document.createElement("li");
      li.textContent = texto;
      lista.append(li);
    });

    explicacao.textContent =
      dados.explicacao || "O Python calculou o resultado. A explicação adicional do Ollama não está disponível.";

    if (dados.aviso) {
      aviso.textContent = dados.aviso;
      aviso.classList.remove("chat-hidden");
    } else {
      aviso.classList.add("chat-hidden");
    }
    resposta.classList.remove("chat-hidden");
  }

  async function aoEnviar(evento) {
    evento.preventDefault();
    const pergunta = campo.value.trim();
    if (pergunta.length < 3 || consultando) return;

    consultando = true;
    atualizar();
    resposta.classList.add("chat-hidden");
    aviso.classList.add("chat-hidden");
    statusChat.textContent = "Consultando os dados…";

    try {
      if (!apiAtiva) {
        apiAtiva = await descobrirApi();
        marcarApi(Boolean(apiAtiva), apiAtiva ? "API Python conectada" : "API desconectada — inicie iniciar_linux.sh");
      }
      if (!apiAtiva) {
        throw new Error("API Python não encontrada. Execute iniciar_linux.sh e mantenha o terminal aberto.");
      }

      const dados = await enviarPergunta(apiAtiva, pergunta);
      mostrarResposta(dados, pergunta);
      statusChat.textContent = "Consulta concluída com os dados do CSV.";
    } catch (err) {
      statusChat.textContent = err.message || "Não foi possível concluir a consulta.";
      if (!apiAtiva) marcarApi(false, "Verifique a conexão com a API");
      console.error("[Radar IA]", err);
    } finally {
      consultando = false;
      atualizar();
    }
  }

  // ---------------------------------------------------------------------------
  // Eventos
  // ---------------------------------------------------------------------------
  document.querySelectorAll(".chat-sugestao").forEach((botaoSugestao) => {
    botaoSugestao.addEventListener("click", () => {
      campo.value = botaoSugestao.textContent.trim();
      atualizar();
      campo.focus();
      form.requestSubmit();
    });
  });

  campo.addEventListener("input", atualizar);
  form.addEventListener("submit", aoEnviar);

  atualizar();
  verificar();
})();