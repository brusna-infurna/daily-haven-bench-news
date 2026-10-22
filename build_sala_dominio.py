#!/usr/bin/env python3
"""Gera a Sala do Time pra rodar no domínio próprio (www.projetorepertorio.com.br/benchnews/sala/),
com Supabase como banco. Sala aberta: quem tem o link entra e escolhe o nome. Página estática: lê o radar-data.json do GitHub Pages
ao abrir, então não precisa ser regerada a cada edição.
Uso: python3 build_sala_dominio.py SUPABASE_URL SUPABASE_ANON_KEY [destino]
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3:
    print("uso: build_sala_dominio.py SUPABASE_URL SUPABASE_ANON_KEY [destino]"); sys.exit(1)
SB_URL, SB_KEY = sys.argv[1], sys.argv[2]
dest = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "..", "sala-dominio", "index.html")

site = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", site, re.S).group(1)
sala = open(os.path.join(HERE, "build_sala.py"), encoding="utf-8").read()
extra = re.search(r'EXTRA_CSS = r"""(.*?)"""', sala, re.S).group(1)
extra += r"""
  .login{max-width:520px;margin:40px auto;padding:28px;background:var(--paper);border:1px solid var(--rule)}
  .login h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;margin-bottom:8px}
  .login p{font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--espresso);margin-bottom:14px}
  .top-actions{display:flex;gap:14px;align-items:center}
  input[type=email],input[type=password]{font-family:var(--serif2);font-size:17px;line-height:1.4;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:10px 12px;width:100%}
  .int .cm li .resp{margin-top:8px;padding:8px 0 2px 12px;border-left:2px solid var(--teal);font-size:16px}
  .int .cm li .resp i{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:4px}
