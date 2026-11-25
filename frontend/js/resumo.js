"use strict";

const $ = (id) => document.getElementById(id);
const elementos = {
  atualizacao: $("atualizacao"),
  periodo: $("periodo-dados"),
  botao: $("botao-atualizar"),
  mensagem: $("mensagem"),
  resumo: $("resumo"),
  ocorrencias: $("total-ocorrencias"),
  bairros: $("total-bairros"),
  orgaos: $("total-orgaos"),
  media: $("media-resolucao"),
  mediana: $("mediana-resolucao"),
  problemas: $("lista-problemas"),
  totalProblemas: $("total-geral-problemas"),
  listaBairros: $("lista-bairros"),
  meses: $("grafico-meses"),
  gravidade: $("grafico-gravidade"),
  status: $("grafico-status"),
  insights: $("lista-insights"),
};

const inteiro = (valor) => Number(valor).toLocaleString("pt-BR");
const decimal = (valor) => valor == null ? "—" : Number(valor).toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 2 });
const dataBR = (valor) => {
  if (!valor) return "—";
  const [ano, mes, dia] = valor.split("-");
  return `${dia}/${mes}/${ano}`;
};

function mostrarMensagem(texto, tipo = "sucesso") {
  elementos.mensagem.textContent = texto;
  elementos.mensagem.className = `mensagem ${tipo}`;
  elementos.mensagem.hidden = false;
}

function preencherTabela(tbody, itens, colunas, totalCell = null) {
  tbody.replaceChildren();
  if (!Array.isArray(itens) || itens.length === 0) {
    const linha = document.createElement("tr");
    const celula = document.createElement("td");
    celula.colSpan = colunas.length;
    celula.className = "vazio";
    celula.textContent = "Nenhum registro encontrado.";
    linha.appendChild(celula);
    tbody.appendChild(linha);
    if (totalCell) totalCell.textContent = "0";
    return;
  }
  let soma = 0;
  for (const item of itens) {
    const linha = document.createElement("tr");
    for (const coluna of colunas) {
      const celula = document.createElement("td");
      const valor = item[coluna.campo];
      celula.textContent = coluna.formatar ? coluna.formatar(valor) : (valor ?? "—");
      if (coluna.numero) celula.className = "numero";
      linha.appendChild(celula);
    }
    soma += Number(item[colunas[1]?.campo] || 0);
    tbody.appendChild(linha);
  }
  if (totalCell) totalCell.textContent = inteiro(soma);
}

