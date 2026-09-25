const API = "http://127.0.0.1:8000";

const camposBooleanos = new Set(["ativo", "ativa", "status_final"]);

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab,.panel").forEach((el) => el.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById(tab.dataset.panel).classList.add("active");
  });
});

function textoRegistro(endpoint, item) {
  if (endpoint === "categorias") return [item.nome, `${item.codigo} · ${item.descricao || "Sem descrição"}`, item.ativo];
  if (endpoint === "status-ocorrencia") return [item.nome, `${item.codigo} · ordem ${item.ordem}`, !item.status_final];
  return [item.nome, item.especialidade, item.ativa];
}

function idRegistro(endpoint, item) {
  return endpoint === "categorias" ? item.id_categoria : endpoint === "status-ocorrencia" ? item.id_status : item.id_equipe;
}

async function listar(endpoint) {
  const area = document.querySelector(`[data-records="${endpoint}"]`);
  area.innerHTML = '<p class="empty">Carregando dados...</p>';
  try {
    const resposta = await fetch(`${API}/${endpoint}`);
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    const itens = await resposta.json();
    area.innerHTML = itens.length ? "" : '<p class="empty">Nenhum registro encontrado.</p>';
    itens.forEach((item) => {
      const [titulo, detalhe, ativo] = textoRegistro(endpoint, item);
      const card = document.createElement("article");
      card.className = "record";
      card.innerHTML = `<span class="record-id">#${idRegistro(endpoint, item)}</span><div><strong>${titulo}</strong><small>${detalhe}</small></div><span class="badge ${ativo ? "" : "off"}">${ativo ? "Ativo" : "Final/Inativo"}</span>`;
      area.appendChild(card);
    });
  } catch (erro) {
    area.innerHTML = '<p class="empty">Inicie a API para carregar os dados.</p>';
  }
}

document.querySelectorAll("form[data-endpoint]").forEach((form) => {
  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    const feedback = form.querySelector(".feedback");
    const dados = {};
    new FormData(form).forEach((valor, chave) => {
      dados[chave] = chave === "ordem" ? Number(valor) : valor;
    });
    form.querySelectorAll('input[type="checkbox"]').forEach((campo) => {
      if (camposBooleanos.has(campo.name)) dados[campo.name] = campo.checked;
    });
    feedback.className = "feedback";
    feedback.textContent = "Enviando...";
    try {
      const resposta = await fetch(`${API}/${form.dataset.endpoint}`, {method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(dados)});
      const corpo = await resposta.json();
      if (!resposta.ok) throw new Error(corpo.detail || `HTTP ${resposta.status}`);
      feedback.classList.add("success");
      feedback.textContent = `Registro criado com sucesso. ID ${idRegistro(form.dataset.endpoint, corpo)}.`;
      form.reset();
      await listar(form.dataset.endpoint);
    } catch (erro) {
      feedback.classList.add("error");
      feedback.textContent = typeof erro.message === "string" ? erro.message : "Não foi possível cadastrar.";
    }
  });
});

document.querySelectorAll(".refresh").forEach((botao) => botao.addEventListener("click", () => listar(botao.dataset.list)));

fetch(`${API}/saude`).then((r) => {
  if (!r.ok) throw new Error();
  document.getElementById("api-status").textContent = "conectada";
}).catch(() => document.getElementById("api-status").textContent = "offline");

["categorias", "status-ocorrencia", "equipes"].forEach(listar);

