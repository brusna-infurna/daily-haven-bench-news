#!/usr/bin/env python3
"""Gera o Brainstorm do time (www.projetorepertorio.com.br/benchnews/brainstorm/):
quadro de conversa ao vivo por área (Vendas, Membership, Parcerias, Marketing/Social), com Supabase Realtime.
Junta os comentários feitos nos itens da sala (tabela comentarios, mapeados pela área do item) com as mensagens
escritas direto no quadro (tabela brainstorm). Mesma identidade da sala: nome guardado no aparelho.
Uso: python3 build_brainstorm.py SUPABASE_URL SUPABASE_ANON_KEY [destino]
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3:
    print("uso: build_brainstorm.py SUPABASE_URL SUPABASE_ANON_KEY [destino]"); sys.exit(1)
SB_URL, SB_KEY = sys.argv[1], sys.argv[2]
dest = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "brainstorm", "index.html")

site = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", site, re.S).group(1)
sala = open(os.path.join(HERE, "build_sala.py"), encoding="utf-8").read()
extra = re.search(r'EXTRA_CSS = r"""(.*?)"""', sala, re.S).group(1)
extra += r"""
  .login{max-width:520px;margin:40px auto;padding:28px;background:var(--paper);border:1px solid var(--rule)}
  .login h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;margin-bottom:8px}
  .login p{font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--espresso);margin-bottom:14px}
  .top-actions{display:flex;gap:14px;align-items:center}
  select{font-family:var(--serif2);font-size:17px;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:10px 12px;width:100%}

  /* brainstorm */
  .bs-intro{font-family:var(--serif2);font-size:18px;line-height:1.5;color:var(--espresso);max-width:70ch;padding:22px 0 8px}
  .bs-grid{display:flex;flex-direction:column;gap:18px;padding-top:22px}
  .bs-col{display:flex;flex-direction:column;background:var(--paper);border:1px solid var(--rule);border-top:3px solid var(--terracotta)}
  .bs-col.a-vendas{border-top-color:var(--forest)} .bs-col.a-membership{border-top-color:var(--terracotta)} .bs-col.a-parcerias{border-top-color:var(--teal)} .bs-col.a-marketing{border-top-color:var(--plum)}
  .bs-col h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:24px;line-height:1.1;padding:14px 16px 10px;border-bottom:1px solid var(--rule);cursor:pointer;display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;user-select:none}
  .bs-col h2:hover{background:rgba(63,56,50,.04)}
  .bs-col h2 small{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}
  .bs-col h2 em{font-style:normal;font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-left:10px}
  .bs-col.expand{order:-1;border-width:1px;border-top-width:4px;box-shadow:0 10px 30px rgba(43,38,34,.08)}
  .bs-col.expand h2{font-size:30px}
  .bs-feed{overflow-y:auto;max-height:260px;padding:6px 16px 10px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
  .bs-col.expand .bs-feed{max-height:68vh;min-height:40vh}
  @media(min-width:900px){.bs-col .bs-form{flex-direction:row;align-items:flex-end}.bs-col .bs-form textarea{flex:1 1 auto}.bs-col .bs-form .row{flex-direction:column;align-items:flex-end;gap:6px}}
  .bs-msg{font-family:var(--serif2);font-size:16.5px;line-height:1.42;color:var(--espresso);padding:8px 0 10px;border-bottom:1px solid var(--rule);word-break:break-word}
  .bs-msg .txt{white-space:pre-wrap;display:block}
  .bs-msg.mine{color:var(--ink)}
  .bs-msg .who{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-bottom:4px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;white-space:normal}
  .bs-msg .who b{color:var(--ink);font-weight:700}
  .bs-msg .ref{display:block;font-family:var(--sans);font-size:11px;color:var(--mute);margin-top:6px;white-space:normal}
  .bs-msg .ref a{text-decoration:underline;color:var(--soft)}
  .bs-msg .bc{font-family:var(--sans);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;background:transparent;border:1px solid var(--ochre);color:var(--ochre);padding:4px 8px;cursor:pointer}
  .bs-msg .bc:hover{background:var(--ochre);color:var(--paper)}
  .bs-msg .pill.basecamp{color:var(--ochre);border-color:var(--ochre)}
  .bs-msg .apagar{font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;background:none;border:0;color:var(--mute);cursor:pointer;padding:0}
  .bs-msg .apagar:hover{color:var(--terracotta)}
  .bs-vazio{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute);padding:16px 0}
  .bs-form{padding:10px 16px 14px;border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:8px;background:var(--paper)}
  .bs-form textarea{min-height:52px}
  .bs-form .row{justify-content:space-between}
  .bs-form .hint{font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
  .bs-msg .st{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px;align-items:center}
  .bs-msg .st button{font-family:var(--sans);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;background:transparent;border:1px solid var(--rule);color:var(--soft);padding:4px 8px;cursor:pointer}
  .bs-msg .st button:hover{border-color:var(--espresso);color:var(--ink)}
  .bs-msg.st-andamento{border-left:3px solid var(--forest);padding-left:10px}
  .bs-msg .pill{margin:0}
  .bs-enc{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);background:transparent;border:0;border-bottom:1px solid var(--rule);padding:8px 0;cursor:pointer;text-align:left}
  .bs-enc:hover{color:var(--ink)}
  .bs-msg.encerrada{opacity:.6}
  .bs-msg.encerrada.st-descartada{text-decoration:line-through}
  .bc-box{margin-top:18px;padding:14px 16px;background:var(--paper);border:1px solid var(--rule);border-left:3px solid var(--ochre)}
  .bc-box h3{font-family:var(--serif);font-weight:500;font-style:italic;font-size:20px;margin-bottom:6px}
  .bc-box p{font-family:var(--serif2);font-size:16px;line-height:1.45;color:var(--espresso);margin-bottom:10px}
  .bc-box .grid{display:grid;grid-template-columns:1fr;gap:10px}
  @media(min-width:900px){.bc-box .grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .bc-box label{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);display:block;margin-bottom:4px}
  .bc-box select{font-size:15px;padding:8px 10px}
  .bc-box .ok{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--forest)}

  .bs-resp{margin-top:8px;padding:8px 0 2px 12px;border-left:2px solid var(--teal);font-family:var(--serif2);font-size:16px;line-height:1.42;color:var(--ink);white-space:pre-wrap}
  .bs-resp i{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:4px}
  .live{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);display:inline-flex;align-items:center;gap:6px}
  .live i{width:7px;height:7px;border-radius:50%;background:var(--sand);display:inline-block}
  .live.on i{background:var(--forest)}
