#!/usr/bin/env python3
"""Daily Haven Bench News v2: home e sala com a mesma diagramação de jornal, UX revista.
Lê o radar-data.json do GitHub Pages ao abrir (não precisa regerar a cada edição).
  home: python3 build_v2.py home destino
  sala: python3 build_v2.py sala SUPABASE_URL SUPABASE_ANON_KEY destino
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3:
    print(__doc__); sys.exit(1)
OFICIAL = "oficial" in sys.argv          # caminhos oficiais (/benchnews/ e /benchnews/sala/) em vez de /v2/
args = [a for a in sys.argv[1:] if a != "oficial"]
MODE = args[0]
if MODE == "home":
    SB_URL, SB_KEY, dest = "", "", args[1]
else:
    SB_URL, SB_KEY, dest = args[1], args[2], args[3]
UP = "../" if OFICIAL else "../../"       # da sala até /benchnews/
SALA_LINK = "sala/" if OFICIAL else "../sala/v2/"

site = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", site, re.S).group(1)
sala = open(os.path.join(HERE, "build_sala.py"), encoding="utf-8").read()
extra = re.search(r'EXTRA_CSS = r"""(.*?)"""', sala, re.S).group(1)

V2 = r"""
  /* ===== v2 ===== */
  .page{max-width:1240px}
  .mast h1{margin:6px 0 8px}
  @media(min-width:1100px){.mast h1{font-size:68px}}

  /* régua fixa */
  .bar{position:sticky;top:0;z-index:20;background:var(--ivory);border-bottom:1px solid var(--rule-strong);display:flex;align-items:center;gap:18px;padding:8px 0;flex-wrap:nowrap;font-family:var(--sans);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--soft)}
  .bar .ed{display:flex;align-items:center;gap:8px;white-space:nowrap;flex:none}
  .bar .ed select{font:inherit;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);background:transparent;border:0;border-bottom:1px solid var(--ink);padding:1px 18px 1px 0;cursor:pointer;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path d='M1 1l4 4 4-4' fill='none' stroke='%232B2622' stroke-width='1.2'/></svg>");background-repeat:no-repeat;background-position:right 2px center}
  .bar .jump{display:flex;gap:16px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1 1 auto;min-width:0}
  .bar .jump::-webkit-scrollbar{display:none}
  .bar .jump a{white-space:nowrap;padding:4px 0;border-bottom:2px solid transparent;color:var(--soft)}
  .bar .jump a.on,.bar .jump a:hover{color:var(--ink);border-bottom-color:var(--terracotta)}
  .bar .jump a.bs{color:var(--teal);font-weight:700;border-bottom-color:transparent}
  .bar .jump a.bs:hover{border-bottom-color:var(--teal)}
  .bar .jump a em{font-style:normal;color:var(--mute);margin-left:4px;font-size:10px}
  .bar .who{display:flex;align-items:center;gap:10px;flex:none;white-space:nowrap}
  .bar .who b{color:var(--ink)}
  .bar .btn.sm{padding:5px 9px;font-size:9.5px}
  .live{display:inline-flex;align-items:center;gap:6px;color:var(--mute)}
  .live i{width:7px;height:7px;border-radius:50%;background:var(--sand);display:inline-block}
  .live.on i{background:var(--forest)}
  @media(max-width:759px){.bar{gap:12px;padding:7px 0;font-size:10.5px}.bar .num{display:none}.bar .who .me{display:none}}

  /* filtros em uma linha */
  .chips{display:flex;align-items:center;gap:6px;padding:10px 0;border-bottom:1px solid var(--rule);overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}
  .chips::-webkit-scrollbar{display:none}
  .chips [data-f]{display:flex;gap:4px;flex:none;align-items:center}
  @media(min-width:960px){.chips{flex-wrap:wrap;row-gap:8px;overflow:visible}.chips .n{margin-left:auto}}
  .chips .lbl{font-family:var(--sans);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--terracotta);font-weight:700;margin:0 4px 0 14px;flex:none}
  .chips .lbl:first-child{margin-left:0}
  .chips button{font-family:var(--serif2);font-size:16px;font-weight:500;background:transparent;border:1px solid transparent;border-radius:14px;color:var(--soft);cursor:pointer;padding:3px 10px;line-height:1.2;white-space:nowrap;flex:none}
  .chips button:hover{color:var(--ink);border-color:var(--rule)}
  .chips button.on{color:var(--paper);background:var(--espresso);border-color:var(--espresso)}
  .chips .n{margin-left:auto;padding-left:14px;font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);white-space:nowrap;flex:none}
  .chips .limpar{font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--terracotta);background:none;border:0;cursor:pointer;flex:none;text-decoration:underline;text-underline-offset:3px;padding:0 0 0 10px}

  /* abertura */
  .open{padding:28px 0 30px}
  @media(min-width:960px){.open{padding:36px 0 38px;gap:48px}}
  .open .editorial{max-width:62ch;font-size:19.5px}
  .open .manchete{max-width:20ch}
  .watch li{font-size:17px;padding:13px 0}

  /* bench em três colunas */
  .bench ol{gap:0 36px}
  @media(min-width:900px){.bench ol{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(min-width:1100px){.bench ol{grid-template-columns:repeat(3,minmax(0,1fr))}}
  .bench li{grid-template-columns:1fr;gap:0;padding:16px 0 18px}
  .bench li .k{display:none}
  .bench li b{display:flex;gap:8px;align-items:baseline;margin-bottom:6px}
  .bench li b:before{content:attr(data-n);font-weight:400;color:var(--mute);letter-spacing:.1em}
  .bench li p{font-size:17px}
  .bench li p strong{font-family:var(--serif);font-weight:500;font-size:19px;line-height:1.25;display:block;margin-bottom:4px;color:var(--ink)}
  .bench li .ref{margin-top:8px;font-size:10px}

  /* mural: cartão de estrutura fixa */
  .sec{margin-top:30px;scroll-margin-top:60px}
  .bench,.open{scroll-margin-top:60px}
  .art{gap:10px;padding-bottom:26px}
  .art h3{font-size:23px;line-height:1.2}
  .art:not(.aberto) .txt{display:-webkit-box;-webkit-box-orient:vertical;overflow:hidden;-webkit-line-clamp:4}
  .art .txt{font-size:17px}
  .art .use{background:var(--paper);border-left:3px solid var(--terracotta);padding:10px 12px 10px 14px;font-size:16.5px}
  .art .use i{font-size:10px}
  .art .mais{font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--terracotta);background:none;border:0;cursor:pointer;padding:0;align-self:flex-start;text-decoration:underline;text-underline-offset:3px}
  .art .foot{flex-direction:row;flex-wrap:wrap;gap:4px 10px;font-size:10.5px;letter-spacing:.08em}
  .art .foot span+span:before{content:"·";margin-right:10px;color:var(--mute)}
  .tag em.time{font-style:normal;color:var(--teal);margin-left:10px;letter-spacing:.14em;font-weight:600}
  .brief h3{font-size:19px}

  /* faixa ao vivo (sala) */
  .strip{display:flex;align-items:stretch;gap:0;border-bottom:1px solid var(--rule-strong);background:var(--paper);margin-top:0}
  .strip button,.strip a{flex:1 1 0;font-family:var(--sans);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft);background:none;border:0;border-right:1px solid var(--rule);padding:12px 10px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
  .strip a:last-child,.strip button:last-child{border-right:0}
  .strip em{font-family:var(--serif);font-style:italic;font-weight:500;font-size:22px;line-height:1;color:var(--ink);text-transform:none;letter-spacing:0}
  .strip em.zero{color:var(--mute)}
  .strip .on{background:var(--ivory);color:var(--ink);box-shadow:inset 0 -3px 0 var(--terracotta)}
  .strip a em{color:var(--teal)}
  .painel{display:none;padding:18px 0 20px;border-bottom:1px solid var(--rule-strong)}
  .painel.on{display:block}
  .painel .box h2{font-size:22px;border-bottom-width:2px}
  .painel .box{max-width:78ch}
  .painel .box li{font-size:16.5px}
  .painel .form textarea{min-height:48px}
  .painel .fechar{font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);background:none;border:0;cursor:pointer;padding:0;margin-top:10px;text-decoration:underline;text-underline-offset:3px}

  /* interação mais leve */
  .int{gap:6px;padding-top:8px}
  .int .vote,.int .toggle,.int select{font-size:10px;padding:4px 8px}
  .int .toggle{padding:4px 2px}
  .login{max-width:520px;margin:40px auto;padding:28px;background:var(--paper);border:1px solid var(--rule)}
  .login h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;margin-bottom:8px}
  .login p{font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--espresso);margin-bottom:14px}
  select{font-family:var(--serif2);font-size:17px;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:10px 12px;width:100%}
  .int .cm li .resp{margin-top:8px;padding:8px 0 2px 12px;border-left:2px solid var(--teal);font-size:16px}
  .int .cm li .resp i{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:4px}
  footer .sig{display:none}
  .topo{position:fixed;right:18px;bottom:18px;z-index:30;font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;background:var(--espresso);color:var(--paper);border:0;padding:8px 10px;cursor:pointer;opacity:0;pointer-events:none;transition:opacity .2s}
  .topo.on{opacity:.9;pointer-events:auto}
