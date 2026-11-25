"use strict";
const $ = (id) => document.getElementById(id);
const fmt = (v) => Number(v ?? 0).toLocaleString("pt-BR");
const dec = (v) => v == null ? "—" : Number(v).toLocaleString("pt-BR", {minimumFractionDigits:1, maximumFractionDigits:2});
const dataBR = (v) => { if (!v) return "—"; const [a,m,d] = v.split("-"); return `${d}/${m}/${a}`; };

function tabela(id, dados, colunas, totalId) {
  const tbody = $(id); tbody.replaceChildren();
  if (!dados.length) {
    const tr=document.createElement("tr"), td=document.createElement("td");
    td.colSpan=colunas.length; td.className="vazio"; td.textContent="Nenhum registro encontrado.";
    tr.append(td); tbody.append(tr); if(totalId) $(totalId).textContent="0"; return;
  }
  let total=0;
  dados.forEach(item => {
    const tr=document.createElement("tr");
    colunas.forEach(c => {
      const td=document.createElement("td"); td.textContent=c.format ? c.format(item[c.key]) : (item[c.key] ?? "—");
      if(c.num) td.className="numero"; tr.append(td);
    });
    total += Number(item[colunas[1].key] || 0); tbody.append(tr);
  });
  if(totalId) $(totalId).textContent=fmt(total);
}

function svgEl(tag, attrs={}) {
  const el=document.createElementNS("http://www.w3.org/2000/svg",tag);
  Object.entries(attrs).forEach(([k,v])=>el.setAttribute(k,String(v)));
  return el;
}
function desenharOnda(id, dados) {
  const box=$(id); box.replaceChildren();
  if(!Array.isArray(dados)||!dados.length){box.innerHTML='<p class="vazio">Não há dados mensais para exibir.</p>';return;}
  const W=920,H=310,m={t:34,r:28,b:54,l:58},aw=W-m.l-m.r,ah=H-m.t-m.b;
  const vals=dados.map(x=>Math.max(0,Number(x.total_ocorrencias)||0));
  const max=Math.max(...vals,1), teto=Math.ceil(max/50)*50 || max;
  const svg=svgEl("svg",{viewBox:`0 0 ${W} ${H}`,role:"img","aria-label":"Gráfico de linha curva da evolução mensal das ocorrências"});
  const defs=svgEl("defs");
  const grad=svgEl("linearGradient",{id:"resumo-wave-fill",x1:"0",y1:"0",x2:"0",y2:"1"});
  grad.append(svgEl("stop",{offset:"0%","stop-color":"#7565e8","stop-opacity":".32"}));
  grad.append(svgEl("stop",{offset:"100%","stop-color":"#7565e8","stop-opacity":".015"}));
  const glow=svgEl("filter",{id:"resumo-wave-glow",x:"-30%",y:"-30%",width:"160%",height:"160%"});
  glow.append(svgEl("feGaussianBlur",{stdDeviation:"3",result:"blur"}));
  defs.append(grad,glow);svg.append(defs);
  for(let i=0;i<=4;i++){
    const y=m.t+i*ah/4, v=teto*(4-i)/4;
    svg.append(svgEl("line",{x1:m.l,y1:y,x2:W-m.r,y2:y,stroke:"#e9eaf4","stroke-dasharray":"4 6"}));
    const t=svgEl("text",{x:m.l-12,y:y+4,"text-anchor":"end",fill:"#8992a8","font-size":"11"});
    t.textContent=fmt(Math.round(v));svg.append(t);
  }
  const pts=dados.map((d,i)=>({x:m.l+(dados.length===1?aw/2:i*aw/(dados.length-1)),y:m.t+ah-(vals[i]/teto)*ah,d,v:vals[i]}));
  let path=`M ${pts[0].x} ${pts[0].y}`;
  for(let i=1;i<pts.length;i++){
    const a=pts[i-1],b=pts[i],dx=(b.x-a.x)*.42;
    path+=` C ${a.x+dx} ${a.y}, ${b.x-dx} ${b.y}, ${b.x} ${b.y}`;
  }
  const base=m.t+ah;
  svg.append(svgEl("path",{d:`${path} L ${pts.at(-1).x} ${base} L ${pts[0].x} ${base} Z`,fill:"url(#resumo-wave-fill)"}));
  svg.append(svgEl("path",{d:path,fill:"none",stroke:"#6554d8","stroke-width":"4","stroke-linecap":"round","stroke-linejoin":"round"}));
  const step=Math.max(1,Math.ceil(pts.length/10));
  pts.forEach((p,i)=>{
    const c=svgEl("circle",{cx:p.x,cy:p.y,r:i===pts.length-1?6:4.5,fill:"#fff",stroke:"#6554d8","stroke-width":"2.5"});
    const title=svgEl("title");title.textContent=`${p.d.mes}: ${fmt(p.v)} ocorrências`;c.append(title);svg.append(c);
    if(i%step===0||i===pts.length-1){
      const label=svgEl("text",{x:p.x,y:base+24,"text-anchor":"middle",fill:"#69758e","font-size":"11"});
      label.textContent=p.d.mes.slice(5)+"/"+p.d.mes.slice(0,4);svg.append(label);
    }
  });
  box.append(svg);
  const peak=pts.reduce((a,b)=>b.v>a.v?b:a,pts[0]);
  $("resumo-leitura-meses").textContent=`Maior volume do período: ${fmt(peak.v)} ocorrências em ${peak.d.mes.slice(5)}/${peak.d.mes.slice(0,4)}. Total representado no gráfico: ${fmt(vals.reduce((a,b)=>a+b,0))} registros.`;
}
function desenharCategorias(id,dados,campo) {
  const box=$(id);box.replaceChildren();
  if(!Array.isArray(dados)||!dados.length){box.innerHTML='<p class="vazio">Não há dados para exibir.</p>';return;}
  const max=Math.max(...dados.map(x=>Number(x.total_ocorrencias)||0),1);
  dados.forEach((item,i)=>{
    const valor=Number(item.total_ocorrencias)||0;
    const linha=document.createElement("div");linha.className="barra-item";
    const legenda=document.createElement("div");legenda.className="barra-legenda";
    const nome=document.createElement("span");nome.textContent=item[campo]??"Não informado";
    const num=document.createElement("strong");num.textContent=fmt(valor);
    legenda.append(nome,num);
    const trilho=document.createElement("div");trilho.className="barra-trilho";
    const barra=document.createElement("div");barra.className="barra-preenchimento";barra.style.width=`${valor/max*100}%`;
    barra.style.background=i%2?"linear-gradient(90deg,#35aeb7,#75d4ce)":"linear-gradient(90deg,#6655d7,#a99cf7)";
    trilho.append(barra);linha.append(legenda,trilho);box.append(linha);
  });
}