"""

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Brainstorm · Haven Bench News</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
<style>__CSS__</style>
</head>
<body>
<div class="page">
  <header class="mast">
    <div class="kicker">Brainstorm do time · conversa ao vivo por área</div>
    <h1>Daily Haven Bench News</h1>
    <div class="kicker">Vendas · Membership · Parcerias · Marketing/Social</div>
  </header>
  <div class="folio">
    <span><a href="../sala/" style="text-decoration:underline">Voltar pra sala do time</a></span>
    <span class="live" id="live"><i></i><span id="live-txt">conectando</span></span>
    <span class="top-actions"><span class="me" id="me"></span><button class="btn sm ghost" id="sair" hidden>Trocar nome</button></span>
  </div>
  <div class="ro" id="ro" hidden></div>

  <section class="login" id="login" hidden>
    <h2>Quem é você?</h2>
    <p>O brainstorm é aberto pra quem tem o link. Escolha seu nome uma vez; ele fica guardado neste aparelho e assina o que você escrever.</p>
    <form class="form" id="login-form"><select id="login-nome"><option value="">Escolher nome</option><option>Bru</option><option>Teti</option><option>Carolina</option><option>Omi</option><option>Julia</option><option>Julinha</option><option value="__outro">Outro nome</option></select><input type="text" id="login-outro" placeholder="Seu nome" maxlength="40" hidden><div class="row"><button class="btn" type="submit" id="login-btn">Entrar</button></div><div class="note" id="login-note"></div></form>
  </section>

  <div id="app" hidden>
    <p class="bs-intro">Quatro mesas, uma por área. Entram aqui os comentários que o time deixa nos itens da sala, já separados pela área do item, e o que for escrito direto nestas mesas. Tudo aparece na hora pra quem estiver com a página aberta. Toque no título de uma mesa pra abrir só ela em cima, com espaço pra rolar a conversa; toque de novo pra voltar. Cada conversa fica na mesa até alguém marcar em andamento, finalizar ou desprezar; as encerradas ficam na dobra de cada mesa. "Levar pro Basecamp" cria a tarefa na lista do Basecamp ligada à mesa.</p>
    <div class="bc-box" id="bc-box" hidden>
      <h3>Basecamp</h3>
      <p id="bc-txt"></p>
      <div class="grid" id="bc-grid" hidden></div>
    </div>
    <div class="bs-grid" id="grid"></div>
  </div>

  <footer>
    <p>Cada mensagem traz autor, edição do Bench a que se refere e hora. O quadro é lido pela rotina da manhã do Bench. A sala do time fica em <a href="../sala/" style="text-decoration:underline">benchnews/sala</a>.</p>
  </footer>
</div>
<script>
const SB_URL = "__SB_URL__", SB_KEY = "__SB_KEY__";
const RADAR_URL = "https://brusna-infurna.github.io/daily-haven-bench-news/radar-data.json";
const sb = supabase.createClient(SB_URL, SB_KEY);
const AREAS = [["vendas","Vendas","itens marcados pra vendas"],["membership","Membership","itens marcados pra clube"],["parcerias","Parcerias","itens marcados pra parcerias"],["marketing","Marketing/Social","itens marcados pra marketing"]];
const PARA2AREA = {vendas:"vendas", clube:"membership", parcerias:"parcerias", marketing:"marketing"};
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtShort = d => { if(!d) return ""; const [y,m,dd]=String(d).slice(0,10).split("-"); return `${+dd} ${MS[+m-1]}`; };
const fmtTs = t => { const d=new Date(t); return isNaN(d)?"":`${d.getDate()} ${MS[d.getMonth()]} ${String(d.getHours()).padStart(2,"0")}h${String(d.getMinutes()).padStart(2,"0")}`; };
const $ = id => document.getElementById(id);
function note(msg){ const ro=$("ro"); ro.hidden=!msg; ro.innerHTML = msg ? `<b>Aviso.</b> ${esc(msg)}` : ""; }

let RADAR = {dias:[]}; const lookup = {};
let me = "", isAdmin = false, expandida = "";
const bcListas = {};
const FN = SB_URL + "/functions/v1/basecamp";
let bcStatus = null, bcProjects = null;
const verEnc = {vendas:false,membership:false,parcerias:false,marketing:false};
const ST = {aberta:"Aberta",andamento:"Em andamento",finalizada:"Finalizada",descartada:"Desprezada"};
const data = {brainstorm:[], comentarios:[], ideias:[]};
const IDST = {avaliando:"aberta", andamento:"andamento", feita:"finalizada", descartada:"descartada"};
const IDST_BACK = {aberta:"avaliando", andamento:"andamento", finalizada:"feita", descartada:"descartada"};
const ASSUNTO_MAX = 90;
const respDe = m => { if (m.tabela==="ideias") return ""; const R = m.tabela==="brainstorm" ? (RADAR.respostas_brainstorm||{}) : (RADAR.respostas_comentarios||{}); const r = R[m.id]; return r && r.resposta ? `<div class="bs-resp"><i>Bru, via Bench${r.t?" · "+esc(String(r.t).replace("T"," ")):""}</i>${esc(r.resposta)}</div>` : ""; };

/* identidade por nome, igual à sala */
const NOME_KEY = "benchnews-sala-nome";
const lerNome = () => { try { return (localStorage.getItem(NOME_KEY)||"").trim(); } catch(e){ return ""; } };
const guardarNome = n => { try { localStorage.setItem(NOME_KEY, n); } catch(e){} };
$("login-nome").addEventListener("change", e => { $("login-outro").hidden = e.target.value !== "__outro"; if (!$("login-outro").hidden) $("login-outro").focus(); });
$("login-form").addEventListener("submit", e => {
  e.preventDefault(); let n = $("login-nome").value; if (n === "__outro") n = $("login-outro").value;
  n = (n||"").trim().replace(/\s+/g," ").slice(0,40);
  if (!n) { $("login-note").textContent = "Escolha ou digite um nome."; return; }
  guardarNome(n); entrar(n);
});
$("sair").addEventListener("click", () => { try { localStorage.removeItem(NOME_KEY); } catch(e){} location.reload(); });

async function boot(){
  try { RADAR = await (await fetch(RADAR_URL, {cache:"no-store"})).json(); } catch(e){ note("Não consegui carregar as edições agora. O quadro abre mesmo assim."); }
  (RADAR.dias||[]).forEach(d => { (d.itens||[]).forEach((i,n)=>lookup[`e${d.data}-i${n}`]={day:d,obj:i,tipo:"item"}); (d.bench||[]).forEach((b,n)=>lookup[`e${d.data}-b${n}`]={day:d,obj:b,tipo:"bench"}); });
  const n = lerNome(); if (n) await entrar(n); else $("login").hidden=false;
}
async function entrar(nome){
  me = nome; isAdmin = nome === "Bru";
  $("me").innerHTML = `Você: <b>${esc(nome)}</b>`; $("sair").hidden=false;
  $("login").hidden=true; $("app").hidden=false;
  montar(); await carregar(); assinar(); setInterval(carregar, 30000); bcInit();
}
function montar(){
  $("grid").innerHTML = AREAS.map(([k,l,sub]) => `
    <section class="bs-col a-${k}" data-a="${k}">
      <h2 data-exp="${k}"><span>${esc(l)}<em id="n-${k}"></em></span><small>${esc(sub)} e conversa direta · <span id="exp-${k}">abrir em cima</span></small></h2>
      <div class="bs-feed" id="feed-${k}"></div>
      <form class="bs-form" data-a="${k}"><textarea rows="2" placeholder="Escreva pra mesa de ${esc(l)}"></textarea><div class="row"><span class="hint">assina como ${esc(me)}</span><button class="btn sm" type="submit">Enviar</button></div></form>
    </section>`).join("");
  $("grid").addEventListener("click", e => {
    const h=e.target.closest("h2[data-exp]"); if(!h) return;
    expandida = expandida===h.dataset.exp ? "" : h.dataset.exp;
    document.querySelectorAll(".bs-col").forEach(c => { const on = c.dataset.a===expandida; c.classList.toggle("expand", on); $("exp-"+c.dataset.a).textContent = on ? "recolher" : "abrir em cima"; });
    if (expandida) window.scrollTo({top: $("grid").offsetTop - 12, behavior:"smooth"});
  });
  $("grid").addEventListener("submit", async e => {
    e.preventDefault(); const f=e.target; const ta=f.querySelector("textarea"); const txt=ta.value.trim(); if(!txt) return;
    const btn=f.querySelector("button"); btn.disabled=true;
    const edicao = (RADAR.dias && RADAR.dias[0]) ? RADAR.dias[0].data : null;
    const { error } = await sb.from("brainstorm").insert({area:f.dataset.a, autor:me, texto:txt, edicao});
    btn.disabled=false; if (error) { note("Não deu pra enviar: " + (error.message||"erro")); return; }
    ta.value=""; await carregar();
  });
  $("grid").addEventListener("click", async e => {
    const enc=e.target.closest(".bs-enc"); if (enc){ verEnc[enc.dataset.enc]=!verEnc[enc.dataset.enc]; render(); return; }
    const st=e.target.closest(".st button"); if (st){
      const msg=st.closest(".bs-msg"); const tab=msg.dataset.tabela, id=msg.dataset.id, novo=st.dataset.st;
      const agora=new Date().toISOString();
      const patch = tab==="brainstorm" ? {status:novo, status_por:me, status_t:agora} : tab==="ideias" ? {status:IDST_BACK[novo]||"avaliando", status_por:me, status_t:agora} : {bs_status:novo, bs_status_por:me, bs_status_t:agora};
      const { error } = await sb.from(tab).update(patch).eq(tab==="ideias"?"chave":"id", id);
      if (error) note("Não deu pra mudar o estado: " + (error.message||"erro")); else await carregar();
      return; }
    const bc=e.target.closest(".bc"); if (bc){
      const msg=bc.closest(".bs-msg"); const tab=msg.dataset.tabela, id=msg.dataset.id, area=msg.closest(".bs-col").dataset.a;
      const cfg = bcListas[area]; if (!cfg || !cfg.todolist_id){ note("A mesa de " + area + " ainda não está ligada a uma lista do Basecamp. Escolha no quadro Basecamp, no topo."); window.scrollTo({top:0,behavior:"smooth"}); return; }
      const texto = msg.dataset.texto||""; const autor = msg.dataset.autor||""; const edicao = msg.dataset.edicao||"";
      const content = texto.length>ASSUNTO_MAX ? texto.slice(0,ASSUNTO_MAX-1).trimEnd()+"…" : texto;
      const description = `<div>${esc(texto)}</div><div><br></div><div>Origem: Brainstorm do Bench News, mesa ${esc(area)}${edicao?", edição "+fmtShort(edicao):""}, por ${esc(autor)}. <a href="${esc(location.href)}">Abrir o brainstorm</a></div>`;
      bc.disabled=true; bc.textContent="Criando...";
      try {
        const r = await fetch(FN + "/todo", {method:"POST", headers:{"Content-Type":"application/json","apikey":SB_KEY}, body: JSON.stringify({area, content, description, tabela:tab, id, por:me})});
        const j = await r.json();
        if (!r.ok || j.error) throw new Error(j.error || ("erro " + r.status));
        note(""); await carregar();
      } catch(err){ note("Não deu pra criar no Basecamp: " + err.message); bc.disabled=false; bc.textContent="Levar pro Basecamp"; }
      return; }
    const b=e.target.closest(".apagar"); if(!b) return;
    const { error } = await sb.from("brainstorm").delete().eq("id", b.dataset.id);
    if (error) note("Não deu pra apagar: " + (error.message||"erro")); else await carregar();
  });
  $("grid").addEventListener("keydown", e => { if (e.key==="Enter" && (e.metaKey||e.ctrlKey) && e.target.tagName==="TEXTAREA") e.target.form.requestSubmit(); });
}
async function carregar(){
  const [b,c,l,i] = await Promise.all([sb.from("brainstorm").select("*").order("t"), sb.from("comentarios").select("*").order("t"), sb.from("basecamp_listas").select("*"), sb.from("ideias").select("*")]);
  if (b.data) data.brainstorm=b.data; if (c.data) data.comentarios=c.data; if (i.data) data.ideias=i.data;
  if (l.data) l.data.forEach(x => bcListas[x.area]=x);
  render();
}
function areaDoComentario(c){
  const L = lookup[c.chave]; if (!L) return null;
  const paras = L.tipo==="item" ? (L.obj.para||[]) : [String(L.obj.area||"").toLowerCase()];
  for (const p of paras){ const a = PARA2AREA[String(p).toLowerCase()]; if (a) return a; }
  return null;
}
function render(){
  const por = {vendas:[],membership:[],parcerias:[],marketing:[]};
  data.comentarios.forEach(c => { if (c.tipo==="claude") return; const a=areaDoComentario(c); if(!a) return; const L=lookup[c.chave];
    por[a].push({id:c.id, tabela:"comentarios", autor:c.email, texto:c.texto, t:c.t, edicao:L.day.data, status:c.bs_status||"aberta", basecamp:c.bs_basecamp_t, basecampUrl:c.bs_basecamp_url, ref:{titulo: L.tipo==="item"?L.obj.title:L.obj.ideia, url: L.tipo==="item"?L.obj.url:null}, origem:"sala"}); });
  data.ideias.forEach(s => { if (!s.status || s.status==="nova") return; const L=lookup[s.chave]; if (!L || L.tipo!=="bench") return; const a=PARA2AREA[String(L.obj.para||"").toLowerCase()]; if(!a) return;
    por[a].push({id:s.chave, tabela:"ideias", autor:s.dono, texto:L.obj.ideia, t:s.t, edicao:L.day.data, status:IDST[s.status]||"aberta", basecamp:s.basecamp_t, basecampUrl:s.basecamp_url, ref:{titulo:"ideia do Bench pro Haven, assumida no Grupo de Discussão da sala", url:L.obj.url||null}, origem:"ideia"}); });
  data.brainstorm.forEach(m => por[m.area].push({id:m.id, tabela:"brainstorm", autor:m.autor, texto:m.texto, t:m.t, edicao:m.edicao, status:m.status||"aberta", basecamp:m.basecamp_t, basecampUrl:m.basecamp_url, origem:"mesa"}));
  const msgHtml = m => {
    const enc = m.status==="finalizada"||m.status==="descartada";
    const acts = enc ? `<button data-st="aberta">reabrir</button>`
      : (m.status==="andamento" ? `<button data-st="finalizada">finalizar</button><button data-st="descartada">desprezar</button><button data-st="aberta">voltar pra aberta</button>`
                                : `<button data-st="andamento">em andamento</button><button data-st="finalizada">finalizar</button><button data-st="descartada">desprezar</button>`);
    return `<div class="bs-msg ${m.autor===me?'mine':''} st-${m.status} ${enc?'encerrada':''}" data-id="${esc(m.id)}" data-tabela="${m.tabela}" data-texto="${esc(m.texto)}" data-autor="${esc(m.autor||"")}" data-edicao="${esc(m.edicao||"")}">
      <div class="who"><b>${esc(m.autor||"Alguém do time")}</b><span>${m.edicao?"edição "+fmtShort(m.edicao):""}</span><span>${fmtTs(m.t)}</span>${m.status!=="aberta"?`<span class="pill ${esc(m.status)}">${esc(ST[m.status])}</span>`:""}${m.basecamp?(m.basecampUrl?`<a class="pill basecamp" href="${esc(m.basecampUrl)}" target="_blank" rel="noopener">no Basecamp ↗</a>`:`<span class="pill basecamp">no Basecamp</span>`):""}${m.origem==="mesa"&&(m.autor===me||isAdmin)?`<button class="apagar" data-id="${esc(m.id)}">apagar</button>`:""}</div><span class="txt">${esc(m.texto)}</span>${m.ref?`<span class="ref">sobre: ${m.ref.url?`<a href="${esc(m.ref.url)}" target="_blank" rel="noopener">${esc(m.ref.titulo)}</a>`:esc(m.ref.titulo)}</span>`:""}${respDe(m)}
      <div class="st">${acts}${enc?"":`<button class="bc" type="button">${m.basecamp?"Reenviar pro Basecamp":"Levar pro Basecamp"}</button>`}</div>
    </div>`; };
  for (const k of Object.keys(por)){
    const lista = por[k].sort((x,y)=>new Date(x.t)-new Date(y.t));
    const abertas = lista.filter(m=>m.status==="aberta"||m.status==="andamento");
    const encerradas = lista.filter(m=>m.status==="finalizada"||m.status==="descartada");
    const n=$("n-"+k); if(n) n.textContent = abertas.length ? abertas.length+" em aberto" : "";
    const feed=$("feed-"+k); const atBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 60;
    let h = "";
    if (encerradas.length) h += `<button class="bs-enc" data-enc="${k}">${verEnc[k]?"esconder":"ver"} encerradas (${encerradas.length})</button>`;
    if (verEnc[k]) h += encerradas.map(msgHtml).join("");
    h += abertas.length ? abertas.map(msgHtml).join("") : `<div class="bs-vazio">${encerradas.length?"Nada em aberto nesta mesa.":"Mesa vazia. Comece a conversa."}</div>`;
    feed.innerHTML = h;
    if (atBottom || !feed.dataset.init) { feed.scrollTop = feed.scrollHeight; feed.dataset.init="1"; }
  }
}
async function bcInit(){
  const box=$("bc-box"), txt=$("bc-txt"), grid=$("bc-grid");
  try { bcStatus = await (await fetch(FN + "/status", {headers:{"apikey":SB_KEY}})).json(); } catch(e){ bcStatus = null; }
  box.hidden=false;
  if (!bcStatus || !bcStatus.client_configured){ txt.innerHTML = "Integração ainda não configurada. Falta registrar a integração no Basecamp e guardar as chaves no Supabase."; return; }
  if (!bcStatus.connected){ txt.innerHTML = `Basecamp ainda não autorizado. <a href="${esc(FN)}/authorize" style="text-decoration:underline">Autorizar com a conta do Haven</a> (uma vez, por quem administra).`; return; }
  const ligadas = AREAS.filter(([k])=>bcListas[k]&&bcListas[k].todolist_id).length;
  const resumo = AREAS.filter(([k])=>bcListas[k]&&bcListas[k].todolist_id).map(([k,l])=>`${esc(l)} → <b>${esc(bcListas[k].projeto||"")}</b>`).join(" · ");
  txt.innerHTML = `Conectado ao Basecamp. ${ligadas===4?`<span class="ok">Cada mesa leva pra lista "Brainstorm Bench News" do seu projeto:</span> ${resumo}.`:`${ligadas} de 4 mesas ligadas a listas.`} <button class="btn sm ghost" id="bc-cfg" type="button">${ligadas===4?"Mudar listas":"Escolher listas"}</button>`;
  $("bc-cfg").addEventListener("click", async () => {
    $("bc-cfg").disabled=true; $("bc-cfg").textContent="Carregando projetos...";
    try { bcProjects = (await (await fetch(FN + "/projects", {headers:{"apikey":SB_KEY}})).json()).projects || []; } catch(e){ note("Não consegui listar os projetos do Basecamp."); $("bc-cfg").disabled=false; return; }
    const opts = (sel) => `<option value="">Escolher lista</option>` + bcProjects.map(p => `<optgroup label="${esc(p.name)}">${p.lists.map(l => `<option value="${p.id}|${l.id}" ${sel&&sel.todolist_id==l.id?"selected":""}>${esc(l.name)}</option>`).join("")}</optgroup>`).join("");
    grid.hidden=false; grid.innerHTML = AREAS.map(([k,l]) => `<div><label>Mesa de ${esc(l)}</label><select data-area="${k}">${opts(bcListas[k])}</select></div>`).join("");
    $("bc-cfg").disabled=false; $("bc-cfg").textContent="Listas carregadas";
  });
  grid.addEventListener("change", async e => {
    const sel=e.target; if(!sel.dataset.area || !sel.value) return;
    const [bucket_id, todolist_id] = sel.value.split("|").map(Number);
    const p = bcProjects.find(x=>x.id===bucket_id); const l = p && p.lists.find(x=>x.id===todolist_id);
    const r = await fetch(FN + "/config", {method:"POST", headers:{"Content-Type":"application/json","apikey":SB_KEY}, body: JSON.stringify({area:sel.dataset.area, bucket_id, todolist_id, projeto:p?p.name:"", lista:l?l.name:""})});
    const j = await r.json(); if (!r.ok || j.error) { note("Não deu pra salvar: " + (j.error||r.status)); return; }
    await carregar(); bcInit();
  });
}
function assinar(){
  const ch = sb.channel("brainstorm-live")
    .on("postgres_changes", {event:"*", schema:"public", table:"brainstorm"}, () => carregar())
    .on("postgres_changes", {event:"*", schema:"public", table:"comentarios"}, () => carregar())
    .on("postgres_changes", {event:"*", schema:"public", table:"ideias"}, () => carregar())
    .subscribe(st => { const ok = st==="SUBSCRIBED"; $("live").classList.toggle("on", ok); $("live-txt").textContent = ok ? "ao vivo" : (st==="CHANNEL_ERROR"||st==="TIMED_OUT" ? "atualizando a cada 30s" : "conectando"); });
}
boot();
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__CSS__", css + extra).replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY)
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
open(dest, "w", encoding="utf-8").write(html)
print("brainstorm gerado:", dest, len(html), "bytes")