"""

SALA_HTML = r"""
  <div class="strip" id="strip">
    <button data-p="pautas"><em id="n-pautas">0</em>pra pauta</button>
    <button data-p="disc"><em id="n-disc">0</em>em discussão</button>
    <a href="../../brainstorm/"><em id="n-bs">0</em>brainstorm ao vivo ↗</a>
  </div>
  <section class="painel" id="p-pautas">
    <div class="box"><h2>Pra pauta</h2><p class="sub">pedidos do time pra Bru e pro radar da manhã seguinte: tema, link, dúvida de mercado</p><ul id="pautas"></ul>
      <form class="form" id="pauta-form"><textarea id="pauta-txt" rows="2" placeholder="Ex.: quero que o Bench olhe os clubes de corrida de marca em SP, com preço."></textarea><button class="btn" type="submit" id="pauta-btn">Mandar pra pauta</button></form>
      <button class="fechar" data-p="pautas">fechar</button></div>
  </section>
  <section class="painel" id="p-disc">
    <div class="box andamento"><h2>Grupo de Discussão</h2><p class="sub">ideias do Bench que alguém do time assumiu, de qualquer edição</p><ul id="andamento"></ul>
      <div class="row" style="margin-top:12px"><a class="btn" href="../../brainstorm/">Abrir o brainstorm</a><button class="fechar" data-p="disc" style="margin:0">fechar</button></div></div>
  </section>
  <details class="ajuda"><summary>como funciona a sala</summary><p>A sala é o jornal do Bench com o time dentro. Em cada item você marca <b>Serviu</b> ou <b>Não serviu</b> e deixa comentário; o que você escreve aparece pra todo mundo na hora e a Bru responde pela rotina do Bench ao longo do dia. Em cada ideia do <b>Bench pro Haven</b> dá pra mudar o status e clicar em <b>Assumir</b>: a ideia entra no <b>Grupo de Discussão</b> aqui em cima e, ao mesmo tempo, na mesa certa do <b>Brainstorm</b> (Vendas, Membership, Parcerias ou Marketing/Social), onde a conversa continua ao vivo e pode ir pro Basecamp. Comentário feito num item marcado pra uma área também cai na mesa dessa área. Em <b>Pra pauta</b> você pede um tema, um link ou uma dúvida de mercado: entra na pesquisa da manhã seguinte e a resposta aparece embaixo do pedido. Link colado em qualquer lugar da sala ou do brainstorm é aberto, conferido e publicado na edição seguinte com a marca "trazido pelo time". Seu nome fica guardado neste aparelho; pra trocar, use "Trocar nome" na régua.</p></details>
