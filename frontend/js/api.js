"use strict";

// Camada de comunicação do frontend com a API do backend.
// Se a API estiver em outro endereço, altere somente esta constante.
window.RadarAPI = (() => {
  const BASE_URL = "http://127.0.0.1:8000";

  async function consultar(caminho) {
    let resposta;
    try {
      resposta = await fetch(`${BASE_URL}${caminho}`, {
        method: "GET",
        headers: { Accept: "application/json" },
      });
    } catch {
      throw new Error("Não foi possível conectar à API. Confira se o backend está ligado na porta 8000.");
    }

    let dados;
    try {
      dados = await resposta.json();
    } catch {
      throw new Error(`A API respondeu de forma inválida (${resposta.status}).`);
    }

    if (!resposta.ok) {
      throw new Error(dados.detail || `Falha na consulta (${resposta.status}).`);
    }
    return dados;
  }

  return { consultar };
})();