function desenharBarras(container, itens, campoNome, campoValor, formatarNome = (v) => v, tipo = "categoria") {
  container.replaceChildren();
  container.className = `grafico-visual ${tipo === "temporal" ? "grafico-temporal" : "grafico-categorias"}`;

  if (!Array.isArray(itens) || itens.length === 0) {
    const vazio = document.createElement("p");
    vazio.className = "vazio";
    vazio.textContent = "Não há dados para exibir.";
    container.appendChild(vazio);
    return;
  }

  const ns = "http://www.w3.org/2000/svg";
  const criar = (tag, attrs = {}) => {
    const el = document.createElementNS(ns, tag);
    for (const [chave, valor] of Object.entries(attrs)) el.setAttribute(chave, String(valor));
    return el;
  };
  const svg = criar("svg", {
    role: "img",
    "aria-label": tipo === "temporal" ? "Evolução mensal das ocorrências" : "Comparação de ocorrências por categoria"
  });
  const valores = itens.map(item => Math.max(0, Number(item[campoValor]) || 0));
  const maximo = Math.max(...valores, 1);

  if (tipo === "temporal") {
    // Linha temporal: não rotula todos os pontos para evitar sobreposição.
    const largura = 900;
    const altura = 260;
    const margem = { top: 24, right: 22, bottom: 48, left: 48 };
    const areaW = largura - margem.left - margem.right;
    const areaH = altura - margem.top - margem.bottom;
    const teto = Math.ceil(maximo / 10) * 10 || 10;
    svg.setAttribute("viewBox", `0 0 ${largura} ${altura}`);
    svg.setAttribute("width", largura);
    svg.setAttribute("height", altura);

    for (let i = 0; i <= 4; i++) {
      const y = margem.top + i * areaH / 4;
      const valor = teto * (4 - i) / 4;
      svg.appendChild(criar("line", { x1: margem.left, y1: y, x2: largura - margem.right, y2: y, stroke: "#e7edf4", "stroke-width": 1 }));
      const tick = criar("text", { x: margem.left - 9, y: y + 4, "text-anchor": "end", fill: "#75849a", "font-size": 11 });
      tick.textContent = inteiro(valor);
      svg.appendChild(tick);
    }

    const pontos = itens.map((item, i) => ({
      x: margem.left + (itens.length === 1 ? areaW / 2 : i * areaW / (itens.length - 1)),
      y: margem.top + areaH - (valores[i] / teto) * areaH,
      item,
      valor: valores[i]
    }));
    let caminho = `M ${pontos[0].x} ${pontos[0].y}`;
    for (let i = 1; i < pontos.length; i++) {
      const anterior = pontos[i - 1], atual = pontos[i];
      const meio = (anterior.x + atual.x) / 2;
      caminho += ` C ${meio} ${anterior.y}, ${meio} ${atual.y}, ${atual.x} ${atual.y}`;
    }
    const baseY = margem.top + areaH;
    const area = `${caminho} L ${pontos[pontos.length - 1].x} ${baseY} L ${pontos[0].x} ${baseY} Z`;
    const defs = criar("defs");
    const grad = criar("linearGradient", { id: `area-${container.id}`, x1: 0, y1: 0, x2: 0, y2: 1 });
    grad.append(criar("stop", { offset: "0%", "stop-color": "#397fc0", "stop-opacity": .28 }), criar("stop", { offset: "100%", "stop-color": "#397fc0", "stop-opacity": .02 }));
    defs.appendChild(grad);
    svg.appendChild(defs);
    svg.appendChild(criar("path", { d: area, fill: `url(#area-${container.id})` }));
    svg.appendChild(criar("path", { d: caminho, fill: "none", stroke: "#6556d9", "stroke-width": 3, "stroke-linecap": "round", "stroke-linejoin": "round" }));

    const passo = Math.max(1, Math.ceil(itens.length / 10));
    pontos.forEach((ponto, i) => {
      const circulo = criar("circle", { cx: ponto.x, cy: ponto.y, r: 3.5, fill: "#fff", stroke: "#6556d9", "stroke-width": 2 });
      const dica = criar("title");
      dica.textContent = `${formatarNome(ponto.item[campoNome])}: ${inteiro(ponto.valor)} ocorrências`;
      circulo.appendChild(dica);
      svg.appendChild(circulo);
      if (i % passo === 0 || i === pontos.length - 1) {
        const rotulo = criar("text", { x: ponto.x, y: baseY + 22, "text-anchor": "middle", fill: "#65758b", "font-size": 10 });
        rotulo.textContent = formatarNome(ponto.item[campoNome]);
        svg.appendChild(rotulo);
        const valorTexto = criar("text", { x: ponto.x, y: ponto.y - 10, "text-anchor": "middle", fill: "#5144b7", "font-size": 11, "font-weight": 700 });
        valorTexto.textContent = inteiro(ponto.valor);
        svg.appendChild(valorTexto);
      }
    });
  } else if (tipo === "area") {
    // Área suave para comparar níveis ordenados de gravidade, seguindo a referência visual.
    const largura = 620, altura = 260;
    const margem = { top: 28, right: 28, bottom: 42, left: 34 };
    const areaW = largura - margem.left - margem.right;
    const areaH = altura - margem.top - margem.bottom;
    const teto = Math.ceil(maximo / 100) * 100 || 100;
    svg.setAttribute("viewBox", `0 0 ${largura} ${altura}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", altura);
    for (let i = 0; i <= 4; i++) {
      const y = margem.top + i * areaH / 4;
      const valor = teto * (4 - i) / 4;
      svg.appendChild(criar("line", { x1: margem.left, y1: y, x2: largura - margem.right, y2: y, stroke: "#e9e8f2", "stroke-width": 1 }));
      const tick = criar("text", { x: margem.left - 7, y: y + 4, "text-anchor": "end", fill: "#8790a3", "font-size": 10 });
      tick.textContent = inteiro(valor);
      svg.appendChild(tick);
    }
    const pontos = itens.map((item, i) => ({
      x: margem.left + (itens.length === 1 ? areaW / 2 : i * areaW / (itens.length - 1)),
      y: margem.top + areaH - (valores[i] / teto) * areaH,
      item, valor: valores[i]
    }));
    let caminho = `M ${pontos[0].x} ${pontos[0].y}`;
    for (let i = 1; i < pontos.length; i++) {
      const a = pontos[i - 1], b = pontos[i], meio = (a.x + b.x) / 2;
      caminho += ` C ${meio} ${a.y}, ${meio} ${b.y}, ${b.x} ${b.y}`;
    }
    const baseY = margem.top + areaH;
    const area = `${caminho} L ${pontos[pontos.length - 1].x} ${baseY} L ${pontos[0].x} ${baseY} Z`;
    const defs = criar("defs");
    const grad = criar("linearGradient", { id: `area-${container.id}`, x1: 0, y1: 0, x2: 0, y2: 1 });
    grad.append(criar("stop", { offset: "0%", "stop-color": "#7552d1", "stop-opacity": .38 }));
    grad.append(criar("stop", { offset: "100%", "stop-color": "#7552d1", "stop-opacity": .035 }));
    defs.appendChild(grad); svg.appendChild(defs);
    svg.appendChild(criar("path", { d: area, fill: `url(#area-${container.id})` }));
    svg.appendChild(criar("path", { d: caminho, fill: "none", stroke: "#6242bd", "stroke-width": 3, "stroke-linecap": "round" }));
    pontos.forEach((p, i) => {
      svg.appendChild(criar("circle", { cx: p.x, cy: p.y, r: 4, fill: "#fff", stroke: "#6242bd", "stroke-width": 2 }));
      const valor = criar("text", { x: p.x, y: p.y - 10, "text-anchor": "middle", fill: "#5144b7", "font-size": 11, "font-weight": 700 });
      valor.textContent = inteiro(p.valor); svg.appendChild(valor);
      const nome = criar("text", { x: p.x, y: baseY + 20, "text-anchor": "middle", fill: "#788397", "font-size": 11 });
      nome.textContent = formatarNome(p.item[campoNome]); svg.appendChild(nome);
    });
  } else {
    // Barras horizontais: adequadas para categorias sem continuidade entre si.
    const largura = 680;
    const altura = Math.max(150, itens.length * 54 + 24);
    const inicioBarra = 145;
    const fimBarra = largura - 65;
    const larguraBarra = fimBarra - inicioBarra;
    svg.setAttribute("viewBox", `0 0 ${largura} ${altura}`);
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", altura);
    const paleta = ["#6757d8", "#3aaeb8", "#8c7be8", "#e4a34f", "#4d79c8", "#5eaf91"];
    itens.forEach((item, i) => {
      const y = 16 + i * 54;
      const valor = valores[i];
      const cor = paleta[i % paleta.length];
      const nome = String(formatarNome(item[campoNome]));
      const rotulo = criar("text", { x: 8, y: y + 20, fill: "#40536f", "font-size": 13, "font-weight": 600 });
      rotulo.textContent = nome.length > 17 ? `${nome.slice(0, 16)}…` : nome;
      svg.appendChild(rotulo);
      svg.appendChild(criar("rect", { x: inicioBarra, y: y + 5, width: larguraBarra, height: 18, rx: 9, fill: "#edf2f8" }));
      svg.appendChild(criar("rect", { x: inicioBarra, y: y + 5, width: Math.max(valor > 0 ? 3 : 0, larguraBarra * valor / maximo), height: 18, rx: 9, fill: cor }));
      const numero = criar("text", { x: largura - 8, y: y + 20, "text-anchor": "end", fill: "#263456", "font-size": 13, "font-weight": 800 });
      numero.textContent = inteiro(valor);
      svg.appendChild(numero);
      const dica = criar("title");
      dica.textContent = `${nome}: ${inteiro(valor)} ocorrências`;
      svg.lastChild.appendChild(dica);
    });
  }

  container.appendChild(svg);
}

function gerarInsights(resumo, problemas, bairros, meses, gravidade, status) {
  elementos.insights.replaceChildren();

  const maior = (lista, campoNome, campoValor) => {
    if (!Array.isArray(lista) || lista.length === 0) return null;
    return lista.reduce((atual, item) =>
      Number(item[campoValor] || 0) > Number(atual[campoValor] || 0) ? item : atual
    );
  };

  const problemaPrincipal = maior(problemas, "tipo_problema", "total_ocorrencias");
  const bairroPrincipal = maior(bairros, "bairro", "total_ocorrencias");
  const mesPrincipal = maior(meses, "mes", "total_ocorrencias");
  const gravidadePrincipal = maior(gravidade, "gravidade", "total_ocorrencias");
  const statusPrincipal = maior(status, "status", "total_ocorrencias");

  const destaques = [
    problemaPrincipal && {
      titulo: "Problema mais registrado",
      valor: problemaPrincipal.tipo_problema,
      detalhe: `${inteiro(problemaPrincipal.total_ocorrencias)} ocorrências`,
    },
    bairroPrincipal && {
      titulo: "Bairro com mais registros",
      valor: bairroPrincipal.bairro,
      detalhe: `${inteiro(bairroPrincipal.total_ocorrencias)} ocorrências`,
    },
    mesPrincipal && {
      titulo: "Mês com maior volume",
      valor: (() => {
        const [ano, mes] = mesPrincipal.mes.split("-");
        return `${mes}/${ano}`;
      })(),
      detalhe: `${inteiro(mesPrincipal.total_ocorrencias)} ocorrências`,
    },
    gravidadePrincipal && {
      titulo: "Gravidade mais frequente",
      valor: gravidadePrincipal.gravidade,
      detalhe: `${inteiro(gravidadePrincipal.total_ocorrencias)} ocorrências`,
    },
    statusPrincipal && {
      titulo: "Status predominante",
      valor: statusPrincipal.status,
      detalhe: `${inteiro(statusPrincipal.total_ocorrencias)} registros`,
    },
  ].filter(Boolean);

  if (!destaques.length) {
    const vazio = document.createElement("p");
    vazio.className = "vazio";
    vazio.textContent = "Não há dados suficientes para gerar destaques.";
    elementos.insights.appendChild(vazio);
    return;
  }

  for (const destaque of destaques) {
    const artigo = document.createElement("article");
    artigo.className = "insight-item";
    const titulo = document.createElement("p");
    titulo.className = "insight-titulo";
    titulo.textContent = destaque.titulo;
    const valor = document.createElement("strong");
    valor.className = "insight-valor";
    valor.textContent = destaque.valor;
    const detalhe = document.createElement("span");
    detalhe.className = "insight-detalhe";
    detalhe.textContent = destaque.detalhe;
    artigo.append(titulo, valor, detalhe);
    elementos.insights.appendChild(artigo);
  }
}

async function carregarDados() {
  elementos.botao.disabled = true;
  elementos.resumo.setAttribute("aria-busy", "true");
  elementos.atualizacao.textContent = "Consultando a API...";
  elementos.mensagem.hidden = true;
  try {
    const [resumo, problemas, bairros, meses, gravidade, status] = await Promise.all([
      window.RadarAPI.consultar("/analise/resumo"),
      window.RadarAPI.consultar("/analise/problemas"),
      window.RadarAPI.consultar("/analise/bairros"),
      window.RadarAPI.consultar("/dashboard/ocorrencias-por-mes"),
      window.RadarAPI.consultar("/dashboard/gravidade"),
      window.RadarAPI.consultar("/dashboard/status"),
    ]);

    elementos.ocorrencias.textContent = inteiro(resumo.total_ocorrencias);
    elementos.bairros.textContent = inteiro(resumo.bairros_atendidos);
    elementos.orgaos.textContent = inteiro(resumo.orgaos_responsaveis);
    elementos.media.textContent = resumo.media_tempo_resolucao_dias == null ? "—" : `${decimal(resumo.media_tempo_resolucao_dias)} dias`;
    elementos.mediana.textContent = resumo.mediana_tempo_resolucao_dias == null ? "—" : `${decimal(resumo.mediana_tempo_resolucao_dias)} dias`;
    elementos.periodo.textContent = `Período dos registros: ${dataBR(resumo.data_inicial)} a ${dataBR(resumo.data_final)}`;

    preencherTabela(elementos.problemas, problemas, [
      { campo: "tipo_problema" },
      { campo: "total_ocorrencias", numero: true, formatar: inteiro },
      { campo: "media_tempo_resolucao_dias", numero: true, formatar: decimal },
    ], elementos.totalProblemas);
    preencherTabela(elementos.listaBairros, bairros, [
      { campo: "bairro" },
      { campo: "total_ocorrencias", numero: true, formatar: inteiro },
      { campo: "tempo_medio_resolucao_dias", numero: true, formatar: decimal },
    ]);
    desenharBarras(elementos.meses, meses, "mes", "total_ocorrencias", (mes) => {
      const [ano, numeroMes] = mes.split("-");
      return `${numeroMes}/${ano}`;
    }, "temporal");
    desenharBarras(elementos.gravidade, gravidade, "gravidade", "total_ocorrencias", (v) => v);
    desenharBarras(elementos.status, status, "status", "total_ocorrencias");
    gerarInsights(resumo, problemas, bairros, meses, gravidade, status);

    elementos.atualizacao.textContent = `Última consulta: ${new Date().toLocaleString("pt-BR")}`;
    mostrarMensagem("Dados atualizados com sucesso.", "sucesso");
  } catch (erro) {
    elementos.atualizacao.textContent = "Não foi possível atualizar os dados.";
    mostrarMensagem(erro.message || "Ocorreu um erro inesperado.", "erro");
  } finally {
    elementos.botao.disabled = false;
    elementos.resumo.setAttribute("aria-busy", "false");
  }
}

elementos.botao.addEventListener("click", carregarDados);
document.addEventListener("DOMContentLoaded", carregarDados);