"""

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
__SBJS__
<style>__CSS__</style>
</head>
<body>
<div class="page">
  <header class="mast">
    <div class="kicker">__KICKER__</div>
    <h1>Daily Haven Bench News</h1>
    <div class="kicker">Pra parcerias, marketing, vendas e clube</div>
  </header>
  <div class="bar" id="bar">
    <span class="num" id="folio-left"></span>
    <span class="ed"><label for="day">Edição</label><select id="day" aria-label="Escolher edição"></select></span>
    <nav class="jump" id="jump" aria-label="Seções"><a href="#manchete">Manchete</a><a href="#atencao">Atenção</a><a href="#bench">Bench <em id="j-bench"></em></a><a href="#mural">Mural <em id="j-mural"></em></a>__JUMP_SALA__</nav>
    <span class="who" id="who">__WHO__</span>
  </div>
  <div class="ro" id="ro" hidden></div>
  __LOGIN__
  <div id="app" __APP_HIDDEN__>
  __SALA__
  <nav class="chips" id="chips" aria-label="Filtros">
    <span class="lbl">Pra quem</span><span data-f="para"><button class="on" data-v="">Tudo</button><button data-v="parcerias">Parcerias</button><button data-v="marketing">Marketing</button><button data-v="vendas">Vendas</button><button data-v="clube">Clube</button></span>
    <span class="lbl">Onde</span><span data-f="escopo"><button class="on" data-v="">Tudo</button><button data-v="brasil">Brasil</button><button data-v="mundo">Mundo</button></span>
    <span class="lbl">Pilar</span><span data-f="pilar"><button class="on" data-v="">Todos</button><button data-v="wellness-residence">Wellness residence</button><button data-v="membership">Membership</button><button data-v="longevidade">Longevidade</button><button data-v="comunidade">Comunidade</button><button data-v="lifestyle">Lifestyle</button><button data-v="estudos">Estudos</button><button data-v="eventos">Eventos</button><button data-v="marcas">Marcas</button></span>
    <span class="n" id="count"></span><button class="limpar" id="limpar" hidden>limpar</button>
  </nav>
  <main id="main"></main>
  </div>
  <footer>
    <p>__FOOT__</p>
  </footer>
</div>
<button class="topo" id="topo" type="button">topo ↑</button>
<script>
const SALA = __SALA_FLAG__;
const SB_URL = "__SB_URL__", SB_KEY = "__SB_KEY__";
const RADAR_URL = "https://brusna-infurna.github.io/daily-haven-bench-news/radar-data.json";
const sb = SALA ? supabase.createClient(SB_URL, SB_KEY) : null;
const PILAR = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade","estudos":"Estudos","eventos":"Eventos","marcas":"Marcas"};
const STATUS = {nova:"Nova",avaliando:"Avaliando",andamento:"Em andamento",feita:"Feita",descartada:"Descartada"};
const PARA2AREA = {vendas:"vendas", clube:"membership", parcerias:"parcerias", marketing:"marketing"};
const M=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const W=["dom","seg","ter","qua","qui","sex","sáb"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtBar = d => { const [y,m,dd]=d.split("-").map(Number); const w=new Date(Date.UTC(y,m-1,dd)).getUTCDay(); return `${W[w]} ${dd} ${MS[m-1]}`; };
const fmtSel = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]} ${y}`; };
const fmtShort = d => { const [y,m,dd]=String(d).slice(0,10).split("-"); return `${+dd} ${MS[+m-1]}`; };
const fmtTs = t => { const d=new Date(t); return isNaN(d)?"":`${d.getDate()} ${MS[d.getMonth()]} ${String(d.getHours()).padStart(2,"0")}h${String(d.getMinutes()).padStart(2,"0")}`; };
const $ = id => document.getElementById(id);
function note(msg){ const ro=$("ro"); ro.hidden=!msg; ro.innerHTML = msg ? `<b>Aviso.</b> ${esc(msg)}` : ""; }

let RADAR = {dias:[]};
const state = {day:"", escopo:"", pilar:"", para:""};
const shared = {votos:[], comentarios:[], pautas:[], ideias:{}, membros:{}, brainstorm:[]};
let me = null, meEmail = "", isAdmin = false;
const opened = new Set(), abertos = new Set();
const lookup = {};
const keyItem = (day,n) => `e${day.data}-i${n}`;
const keyBench = (day,n) => `e${day.data}-b${n}`;
const nameOf = e => (shared.membros[String(e||"").toLowerCase()]) || (e && !String(e).includes("@") ? String(e) : "Alguém do time");

/* identidade (sala) */
const NOME_KEY = "benchnews-sala-nome";
const lerNome = () => { try { return (localStorage.getItem(NOME_KEY)||"").trim(); } catch(e){ return ""; } };
const guardarNome = n => { try { localStorage.setItem(NOME_KEY, n); } catch(e){} };
if (SALA){
  $("login-nome").addEventListener("change", e => { $("login-outro").hidden = e.target.value !== "__outro"; if (!$("login-outro").hidden) $("login-outro").focus(); });
  $("login-form").addEventListener("submit", e => { e.preventDefault(); let n = $("login-nome").value; if (n === "__outro") n = $("login-outro").value; n = (n||"").trim().replace(/\s+/g," ").slice(0,40); if (!n) { $("login-note").textContent = "Escolha ou digite um nome."; return; } guardarNome(n); entrar(n); });
  $("sair").addEventListener("click", () => { try { localStorage.removeItem(NOME_KEY); } catch(e){} location.reload(); });
}

async function boot(){
  try { RADAR = await (await fetch(RADAR_URL, {cache:"no-store"})).json(); } catch(e){ note("Não consegui carregar as edições agora. Tente de novo em instantes."); return; }
  state.day = RADAR.dias[0].data;
  RADAR.dias.forEach(d => { (d.itens||[]).forEach((i,n)=>lookup[keyItem(d,n)]={tipo:"item",day:d,obj:i}); (d.bench||[]).forEach((b,n)=>lookup[keyBench(d,n)]={tipo:"bench",day:d,obj:b}); });
  const sel = $("day"); sel.innerHTML="";
  RADAR.dias.forEach(d => { const o=document.createElement("option"); o.value=d.data; o.textContent=fmtSel(d.data); sel.appendChild(o); });
  sel.addEventListener("change", e => { state.day=e.target.value; abertos.clear(); render(); });
  document.querySelectorAll("#chips [data-f]").forEach(g => g.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    g.querySelectorAll("button").forEach(x=>x.classList.remove("on")); b.classList.add("on"); state[g.dataset.f]=b.dataset.v; render();
  })));
  $("limpar").addEventListener("click", () => { state.escopo=state.pilar=state.para=""; document.querySelectorAll("#chips [data-f]").forEach(g => g.querySelectorAll("button").forEach((x,i)=>x.classList.toggle("on", i===0))); render(); });
  $("main").addEventListener("click", e => { const b=e.target.closest(".mais"); if(!b) return; const a=b.closest("article"); const k=a.dataset.k; abertos.has(k)?abertos.delete(k):abertos.add(k); a.classList.toggle("aberto"); b.textContent = a.classList.contains("aberto") ? "fechar" : "ler tudo"; });
  $("topo").addEventListener("click", () => window.scrollTo({top:0,behavior:"smooth"}));
  window.addEventListener("scroll", () => { $("topo").classList.toggle("on", window.scrollY > 900); marcarSecao(); }, {passive:true});
  if (SALA){
    try { const m = await sb.from("membros").select("email,nome"); (m.data||[]).forEach(x => { if (x.email && x.nome) shared.membros[String(x.email).toLowerCase()] = x.nome; }); } catch(e){}
    const n = lerNome(); if (n) await entrar(n); else { $("login").hidden=false; }
  } else render();
}
function marcarSecao(){
  const links=[...document.querySelectorAll("#jump a[href^='#']")]; let cur=null;
  for (const a of links){ const el=document.querySelector(a.getAttribute("href")); if (el && el.getBoundingClientRect().top <= 80) cur=a; }
  links.forEach(a=>a.classList.toggle("on", a===cur));
}
async function entrar(nome){
  me = {nome}; meEmail = nome; isAdmin = nome === "Bru";
  $("me").innerHTML = `Você: <b>${esc(nome)}</b>`; $("sair").hidden=false;
  $("login").hidden=true; $("app").hidden=false;
  $("strip").addEventListener("click", e => { const b=e.target.closest("button[data-p]"); if(!b) return; togglePainel(b.dataset.p); });
  document.querySelectorAll(".painel .fechar").forEach(b => b.addEventListener("click", () => togglePainel(b.dataset.p, false)));
  await carregar(); setInterval(carregar, 60000); assinar();
}
function togglePainel(p, force){
  const on = force!==undefined ? force : !$("p-"+p).classList.contains("on");
  document.querySelectorAll(".painel").forEach(x=>x.classList.remove("on")); document.querySelectorAll("#strip button").forEach(x=>x.classList.remove("on"));
  if (on){ $("p-"+p).classList.add("on"); document.querySelector(`#strip button[data-p=${p}]`).classList.add("on"); }
}
async function carregar(){
  const [v,c,p,i,b] = await Promise.all([sb.from("votos").select("*"), sb.from("comentarios").select("*").order("t"), sb.from("pautas").select("*").order("t",{ascending:false}), sb.from("ideias").select("*"), sb.from("brainstorm").select("id,status")]);
  if (v.data) shared.votos=v.data; if (c.data) shared.comentarios=c.data; if (p.data) shared.pautas=p.data; if (b.data) shared.brainstorm=b.data;
  if (i.data){ shared.ideias={}; i.data.forEach(x=>shared.ideias[x.chave]=x); }
  render();
}
function assinar(){
  sb.channel("sala-live").on("postgres_changes",{event:"*",schema:"public",table:"brainstorm"},()=>carregar()).on("postgres_changes",{event:"*",schema:"public",table:"comentarios"},()=>carregar()).on("postgres_changes",{event:"*",schema:"public",table:"pautas"},()=>carregar()).on("postgres_changes",{event:"*",schema:"public",table:"ideias"},()=>carregar())
    .subscribe(st => { const ok = st==="SUBSCRIBED"; $("live").classList.toggle("on", ok); $("live-txt").textContent = ok ? "ao vivo" : "a cada 60s"; });
}
function votesFor(key){ const out={sim:0,nao:0,mine:null}; for (const v of shared.votos) if (v.chave===key){ if(v.v==="sim")out.sim++; else out.nao++; if(v.email===meEmail)out.mine=v.v; } return out; }
function commentsFor(key){ return shared.comentarios.filter(c=>c.chave===key); }
function intHtml(key, isBench){
  if (!SALA) return "";
  const v = votesFor(key), cs = commentsFor(key); const st = shared.ideias[key] || {}; const status = st.status || "nova";
  let h = `<div class="int" data-key="${esc(key)}"><div class="acts">`;
  if (isBench) {
    h += `<select data-act="status" aria-label="Status da ideia">${Object.entries(STATUS).map(([k,l])=>`<option value="${k}" ${k===status?"selected":""}>${l}</option>`).join("")}</select>`;
    if (st.dono) h += `<span class="pill ${esc(status)}">${esc(nameOf(st.dono))}</span>`; else h += `<button class="vote" data-act="assumir">Assumir</button>`;
  } else {
    h += `<button class="vote ${v.mine==="sim"?"on":""}" data-act="sim">Serviu<em>${v.sim}</em></button><button class="vote ${v.mine==="nao"?"on":""}" data-act="nao">Não serviu<em>${v.nao}</em></button>`;
  }
  h += `<button class="toggle" data-act="toggle">${opened.has(key)?"Fechar":"Comentar"}${cs.length?` (${cs.length})`:""}</button></div>`;
  if (opened.has(key)) {
    const RC = RADAR.respostas_comentarios || {};
    h += `<ul class="cm">${cs.map(c=>{ const r = RC[c.id]; return `<li class="${c.tipo==="claude"?"claude":""}">${esc(c.texto)}<div class="who"><b>${esc(nameOf(c.email))}</b> ${fmtTs(c.t)}${(c.email===meEmail||isAdmin)?` · <button class="toggle" data-act="apagar" data-id="${esc(c.id)}">apagar</button>`:""}</div>${r?`<div class="resp"><i>Resposta da Bru, via Bench</i>${esc(r.resposta)}</div>`:""}</li>`; }).join("")}</ul>`;
    h += `<form class="form" data-act="comment"><textarea rows="2" placeholder="Comentário pro time"></textarea><div class="row"><button class="btn sm" type="submit">Publicar</button></div></form>`;
  }
  return h + `</div>`;
}
const tagHtml = i => `<div class="tag">${esc(PILAR[i.pilar]||i.pilar)}${i.origem==="time"?`<em class="time">trazido pelo time</em>`:""}<span>${i.escopo==="brasil"?"Brasil":"Mundo"} · ${esc(i.region||"")}</span></div>`;
const artHtml = (i,key) => `<article class="art p-${esc(i.pilar)} ${abertos.has(key)?"aberto":""}" data-k="${esc(key)}">${tagHtml(i)}<h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3><p class="txt">${esc(i.resumo)}</p><button class="mais" type="button">${abertos.has(key)?"fechar":"ler tudo"}</button><div class="use"><i>O que o Haven faz com isso</i>${esc(i.por_que_importa)}</div><div class="foot"><span><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a></span><span>${fmtShort(i.date)}</span><span>${(i.para||[]).map(esc).join(" · ")}</span></div>${intHtml(key,false)}</article>`;
const briefHtml = (i,key) => `<article class="brief p-${esc(i.pilar)}" data-k="${esc(key)}">${tagHtml(i)}<h3><a href="${esc(i.url)}" target="_blank" rel="noopener" title="${esc(i.title)}">${esc(i.title)}</a></h3><p class="use">${esc(i.por_que_importa)}</p><div class="foot"><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)} · ${(i.para||[]).map(esc).join(" · ")}</div>${intHtml(key,false)}</article>`;
const benchHtml = (b,n,key) => `<li><span class="k"></span><div><b data-n="${String(n).padStart(2,"0")}">${esc(b.area||b.para||"")}</b><p>${b.titulo?`<strong>${esc(b.titulo)}</strong>`:""}${esc(b.ideia)}</p>${b.ref?`<div class="ref"><i>A partir de</i>${b.url?`<a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.ref)}</a>`:esc(b.ref)}</div>`:""}${intHtml(key,true)}</div></li>`;
const splitWatch = a => { const m = String(a).match(/^([^:]{2,24}):\s*(.*)$/s); return m ? `<span><b>${esc(m[1])}</b>${esc(m[2])}</span>` : `<span>${esc(a)}</span>`; };

function render(){
  const idx = RADAR.dias.findIndex(d=>d.data===state.day); const day = RADAR.dias[idx] || RADAR.dias[0]; if(!day) return;
  const num = RADAR.dias.length - (idx<0?0:idx); const items = day.itens || []; const br=items.filter(i=>i.escopo==="brasil").length;
  $("folio-left").textContent = `Nº ${num} · ${fmtBar(day.data)}`;
  const keyed = items.map((i,n)=>({i,key:keyItem(day,n)}));
  const list = keyed.filter(({i}) => (!state.escopo||i.escopo===state.escopo) && (!state.pilar||i.pilar===state.pilar) && (!state.para||(i.para||[]).includes(state.para)));
  const unfiltered = !state.escopo && !state.pilar && !state.para;
  $("count").textContent = unfiltered ? `${items.length} itens · ${br} Brasil · ${items.length-br} mundo` : `${list.length} de ${items.length}`;
  $("limpar").hidden = unfiltered;
  const leads = list.filter(x=>x.i.destaque), rest = list.filter(x=>!x.i.destaque);
  const restBr = rest.filter(x=>x.i.escopo==="brasil"), restWd = rest.filter(x=>x.i.escopo==="mundo");
  let html = "";
  if (unfiltered) html += `<section class="open" id="manchete"><div><h2 class="manchete">${esc(day.manchete||"")}</h2><p class="editorial">${esc(day.editorial||"")}</p><div class="tally">${items.length} itens conferidos na fonte · ${br} do Brasil · ${items.length-br} do mundo</div></div><aside class="watch" id="atencao"><h2>Pra prestar atenção</h2><ol>${(day.atencao||[]).map(a=>`<li>${splitWatch(a)}</li>`).join("")}</ol></aside></section>`;
  const bench = (day.bench||[]).map((b,n)=>({b,n,key:keyBench(day,n)})).filter(x => !state.para || x.b.para===state.para);
  $("j-bench").textContent = bench.length || "";
  if (bench.length && !state.escopo && !state.pilar) html += `<section class="bench" id="bench"><div class="head"><h2>Bench pro Haven</h2><span>${bench.length} ${bench.length>1?"referências aplicadas ao projeto":"referência aplicada ao projeto"}</span></div><ol>${bench.map((x,k)=>benchHtml(x.b,k+1,x.key)).join("")}</ol></section>`;
  $("j-mural").textContent = list.length || "";
  if (leads.length) html += `<div class="sec" id="mural"><h2>Mural · Destaques</h2><span>o que merece leitura inteira</span></div><div class="grid">${leads.map(x=>artHtml(x.i,x.key)).join("")}</div>`;
  if (unfiltered) {
    if (restBr.length) html += `<div class="sec" ${leads.length?"":'id="mural"'}><h2>Em pauta · Brasil</h2><span>${restBr.length} ${restBr.length>1?"itens":"item"}</span></div><div class="pauta">${restBr.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
    if (restWd.length) html += `<div class="sec"><h2>Em pauta · Mundo</h2><span>${restWd.length} ${restWd.length>1?"itens":"item"}</span></div><div class="pauta">${restWd.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
  } else if (rest.length) html += `<div class="sec" ${leads.length?"":'id="mural"'}><h2>Em pauta</h2><span>${rest.length} ${rest.length>1?"itens":"item"}</span></div><div class="pauta">${rest.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
  if (!list.length) html += `<div class="empty">Nenhum item com esses filtros. Escolha outro pilar ou volte pra tudo.</div>`;
  $("main").innerHTML = html;
  marcarSecao();
  if (!SALA) return;
  const RS = RADAR.respostas_sala || {};
  $("pautas").innerHTML = shared.pautas.length ? shared.pautas.map(p=>{ const r = RS[p.id]; const resp = (r&&r.resposta)||p.resposta; const ed = (r&&r.edicao)||p.edicao; const done = p.status==="respondida"||!!r;
    return `<li>${esc(p.texto)}<div class="who"><b>${esc(nameOf(p.email))}</b> ${fmtTs(p.t)} · ${done?"respondida na edição "+fmtShort(ed||""):"aberta"}${(p.email===meEmail||isAdmin)?` · <button class="toggle" data-act="apagar-pauta" data-id="${esc(p.id)}">apagar</button>`:""}</div>${resp?`<div class="resp"><i>Resposta da Bru</i>${esc(resp)}</div>`:""}</li>`; }).join("")
    : `<li class="vazio">Nenhuma pauta ainda. O primeiro pedido do time aparece aqui e entra no radar da manhã seguinte.</li>`;
  const ativos = Object.values(shared.ideias).filter(s=>s.status && s.status!=="nova" && lookup[s.chave]).sort((a,b)=>new Date(b.t)-new Date(a.t));
  $("andamento").innerHTML = ativos.length ? ativos.map(s=>{ const L=lookup[s.chave]; return `<li><span class="pill ${esc(s.status)}">${esc(STATUS[s.status]||s.status)}</span><div>${esc(L.obj.ideia)}<div class="who"><b>${esc(s.dono?nameOf(s.dono):"sem responsável")}</b> · ${esc(L.obj.area||"")} · edição ${fmtShort(L.day.data)}</div></div></li>`; }).join("")
    : `<li class="vazio">Nada assumido ainda. Mude o status de uma ideia do Bench ou clique em Assumir e ela aparece aqui.</li>`;
  const pAb = shared.pautas.filter(p => !(p.status==="respondida" || RS[p.id])).length;
  const bsAb = shared.brainstorm.filter(m => !m.status || m.status==="aberta" || m.status==="andamento").length
    + shared.comentarios.filter(c => { if (c.tipo==="claude") return false; const L=lookup[c.chave]; if(!L) return false; const paras = L.tipo==="item"?(L.obj.para||[]):[String(L.obj.area||"").toLowerCase()]; if (!paras.some(p=>PARA2AREA[String(p).toLowerCase()])) return false; const s=c.bs_status||"aberta"; return s==="aberta"||s==="andamento"; }).length;
  const setN = (id,n) => { const e=$(id); e.textContent=n; e.classList.toggle("zero", !n); };
  setN("n-pautas", pAb); setN("n-disc", ativos.length); setN("n-bs", bsAb);
}
async function gravar(p){ const { error } = await p; if (error) note("Não deu pra salvar agora. Tente de novo em instantes."); else { note(""); await carregar(); } }
if (SALA){
document.addEventListener("click", async e => {
  const b = e.target.closest("[data-act]"); if (!b) return; const act = b.dataset.act;
  if (act==="apagar"){ return gravar(sb.from("comentarios").delete().eq("id", b.dataset.id)); }
  if (act==="apagar-pauta"){ return gravar(sb.from("pautas").delete().eq("id", b.dataset.id)); }
  const box = b.closest(".int"); const key = box && box.dataset.key; if (!key) return;
  if (act==="toggle"){ opened.has(key)?opened.delete(key):opened.add(key); render(); return; }
  if (act==="sim"||act==="nao"){ const cur = votesFor(key).mine;
    return gravar(cur===act ? sb.from("votos").delete().match({chave:key,email:meEmail}) : sb.from("votos").upsert({chave:key,email:meEmail,v:act,t:new Date().toISOString()})); }
  if (act==="assumir"){ const prev = shared.ideias[key]||{}; return gravar(sb.from("ideias").upsert({chave:key,status:prev.status&&prev.status!=="nova"?prev.status:"avaliando",dono:meEmail,t:new Date().toISOString()})); }
});
document.addEventListener("change", async e => {
  const s = e.target.closest("select[data-act=status]"); if (!s) return; const key = s.closest(".int").dataset.key; const prev = shared.ideias[key]||{};
  gravar(sb.from("ideias").upsert({chave:key,status:s.value,dono:prev.dono||(s.value==="nova"?null:meEmail),t:new Date().toISOString()}));
});
document.addEventListener("submit", async e => {
  const f = e.target; if (f.id==="login-form") return; e.preventDefault();
  if (f.id==="pauta-form"){ const ta=$("pauta-txt"); const txt=ta.value.trim(); if(!txt) return; $("pauta-btn").disabled=true;
    await gravar(sb.from("pautas").insert({email:meEmail,texto:txt})); ta.value=""; $("pauta-btn").disabled=false; return; }
  if (f.dataset.act==="comment"){ const key=f.closest(".int").dataset.key; const ta=f.querySelector("textarea"); const txt=ta.value.trim(); if(!txt) return;
    await gravar(sb.from("comentarios").insert({chave:key,email:meEmail,texto:txt})); }
});
}
boot();
</script>
</body>
</html>
"""