async function carregarResumo() {
  const botao=$("atualizar-resumo"), msg=$("mensagem-resumo");
  botao.disabled=true; msg.hidden=true; $("atualizacao-resumo").textContent="Consultando a API...";
  try {
    const [r, problemas, bairros, meses, gravidade, status] = await Promise.all([
      window.RadarAPI.consultar("/analise/resumo"),
      window.RadarAPI.consultar("/analise/problemas"),
      window.RadarAPI.consultar("/analise/bairros"),
      window.RadarAPI.consultar("/dashboard/ocorrencias-por-mes"),
      window.RadarAPI.consultar("/dashboard/gravidade"),
      window.RadarAPI.consultar("/dashboard/status")
    ]);
    $("r-total").textContent=fmt(r.total_ocorrencias);
    $("r-bairros").textContent=fmt(r.bairros_atendidos);
    $("r-orgaos").textContent=fmt(r.orgaos_responsaveis);
    $("r-media").textContent=r.media_tempo_resolucao_dias == null ? "—" : `${dec(r.media_tempo_resolucao_dias)} dias`;
    $("r-mediana").textContent=r.mediana_tempo_resolucao_dias == null ? "—" : `${dec(r.mediana_tempo_resolucao_dias)} dias`;
    $("periodo-resumo").textContent=`Período dos registros: ${dataBR(r.data_inicial)} a ${dataBR(r.data_final)}`;
    tabela("tabela-problemas", problemas, [
      {key:"tipo_problema"}, {key:"total_ocorrencias",num:true,format:fmt},
      {key:"media_tempo_resolucao_dias",num:true,format:dec}
    ], "total-problemas-resumo");
    tabela("tabela-bairros", bairros, [
      {key:"bairro"}, {key:"total_ocorrencias",num:true,format:fmt},
      {key:"tempo_medio_resolucao_dias",num:true,format:dec}
    ]);
    desenharOnda("resumo-grafico-meses", meses);
    desenharCategorias("resumo-grafico-gravidade", gravidade, "gravidade");
    desenharCategorias("resumo-grafico-status", status, "status");
    $("atualizacao-resumo").textContent=`Última consulta: ${new Date().toLocaleString("pt-BR")}`;
    msg.textContent="Resumo atualizado com sucesso."; msg.className="mensagem sucesso"; msg.hidden=false;
  } catch(e) {
    $("atualizacao-resumo").textContent="Não foi possível atualizar os dados.";
    msg.textContent=e.message || "Erro inesperado."; msg.className="mensagem erro"; msg.hidden=false;
  } finally { botao.disabled=false; }
}
$("atualizar-resumo").addEventListener("click", carregarResumo);
document.addEventListener("DOMContentLoaded", carregarResumo);