"""

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Sala do Time · Haven Bench News</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.js"></script>
<style>__CSS__</style>
</head>
<body>
<div class="page">
  <header class="mast">
    <div class="kicker">Sala do time · radar diário de wellness residences, membership, longevidade e lifestyle</div>
    <h1>Daily Haven Bench News</h1>
    <div class="kicker">Pra parcerias, marketing, vendas e clube</div>
  </header>
  <div class="folio">
    <span id="folio-left"></span>
    <span><label for="day" style="margin-right:8px">Edição</label><select id="day" aria-label="Escolher edição"></select></span>
    <span id="tally"></span>
    <span class="top-actions"><span class="me" id="me"></span><button class="btn sm ghost" id="sair" hidden>Trocar nome</button></span>
  </div>
  <div class="ro" id="ro" hidden></div>

  <section class="login" id="login" hidden>
    <h2>Quem é você?</h2>
    <p>A sala é aberta pra quem tem o link. Escolha seu nome uma vez; ele fica guardado neste aparelho e assina o que você escrever.</p>
    <form class="form" id="login-form"><select id="login-nome"><option value="">Escolher nome</option><option>Bru</option><option>Teti</option><option>Carolina</option><option>Omi</option><option>Julia</option><option>Julinha</option><option value="__outro">Outro nome</option></select><input type="text" id="login-outro" placeholder="Seu nome" maxlength="40" hidden><div class="row"><button class="btn" type="submit" id="login-btn">Entrar na sala</button></div><div class="note" id="login-note"></div></form>
  </section>

  <div id="app" hidden>
  <nav class="nav" aria-label="Filtros">
    <div class="grp" data-f="para"><span class="lbl">Pra quem</span><button class="on" data-v="">Tudo</button><button data-v="parcerias">Parcerias</button><button data-v="marketing">Marketing</button><button data-v="vendas">Vendas</button><button data-v="clube">Clube</button></div>
    <div class="grp" data-f="escopo"><span class="lbl">Onde</span><button class="on" data-v="">Tudo</button><button data-v="brasil">Brasil</button><button data-v="mundo">Mundo</button></div>
    <div class="grp" data-f="pilar"><span class="lbl">Pilar</span><button class="on" data-v="">Todos</button><button data-v="wellness-residence">Wellness residence</button><button data-v="membership">Membership</button><button data-v="longevidade">Longevidade</button><button data-v="comunidade">Comunidade</button><button data-v="lifestyle">Lifestyle</button><button data-v="estudos">Estudos</button><button data-v="eventos">Eventos</button><button data-v="marcas">Marcas</button></div>
    <span class="n" id="count"></span>
  </nav>

  <section class="sala-top">
    <div class="box" id="pautas-box">
      <h2>Pra pauta</h2>
      <p class="sub">pedidos do time pra Bru e pro radar da manhã seguinte: tema, link, dúvida de mercado</p>
      <ul id="pautas"></ul>
      <form class="form" id="pauta-form">
        <textarea id="pauta-txt" rows="2" placeholder="Ex.: quero que o Bench olhe os clubes de corrida de marca em SP, com preço."></textarea>
        <button class="btn" type="submit" id="pauta-btn">Mandar pra pauta</button>
      </form>
    </div>
    <div class="box andamento" id="andamento-box">
      <h2>Grupo de Discussão</h2>
      <p class="sub">ideias do Bench que alguém do time assumiu, de qualquer edição</p>
      <ul id="andamento"></ul>
      <div class="form"><a class="btn" href="../brainstorm/" id="ver-brainstorm">Ver Brainstorm</a></div>
    </div>
  </section>

  <main id="main"></main>
  </div>

  <footer>
    <p>Cada item foi aberto e conferido na fonte no dia da edição. Nesta sala, reações, comentários, status e pautas são compartilhados com todo o time e lidos pela Bru na rotina da manhã. A edição pública fica em <a href="https://www.projetorepertorio.com.br/benchnews/" style="text-decoration:underline">projetorepertorio.com.br/benchnews</a>.</p>
    <span class="sig">Bru</span>
  </footer>
</div>
<script>
const SB_URL = "__SB_URL__", SB_KEY = "__SB_KEY__";
const RADAR_URL = "https://brusna-infurna.github.io/daily-haven-bench-news/radar-data.json";
const sb = supabase.createClient(SB_URL, SB_KEY);
const PILAR = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade","estudos":"Estudos","eventos":"Eventos","marcas":"Marcas"};
const STATUS = {nova:"Nova",avaliando:"Avaliando",andamento:"Em andamento",feita:"Feita",descartada:"Descartada"};
const M=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const W=["domingo","segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtLong = d => { const [y,m,dd]=d.split("-").map(Number); const w=new Date(Date.UTC(y,m-1,dd)).getUTCDay(); return `${W[w]}, ${dd} de ${M[m-1]} de ${y}`; };
const fmtSel = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]} ${y}`; };
const fmtShort = d => { const [y,m,dd]=String(d).slice(0,10).split("-"); return `${+dd} ${MS[+m-1]}`; };
const fmtTs = t => { const d=new Date(t); return isNaN(d)?"":`${d.getDate()} ${MS[d.getMonth()]} ${String(d.getHours()).padStart(2,"0")}h${String(d.getMinutes()).padStart(2,"0")}`; };

let RADAR = {dias:[]};
const state = {day:"", escopo:"", pilar:"", para:""};
const shared = {votos:[], comentarios:[], pautas:[], ideias:{}, membros:{}};
let me = null, meEmail = "", isAdmin = false;
const opened = new Set();
const lookup = {};
const keyItem = (day,n) => `e${day.data}-i${n}`;
const keyBench = (day,n) => `e${day.data}-b${n}`;

const $ = id => document.getElementById(id);
const nameOf = e => (shared.membros[e] && shared.membros[e].nome) || (e && !String(e).includes("@") ? String(e) : "Alguém do time");
function note(msg){ const ro=$("ro"); ro.hidden=!msg; ro.innerHTML = msg ? `<b>Aviso.</b> ${esc(msg)}` : ""; }

/* identidade por nome, guardada no aparelho */
const NOME_KEY = "benchnews-sala-nome";
const lerNome = () => { try { return (localStorage.getItem(NOME_KEY)||"").trim(); } catch(e){ return ""; } };
const guardarNome = n => { try { localStorage.setItem(NOME_KEY, n); } catch(e){} };
$("login-nome").addEventListener("change", e => { $("login-outro").hidden = e.target.value !== "__outro"; if (!$("login-outro").hidden) $("login-outro").focus(); });
$("login-form").addEventListener("submit", e => {
  e.preventDefault();
  let n = $("login-nome").value; if (n === "__outro") n = $("login-outro").value;
  n = (n||"").trim().replace(/\s+/g," ").slice(0,40);
  if (!n) { $("login-note").textContent = "Escolha ou digite um nome."; return; }
  guardarNome(n); entrar(n);
});
$("sair").addEventListener("click", () => { try { localStorage.removeItem(NOME_KEY); } catch(e){} location.reload(); });

async function boot(){
  try { RADAR = await (await fetch(RADAR_URL, {cache:"no-store"})).json(); } catch(e){ note("Não consegui carregar as edições agora. Tente de novo em instantes."); return; }
  state.day = RADAR.dias[0].data;
  RADAR.dias.forEach(d => { (d.itens||[]).forEach((i,n)=>lookup[keyItem(d,n)]={tipo:"item",day:d,obj:i}); (d.bench||[]).forEach((b,n)=>lookup[keyBench(d,n)]={tipo:"bench",day:d,obj:b}); });
  const sel = $("day"); sel.innerHTML="";
  RADAR.dias.forEach(d => { const o=document.createElement("option"); o.value=d.data; o.textContent=fmtSel(d.data); sel.appendChild(o); });
  sel.addEventListener("change", e => { state.day=e.target.value; render(); });
  document.querySelectorAll(".grp[data-f]").forEach(g => g.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
    g.querySelectorAll("button").forEach(x=>x.classList.remove("on")); b.classList.add("on"); state[g.dataset.f]=b.dataset.v; render();
  })));
  const n = lerNome();
  if (n) await entrar(n); else { $("login").hidden=false; }
}
async function entrar(nome){
  me = {nome}; meEmail = nome; isAdmin = nome === "Bru";
  $("me").innerHTML = `Você: <b>${esc(nome)}</b>`; $("sair").hidden=false;
  $("login").hidden=true; $("app").hidden=false;
  await carregar(); setInterval(carregar, 60000);
}
async function carregar(){
  const [v,c,p,i] = await Promise.all([sb.from("votos").select("*"), sb.from("comentarios").select("*").order("t"), sb.from("pautas").select("*").order("t",{ascending:false}), sb.from("ideias").select("*")]);
  if (v.data) shared.votos=v.data; if (c.data) shared.comentarios=c.data; if (p.data) shared.pautas=p.data;
  if (i.data){ shared.ideias={}; i.data.forEach(x=>shared.ideias[x.chave]=x); }
  render();
}

function votesFor(key){ const out={sim:0,nao:0,mine:null}; for (const v of shared.votos) if (v.chave===key){ if(v.v==="sim")out.sim++; else out.nao++; if(v.email===meEmail)out.mine=v.v; } return out; }
function commentsFor(key){ return shared.comentarios.filter(c=>c.chave===key); }

function intHtml(key, isBench){
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
const tagHtml = i => `<div class="tag">${esc(PILAR[i.pilar]||i.pilar)}<span>${i.escopo==="brasil"?"Brasil":"Mundo"} · ${esc(i.region||"")}</span></div>`;
const artHtml = (i,key) => `<article class="art p-${esc(i.pilar)}">${tagHtml(i)}<h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3><p class="txt">${esc(i.resumo)}</p><div class="use"><i>O que o Haven faz com isso</i>${esc(i.por_que_importa)}</div><div class="foot"><span><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)}</span><span>${(i.para||[]).map(esc).join(" · ")}</span></div>${intHtml(key,false)}</article>`;
const briefHtml = (i,key) => `<article class="brief p-${esc(i.pilar)}">${tagHtml(i)}<h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3><p class="use">${esc(i.por_que_importa)}</p><div class="foot"><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)} · ${(i.para||[]).map(esc).join(" · ")}</div>${intHtml(key,false)}</article>`;
const benchHtml = (b,n,key) => `<li><span class="k">${String(n).padStart(2,"0")}</span><div><b>${esc(b.area||b.para||"")}</b><p>${esc(b.ideia)}</p>${b.ref?`<div class="ref"><i>A partir de</i>${b.url?`<a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.ref)}</a>`:esc(b.ref)}</div>`:""}${intHtml(key,true)}</div></li>`;
const splitWatch = a => { const m = String(a).match(/^([^:]{2,24}):\s*(.*)$/s); return m ? `<span><b>${esc(m[1])}</b>${esc(m[2])}</span>` : `<span>${esc(a)}</span>`; };

function render(){
  const idx = RADAR.dias.findIndex(d=>d.data===state.day); const day = RADAR.dias[idx] || RADAR.dias[0]; if(!day) return;
  const num = RADAR.dias.length - (idx<0?0:idx); const items = day.itens || []; const br=items.filter(i=>i.escopo==="brasil").length;
  $("folio-left").textContent = `Nº ${num} · ${fmtLong(day.data)}`; $("tally").textContent = `${items.length} itens conferidos · ${br} Brasil · ${items.length-br} mundo`;
  const keyed = items.map((i,n)=>({i,key:keyItem(day,n)}));
  const list = keyed.filter(({i}) => (!state.escopo||i.escopo===state.escopo) && (!state.pilar||i.pilar===state.pilar) && (!state.para||(i.para||[]).includes(state.para)));
  $("count").textContent = `${list.length} de ${items.length}`;
  const unfiltered = !state.escopo && !state.pilar && !state.para;
  const leads = list.filter(x=>x.i.destaque), rest = list.filter(x=>!x.i.destaque);
  const restBr = rest.filter(x=>x.i.escopo==="brasil"), restWd = rest.filter(x=>x.i.escopo==="mundo");
  let html = "";
  if (unfiltered) html += `<section class="open"><div><h2 class="manchete">${esc(day.manchete||"")}</h2><p class="editorial">${esc(day.editorial||"")}</p><div class="tally">${items.length} itens conferidos na fonte · ${br} do Brasil · ${items.length-br} do mundo</div></div><aside class="watch"><h2>Pra prestar atenção</h2><ol>${(day.atencao||[]).map(a=>`<li>${splitWatch(a)}</li>`).join("")}</ol></aside></section>`;
  const bench = (day.bench||[]).map((b,n)=>({b,n,key:keyBench(day,n)})).filter(x => !state.para || x.b.para===state.para);
  if (bench.length && !state.escopo && !state.pilar) html += `<section class="bench"><div class="head"><h2>Bench pro Haven</h2><span>${bench.length} ${bench.length>1?"referências aplicadas ao projeto":"referência aplicada ao projeto"}</span></div><ol>${bench.map((x,k)=>benchHtml(x.b,k+1,x.key)).join("")}</ol></section>`;
  if (leads.length) html += `<div class="sec"><h2>Destaques</h2><span>o que merece leitura inteira</span></div><div class="grid">${leads.map(x=>artHtml(x.i,x.key)).join("")}</div>`;
  if (unfiltered) {
    if (restBr.length) html += `<div class="sec"><h2>Em pauta · Brasil</h2><span>${restBr.length} ${restBr.length>1?"itens":"item"}</span></div><div class="pauta">${restBr.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
    if (restWd.length) html += `<div class="sec"><h2>Em pauta · Mundo</h2><span>${restWd.length} ${restWd.length>1?"itens":"item"}</span></div><div class="pauta">${restWd.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
  } else if (rest.length) html += `<div class="sec"><h2>Em pauta</h2><span>${rest.length} ${rest.length>1?"itens":"item"}</span></div><div class="pauta">${rest.map(x=>briefHtml(x.i,x.key)).join("")}</div>`;
  if (!list.length) html += `<div class="empty">Nenhum item com esses filtros. Escolha outro pilar ou volte pra tudo.</div>`;
  $("main").innerHTML = html;
  const RS = RADAR.respostas_sala || {};
  $("pautas").innerHTML = shared.pautas.length ? shared.pautas.map(p=>{ const r = RS[p.id]; const resp = (r&&r.resposta)||p.resposta; const ed = (r&&r.edicao)||p.edicao; const done = p.status==="respondida"||!!r;
    return `<li>${esc(p.texto)}<div class="who"><b>${esc(nameOf(p.email))}</b> ${fmtTs(p.t)} · ${done?"respondida na edição "+fmtShort(ed||""):"aberta"}${(p.email===meEmail||isAdmin)?` · <button class="toggle" data-act="apagar-pauta" data-id="${esc(p.id)}">apagar</button>`:""}</div>${resp?`<div class="resp"><i>Resposta da Bru</i>${esc(resp)}</div>`:""}</li>`; }).join("")
    : `<li class="vazio">Nenhuma pauta ainda. O primeiro pedido do time aparece aqui e entra no radar da manhã seguinte.</li>`;
  const ativos = Object.values(shared.ideias).filter(s=>s.status && s.status!=="nova" && lookup[s.chave]).sort((a,b)=>new Date(b.t)-new Date(a.t));
  $("andamento").innerHTML = ativos.length ? ativos.map(s=>{ const L=lookup[s.chave]; return `<li><span class="pill ${esc(s.status)}">${esc(STATUS[s.status]||s.status)}</span><div>${esc(L.obj.ideia)}<div class="who"><b>${esc(s.dono?nameOf(s.dono):"sem responsável")}</b> · ${esc(L.obj.area||"")} · edição ${fmtShort(L.day.data)}</div></div></li>`; }).join("")
    : `<li class="vazio">Nada assumido ainda. Mude o status de uma ideia do Bench ou clique em Assumir e ela aparece aqui.</li>`;
}

async function gravar(p){ const { error } = await p; if (error) note("Não deu pra salvar agora. Tente de novo em instantes."); else { note(""); await carregar(); } }
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
boot();
</script>
</body>
</html>
"""
out = TEMPLATE.replace("__CSS__", css + extra).replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY)
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
open(dest, "w", encoding="utf-8").write(out)
print("sala (domínio) gerada:", dest, len(out), "bytes")