LOGIN = r"""
  <section class="login" id="login" hidden>
    <h2>Quem é você?</h2>
    <p>A sala é aberta pra quem tem o link. Escolha seu nome uma vez; ele fica guardado neste aparelho e assina o que você escrever.</p>
    <form class="form" id="login-form"><select id="login-nome"><option value="">Escolher nome</option><option>Bru</option><option>Teti</option><option>Carolina</option><option>Omi</option><option>Julia</option><option>Julinha</option><option value="__outro">Outro nome</option></select><input type="text" id="login-outro" placeholder="Seu nome" maxlength="40" hidden><div class="row"><button class="btn" type="submit" id="login-btn">Entrar na sala</button></div><div class="note" id="login-note"></div></form>
  </section>
"""

is_sala = MODE == "sala"
out = (TEMPLATE
  .replace("__CSS__", css + extra + V2)
  .replace("__TITLE__", "Sala do Time · Haven Bench News" if is_sala else "Daily Haven Bench News")
  .replace("__KICKER__", "Sala do time · radar diário de wellness residences, membership, longevidade e lifestyle" if is_sala else "Radar diário de wellness residences, membership, longevidade e lifestyle")
  .replace("__SBJS__", '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>' if is_sala else "")
  .replace("__JUMP_SALA__", '<a href="../../brainstorm/" class="bs">Brainstorm ↗</a>' if is_sala else "")
  .replace("__WHO__", '<span class="live" id="live"><i></i><span id="live-txt">conectando</span></span><span class="me" id="me"></span><button class="btn sm ghost" id="sair" hidden>Trocar nome</button>' if is_sala else '<a href="__SALA_LINK__" style="text-decoration:underline">Sala do time</a>')
  .replace("__LOGIN__", LOGIN if is_sala else "")
  .replace("__APP_HIDDEN__", "hidden" if is_sala else "")
  .replace("__SALA__", SALA_HTML if is_sala else "")
  .replace("__FOOT__", 'Cada item foi aberto e conferido na fonte no dia da edição. Nesta sala, reações, comentários, status e pautas são compartilhados com todo o time e lidos pela rotina da manhã do Bench. A edição pública fica em <a href="../../" style="text-decoration:underline">benchnews</a>.' if is_sala else "Cada item foi aberto e conferido na fonte no dia da edição. Conteúdo patrocinado está marcado junto ao veículo. O radar roda toda manhã e manda um resumo por email; as edições anteriores ficam no seletor da régua.")
  .replace("__SALA_FLAG__", "true" if is_sala else "false")
  .replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY).replace("__SALA_LINK__", SALA_LINK).replace("../../", UP))
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
open(dest, "w", encoding="utf-8").write(out)
print(MODE, "v2 gerado:", dest, len(out), "bytes")
