#!/usr/bin/env python3
"""Gera sala.html, a Sala do Time do Daily Haven Bench News, pra publicar como Artifact no claude.ai.
Mesmo layout do site, mais reações, comentários, status das ideias do Bench, caixa de pauta e pergunta pro Claude.
Uso: python3 build_sala.py [destino]  (padrão: ../sala/sala.html)
O arquivo sai sem doctype/html/head/body: o Artifact monta o esqueleto na publicação.
"""
import json, os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "radar-data.json"), encoding="utf-8"))
data_js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "sala", "sala.html")

# reaproveita o CSS do site
site = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", site, re.S).group(1)
css = css.replace(".page{max-width:1280px;margin:0 auto;padding:22px 16px 72px}",
                  ".page{max-width:1280px;margin:0 auto;padding-block:22px 72px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}")
css = css.replace("@media(min-width:760px){.page{padding:30px 44px 96px}}",
                  "@media(min-width:760px){.page{padding-block:30px 96px;padding-left:max(44px,env(safe-area-inset-left,0px));padding-right:max(44px,env(safe-area-inset-right,0px))}}")
css = css.replace("*{box-sizing:border-box;margin:0;padding:0}", "*{box-sizing:border-box;margin:0;padding:0}\n  :root{color-scheme:light}")

EXTRA_CSS = r"""
  /* sala do time */
  .sala-top{display:grid;grid-template-columns:1fr;gap:28px;padding:26px 0 8px;border-bottom:1px solid var(--rule-strong)}
  @media(min-width:960px){.sala-top{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:56px}}
  .box h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;line-height:1.1;padding-bottom:10px;border-bottom:3px solid var(--terracotta)}
  .box .sub{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute);margin:8px 0 4px}
  .box ul{list-style:none}
  .box li{padding:12px 0;border-bottom:1px solid var(--rule);font-family:var(--serif2);font-size:17px;line-height:1.42;color:var(--espresso)}
  .box li .who{font-family:var(--sans);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-top:4px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
  .box li .who b{color:var(--ink);font-weight:600}
  .box li .resp{margin-top:8px;padding:8px 0 2px 12px;border-left:2px solid var(--terracotta);font-size:16px}
  .box li .resp i{font-family:var(--sans);font-style:normal;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--terracotta);display:block;margin-bottom:4px}
  .box .vazio{font-family:var(--serif2);font-size:17px;color:var(--mute);padding:14px 0}
  .form{display:flex;flex-direction:column;gap:8px;margin-top:12px}
  textarea,input[type=text]{font-family:var(--serif2);font-size:17px;line-height:1.4;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:10px 12px;width:100%;resize:vertical;min-height:44px}
  textarea:focus,input:focus{outline:2px solid var(--terracotta);outline-offset:1px;border-color:var(--terracotta)}
  .btn{font-family:var(--sans);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:600;background:var(--espresso);color:var(--paper);border:0;padding:10px 16px;cursor:pointer;align-self:flex-start}
  .btn:hover{background:var(--ink)}
  .btn[disabled]{opacity:.45;cursor:default}
  .btn.ghost{background:transparent;color:var(--espresso);border:1px solid var(--espresso)}
  .btn.ghost:hover{background:var(--paper)}
  .btn.sm{padding:6px 10px;font-size:10px}
  .row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  .andamento li{display:grid;grid-template-columns:auto 1fr;gap:12px;align-items:start}
  .pill{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;font-weight:700;padding:4px 8px;border:1px solid var(--rule);color:var(--soft);white-space:nowrap;margin-top:4px}
  .pill.avaliando{color:var(--ochre);border-color:var(--ochre)}
  .pill.andamento{color:var(--forest);border-color:var(--forest)}
  .pill.descartada{color:var(--mute);text-decoration:line-through}
  .pill.feita{color:var(--teal);border-color:var(--teal)}

  /* faixa de interação em cada item e ideia */
  .int{margin-top:4px;padding-top:10px;border-top:1px dashed var(--rule);display:flex;flex-direction:column;gap:8px}
  .int .acts{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
  .int .vote{font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;background:transparent;border:1px solid var(--rule);color:var(--soft);padding:5px 9px;cursor:pointer}
  .int .vote.on{border-color:var(--terracotta);color:var(--terracotta);font-weight:700}
  .int .vote[disabled]{cursor:default;opacity:.7}
  .int .vote em{font-style:normal;font-variant-numeric:tabular-nums;margin-left:5px;color:var(--mute)}
  .int .toggle{font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;background:none;border:0;color:var(--terracotta);cursor:pointer;padding:5px 2px;text-decoration:underline;text-underline-offset:3px}
  .int select{font-family:var(--sans);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:5px 8px;cursor:pointer}
  .int .cm{list-style:none;display:flex;flex-direction:column;gap:6px}
  .int .cm li{font-family:var(--serif2);font-size:16px;line-height:1.4;color:var(--espresso);padding:6px 0 6px 12px;border-left:2px solid var(--rule)}
  .int .cm li.claude{border-left-color:var(--teal)}
  .bench li .int .cm li{display:block;grid-template-columns:none;padding:6px 0 6px 12px;border-bottom:0}
  .bench li .int .cm li .who b{display:inline;font-size:10px;letter-spacing:.16em;color:var(--ink);margin:0 4px 0 0}
  .int .cm li .who{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-top:3px}
  .int .cm li .who b{color:var(--ink);font-weight:600}
  .int .ask{display:flex;flex-direction:column;gap:6px}
  .int .ask .out{font-family:var(--serif2);font-size:16.5px;line-height:1.45;color:var(--ink);padding:10px 0 4px 12px;border-left:2px solid var(--teal);white-space:pre-wrap;min-height:0}
  .int .ask .out:empty{display:none}
  .int .note{font-family:var(--sans);font-size:11px;color:var(--mute)}
  .ro{font-family:var(--sans);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute);padding:10px 0;border-bottom:1px solid var(--rule)}
  .ro b{color:var(--terracotta)}
  .me{font-family:var(--sans);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
  .me b{color:var(--ink);font-weight:600}
  .chat{margin-top:26px;border-top:3px solid var(--teal);padding-top:12px}
  .chat h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;line-height:1.1}
  .chat .sub{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute);margin:6px 0 10px}
  .chat .log{display:flex;flex-direction:column;gap:10px;max-width:78ch}
  .chat .msg{font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--ink);padding:8px 0 8px 14px;border-left:2px solid var(--rule);white-space:pre-wrap}
  .chat .msg.me{border-left-color:var(--terracotta);color:var(--espresso)}
  .chat .msg.ai{border-left-color:var(--teal)}
  .chat .msg i{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);display:block;margin-bottom:4px}
  .chat .form{max-width:78ch}
  .chat .form textarea{min-height:56px}
"""

TEMPLATE = r"""<title>Sala do Time · Haven Bench News</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<style>__CSS__</style>
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
    <span class="me" id="me"></span>
  </div>
  <div class="ro" id="ro" hidden><b>Modo leitura.</b> Você vê a sala, mas comentários, votos e pautas precisam de convite da Bru como editor.</div>

  <nav class="nav" aria-label="Filtros">
    <div class="grp" data-f="para"><span class="lbl">Pra quem</span><button class="on" data-v="">Tudo</button><button data-v="parcerias">Parcerias</button><button data-v="marketing">Marketing</button><button data-v="vendas">Vendas</button><button data-v="clube">Clube</button></div>
    <div class="grp" data-f="escopo"><span class="lbl">Onde</span><button class="on" data-v="">Tudo</button><button data-v="brasil">Brasil</button><button data-v="mundo">Mundo</button></div>
    <div class="grp" data-f="pilar"><span class="lbl">Pilar</span><button class="on" data-v="">Todos</button><button data-v="wellness-residence">Wellness residence</button><button data-v="membership">Membership</button><button data-v="longevidade">Longevidade</button><button data-v="comunidade">Comunidade</button><button data-v="lifestyle">Lifestyle</button><button data-v="estudos">Estudos</button><button data-v="eventos">Eventos</button><button data-v="marcas">Marcas</button></div>
    <span class="n" id="count"></span>
  </nav>

  <section class="chat" id="chat" hidden>
    <h2>Fale com o Claude sobre o Haven</h2>
    <p class="sub">conhece o projeto e a edição de hoje; responde na hora, na sua conta; não pesquisa fora. Pra pergunta de mercado, use a caixa Pra pauta</p>
    <div class="log" id="chat-log"></div>
    <form class="form" id="chat-form"><textarea id="chat-txt" rows="2" placeholder="Ex.: como o Preserve Life se compara ao nosso membership? Ou: me dá três ângulos pra falar do Bench de hoje com um Founding."></textarea><div class="row"><button class="btn" type="submit" id="chat-btn">Perguntar</button><button class="btn ghost" type="button" id="chat-stop" hidden>Parar</button><button class="btn ghost" type="button" id="chat-clear" hidden>Limpar conversa</button><span class="note" id="chat-note"></span></div></form>
  </section>
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
      <h2>Em andamento</h2>
      <p class="sub">ideias do Bench que alguém do time assumiu, de qualquer edição</p>
      <ul id="andamento"></ul>
    </div>
  </section>

  <main id="main"></main>

  <footer>
    <p>Cada item foi aberto e conferido na fonte no dia da edição. Nesta sala, reações, comentários, status e pautas são compartilhados com todo o time e lidos pela Bru na rotina da manhã. As respostas do Claude aparecem só pra quem perguntou, até serem salvas como comentário.</p>
    <span class="sig">Bru</span>
  </footer>
</div>
<script>
const RADAR = __DATA__;
const PILAR = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade","estudos":"Estudos","eventos":"Eventos","marcas":"Marcas"};
const STATUS = {nova:"Nova",avaliando:"Avaliando",andamento:"Em andamento",feita:"Feita",descartada:"Descartada"};
const M=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const W=["domingo","segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtLong = d => { const [y,m,dd]=d.split("-").map(Number); const w=new Date(Date.UTC(y,m-1,dd)).getUTCDay(); return `${W[w]}, ${dd} de ${M[m-1]} de ${y}`; };
const fmtSel = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]} ${y}`; };
const fmtShort = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]}`; };
const fmtTs = t => { const d=new Date(t); return isNaN(d)?"":`${d.getDate()} ${MS[d.getMonth()]} ${String(d.getHours()).padStart(2,"0")}h${String(d.getMinutes()).padStart(2,"0")}`; };
const state = {day: RADAR.dias[0].data, escopo:"", pilar:"", para:""};

/* chaves estáveis: edição + posição do item ou da ideia */
const keyItem = (day,n) => `e${day.data}-i${n}`;
const keyBench = (day,n) => `e${day.data}-b${n}`;
const lookup = {};
RADAR.dias.forEach(d => { (d.itens||[]).forEach((i,n)=>lookup[keyItem(d,n)]={tipo:"item",day:d,obj:i}); (d.bench||[]).forEach((b,n)=>lookup[keyBench(d,n)]={tipo:"bench",day:d,obj:b}); });

/* estado compartilhado (vem do db) */
const shared = {votos:{}, comentarios:[], pautas:[], ideias:{}};
let db=null, user=null, sample=null, uid=null, canWrite=null, meName="";
const opened = new Set(); /* comentários abertos por chave */

const sel = document.getElementById("day");
RADAR.dias.forEach(d => { const o=document.createElement("option"); o.value=d.data; o.textContent=fmtSel(d.data); sel.appendChild(o); });
sel.addEventListener("change", e => { state.day=e.target.value; render(); });
document.querySelectorAll(".grp[data-f]").forEach(g => g.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
  g.querySelectorAll("button").forEach(x=>x.classList.remove("on")); b.classList.add("on"); state[g.dataset.f]=b.dataset.v; render();
})));

const nameOf = (ps,id) => (ps && ps[id] && ps[id].name) || "Alguém do time";

function votesFor(key){ const out={sim:0,nao:0,mine:null}; for (const v of Object.values(shared.votos)) if (v.key===key){ if(v.v==="sim")out.sim++; else if(v.v==="nao")out.nao++; if(v.uid===uid)out.mine=v.v; } return out; }
function commentsFor(key){ return shared.comentarios.filter(c=>c.key===key).sort((a,b)=>(a.t||0)-(b.t||0)); }

function intHtml(key, ps, isBench){
  const v = votesFor(key), cs = commentsFor(key), w = canWrite!==false;
  const st = shared.ideias[key] || {};
  const status = st.status || "nova";
  let h = `<div class="int" data-key="${esc(key)}"><div class="acts">`;
  if (isBench) {
    h += `<select data-act="status" aria-label="Status da ideia" ${w?"":"disabled"}>${Object.entries(STATUS).map(([k,l])=>`<option value="${k}" ${k===status?"selected":""}>${l}</option>`).join("")}</select>`;
    if (st.dono) h += `<span class="pill ${esc(status)}">${esc(nameOf(ps,st.dono))}</span>`;
    else if (w) h += `<button class="vote" data-act="assumir">Assumir</button>`;
  } else {
    h += `<button class="vote ${v.mine==="sim"?"on":""}" data-act="sim" ${w?"":"disabled"}>Serviu<em>${v.sim}</em></button>`;
    h += `<button class="vote ${v.mine==="nao"?"on":""}" data-act="nao" ${w?"":"disabled"}>Não serviu<em>${v.nao}</em></button>`;
  }
  h += `<button class="toggle" data-act="toggle">${opened.has(key)?"Fechar":"Comentar"}${cs.length?` (${cs.length})`:""}</button>`;
  if (sample) h += `<button class="toggle" data-act="ask">Perguntar ao Claude</button>`;
  h += `</div>`;
  if (opened.has(key)) {
    h += `<ul class="cm">${cs.map(c=>`<li class="${(c.tipo==="claude"||c.uid==="bench")?"claude":""}">${esc(c.texto)}<div class="who"><b>${esc(c.tipo==="claude"?"Claude, salvo por "+nameOf(ps,c.uid):(c.uid==="bench"?"Resposta da Bru, via Bench":nameOf(ps,c.uid)))}</b> ${fmtTs(c.t)}</div></li>`).join("")}</ul>`;
    if (w) h += `<form class="form" data-act="comment"><textarea rows="2" placeholder="Comentário pro time"></textarea><div class="row"><button class="btn sm" type="submit">Publicar</button></div></form>`;
    if (opened.has(key+"#ask")) h += `<div class="ask"><input type="text" placeholder="Ex.: me dá três ângulos pra post sobre isso" data-ask="q"><div class="row"><button class="btn sm" data-act="askgo">Perguntar</button><button class="btn sm ghost" data-act="askstop" hidden>Parar</button><button class="btn sm ghost" data-act="asksave" hidden>Salvar como comentário</button></div><div class="out" data-ask="out"></div><div class="note" data-ask="note"></div></div>`;
  }
  return h + `</div>`;
}

const tagHtml = i => `<div class="tag">${esc(PILAR[i.pilar]||i.pilar)}<span>${i.escopo==="brasil"?"Brasil":"Mundo"} · ${esc(i.region||"")}</span></div>`;
const artHtml = (i,key,ps) => `
  <article class="art p-${esc(i.pilar)}">
    ${tagHtml(i)}
    <h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3>
    <p class="txt">${esc(i.resumo)}</p>
    <div class="use"><i>O que o Haven faz com isso</i>${esc(i.por_que_importa)}</div>
    <div class="foot"><span><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)}</span><span>${(i.para||[]).map(esc).join(" · ")}</span></div>
    ${intHtml(key,ps,false)}
  </article>`;
const briefHtml = (i,key,ps) => `
  <article class="brief p-${esc(i.pilar)}">
    ${tagHtml(i)}
    <h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3>
    <p class="use">${esc(i.por_que_importa)}</p>
    <div class="foot"><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)} · ${(i.para||[]).map(esc).join(" · ")}</div>
    ${intHtml(key,ps,false)}
  </article>`;
const benchHtml = (b, n, key, ps) => `
  <li><span class="k">${String(n).padStart(2,"0")}</span><div><b>${esc(b.area||b.para||"")}</b><p>${esc(b.ideia)}</p>${b.ref?`<div class="ref"><i>A partir de</i>${b.url?`<a href="${esc(b.url)}" target="_blank" rel="noopener">${esc(b.ref)}</a>`:esc(b.ref)}</div>`:""}${intHtml(key,ps,true)}</div></li>`;
const splitWatch = a => { const m = String(a).match(/^([^:]{2,24}):\s*(.*)$/s); return m ? `<span><b>${esc(m[1])}</b>${esc(m[2])}</span>` : `<span>${esc(a)}</span>`; };

let rendering = false;
async function render(){
  const idx = RADAR.dias.findIndex(d=>d.data===state.day);
  const day = RADAR.dias[idx] || RADAR.dias[0];
  const num = RADAR.dias.length - (idx<0?0:idx);
  const items = day.itens || [];
  const br=items.filter(i=>i.escopo==="brasil").length;
  document.getElementById("folio-left").textContent = `Nº ${num} · ${fmtLong(day.data)}`;
  document.getElementById("tally").textContent = `${items.length} itens conferidos · ${br} Brasil · ${items.length-br} mundo`;
  const keyed = items.map((i,n)=>({i,key:keyItem(day,n)}));
  const list = keyed.filter(({i}) => (!state.escopo||i.escopo===state.escopo) && (!state.pilar||i.pilar===state.pilar) && (!state.para||(i.para||[]).includes(state.para)));
  document.getElementById("count").textContent = `${list.length} de ${items.length}`;
  const unfiltered = !state.escopo && !state.pilar && !state.para;
  const leads = list.filter(x=>x.i.destaque);
  const rest = list.filter(x=>!x.i.destaque);
  const restBr = rest.filter(x=>x.i.escopo==="brasil"), restWd = rest.filter(x=>x.i.escopo==="mundo");

  /* nomes de quem aparece na tela */
  const ids = new Set();
  shared.comentarios.forEach(c=>c.uid&&ids.add(c.uid)); shared.pautas.forEach(p=>p.uid&&ids.add(p.uid)); Object.values(shared.ideias).forEach(s=>s.dono&&ids.add(s.dono));
  const ps = (user && ids.size) ? await user.profiles([...ids]) : {};

  let html = "";
  if (unfiltered) html += `
    <section class="open">
      <div><h2 class="manchete">${esc(day.manchete||"")}</h2><p class="editorial">${esc(day.editorial||"")}</p><div class="tally">${items.length} itens conferidos na fonte · ${br} do Brasil · ${items.length-br} do mundo</div></div>
      <aside class="watch"><h2>Pra prestar atenção</h2><ol>${(day.atencao||[]).map(a=>`<li>${splitWatch(a)}</li>`).join("")}</ol></aside>
    </section>`;
  const bench = (day.bench||[]).map((b,n)=>({b,n,key:keyBench(day,n)})).filter(x => !state.para || x.b.para===state.para);
  if (bench.length && !state.escopo && !state.pilar) html += `
    <section class="bench"><div class="head"><h2>Bench pro Haven</h2><span>${bench.length} ${bench.length>1?"referências aplicadas ao projeto":"referência aplicada ao projeto"}${state.para?` · ${esc(state.para)}`:""}</span></div>
      <ol>${bench.map((x,k)=>benchHtml(x.b,k+1,x.key,ps)).join("")}</ol></section>`;
  if (leads.length) html += `<div class="sec"><h2>Destaques</h2><span>o que merece leitura inteira</span></div><div class="grid">${leads.map(x=>artHtml(x.i,x.key,ps)).join("")}</div>`;
  if (unfiltered) {
    if (restBr.length) html += `<div class="sec"><h2>Em pauta · Brasil</h2><span>${restBr.length} ${restBr.length>1?"itens":"item"}</span></div><div class="pauta">${restBr.map(x=>briefHtml(x.i,x.key,ps)).join("")}</div>`;
    if (restWd.length) html += `<div class="sec"><h2>Em pauta · Mundo</h2><span>${restWd.length} ${restWd.length>1?"itens":"item"}</span></div><div class="pauta">${restWd.map(x=>briefHtml(x.i,x.key,ps)).join("")}</div>`;
  } else if (rest.length) {
    html += `<div class="sec"><h2>Em pauta</h2><span>${rest.length} ${rest.length>1?"itens":"item"}</span></div><div class="pauta">${rest.map(x=>briefHtml(x.i,x.key,ps)).join("")}</div>`;
  }
  if (!list.length) html += `<div class="empty">Nenhum item com esses filtros. Escolha outro pilar ou volte pra tudo.</div>`;
  document.getElementById("main").innerHTML = html;

  /* pautas */
  const pl = document.getElementById("pautas");
  const pautas = [...shared.pautas].sort((a,b)=>(b.t||0)-(a.t||0));
  pl.innerHTML = pautas.length ? pautas.map(p=>`<li>${esc(p.texto)}<div class="who"><b>${esc(nameOf(ps,p.uid))}</b> ${fmtTs(p.t)} · ${p.status==="respondida"?"respondida na edição "+esc(p.edicao||""):"aberta"}</div>${p.resposta?`<div class="resp"><i>Resposta da Bru</i>${esc(p.resposta)}</div>`:""}</li>`).join("")
    : `<li class="vazio">Nenhuma pauta ainda. O primeiro pedido do time aparece aqui e entra no radar da manhã seguinte.</li>`;
  /* em andamento */
  const al = document.getElementById("andamento");
  const ativos = Object.entries(shared.ideias).filter(([k,s])=>s.status && s.status!=="nova" && lookup[k]).sort((a,b)=>(b[1].t||0)-(a[1].t||0));
  al.innerHTML = ativos.length ? ativos.map(([k,s])=>{ const L=lookup[k]; return `<li><span class="pill ${esc(s.status)}">${esc(STATUS[s.status]||s.status)}</span><div>${esc(L.obj.ideia)}<div class="who"><b>${esc(s.dono?nameOf(ps,s.dono):"sem responsável")}</b> · ${esc(L.obj.area||"")} · edição ${fmtShort(L.day.data)}</div></div></li>`; }).join("")
    : `<li class="vazio">Nada assumido ainda. Mude o status de uma ideia do Bench ou clique em Assumir e ela aparece aqui.</li>`;
}

/* ações */
document.addEventListener("click", async e => {
  const b = e.target.closest("[data-act]"); if (!b) return;
  const box = b.closest(".int"); const key = box && box.dataset.key; const act = b.dataset.act;
  if (!key) return;
  if (act==="toggle"){ opened.has(key)?(opened.delete(key),opened.delete(key+"#ask")):opened.add(key); render(); return; }
  if (act==="ask"){ opened.add(key); opened.add(key+"#ask"); render(); setTimeout(()=>{ const q=document.querySelector(`.int[data-key="${CSS.escape(key)}"] [data-ask=q]`); q&&q.focus(); },0); return; }
  if (act==="askgo"||act==="askstop"||act==="asksave"){ e.preventDefault(); return askHandle(key, act, box); }
  if (!db || !uid || canWrite===false) return;
  if (act==="sim"||act==="nao"){
    const cur = votesFor(key).mine; const ref = db.collection("votos").doc(`${key}__${uid}`);
    try { if (cur===act) await ref.delete(); else await ref.set({key, uid, v:act, t:Date.now()}); } catch(err){ onWriteError(err); }
    return;
  }
  if (act==="assumir"){ try { await db.collection("ideias").doc(key).set({...(shared.ideias[key]||{}), status: (shared.ideias[key]||{}).status||"avaliando", dono:uid, t:Date.now()}); } catch(err){ onWriteError(err); } return; }
});
document.addEventListener("change", async e => {
  const s = e.target.closest("select[data-act=status]"); if (!s) return;
  const key = s.closest(".int").dataset.key; if (!db||!uid) return;
  const prev = shared.ideias[key]||{};
  try { await db.collection("ideias").doc(key).set({...prev, status:s.value, dono: prev.dono || (s.value==="nova"?null:uid), t:Date.now()}); } catch(err){ onWriteError(err); }
});
document.addEventListener("submit", async e => {
  const f = e.target; e.preventDefault();
  if (f.id==="pauta-form"){
    const ta = document.getElementById("pauta-txt"); const txt = ta.value.trim(); if (!txt||!db||!uid) return;
    const btn = document.getElementById("pauta-btn"); btn.disabled=true;
    try { await db.collection("pautas").add({uid, texto:txt, t:Date.now(), status:"aberta"}); ta.value=""; } catch(err){ onWriteError(err); } finally { btn.disabled=false; }
    return;
  }
  if (f.dataset.act==="comment"){
    const key = f.closest(".int").dataset.key; const ta=f.querySelector("textarea"); const txt=ta.value.trim(); if(!txt||!db||!uid) return;
    try { await db.collection("comentarios").add({key, uid, texto:txt, t:Date.now(), tipo:"comentario"}); ta.value=""; } catch(err){ onWriteError(err); }
  }
});
function onWriteError(err){
  const code = err && err.code;
  if (code==="invalid_argument"||code==="not_granted"||code==="revoked"){ canWrite=false; document.getElementById("ro").hidden=false; render(); }
  else if (code==="quota_exceeded"){ alertNote("A sala atingiu o limite de registros. Avise a Bru pra arquivar o que já foi lido."); }
  else alertNote("Não deu pra salvar agora. Tente de novo em instantes.");
}
function alertNote(msg){ const ro=document.getElementById("ro"); ro.hidden=false; ro.innerHTML=`<b>Aviso.</b> ${esc(msg)}`; }

/* pergunta pro Claude, dentro da página */
const asks = {};
function contextFor(key){
  const L = lookup[key]; if (!L) return BRIEF;
  const d = L.day;
  let ctx = BRIEF + `\nEdição do Daily Haven Bench News de ${d.data}.\nManchete: ${d.manchete}\nEditorial: ${d.editorial}\n`;
  if (L.tipo==="item"){ const i=L.obj; ctx += `\nItem em discussão:\nTítulo: ${i.title}\nFonte: ${i.source} (${i.date}), ${i.region}\nResumo: ${i.resumo}\nO que o Haven faz com isso: ${i.por_que_importa}\nTimes: ${(i.para||[]).join(", ")}\n`; }
  else { const b=L.obj; ctx += `\nIdeia do Bench pro Haven em discussão:\nÁrea: ${b.area}\nIdeia: ${b.ideia}\nReferência: ${b.ref}\n`; }
  const cs = commentsFor(key).filter(c=>c.tipo!=="claude").slice(-6);
  if (cs.length) ctx += `\nComentários do time até agora:\n` + cs.map(c=>`- ${c.texto}`).join("\n") + "\n";
  return ctx;
}
const BRIEF = `BRIEFING DO HAVEN (uso interno do time; números marcados como hipótese estão em validação e não devem ser citados como fechados)
O que é: residence club com alma brasileira em Porto Feliz, SP, a cerca de 90 minutos de São Paulo. Uma vila de casas prontas pra morar e um social club com admissão por comitê. A comunidade vem antes do metro quadrado: toda casa começa com uma candidatura ao Haven Club, lida por um comitê de curadores que procura alinhamento e repertório, antes de bolso, cargo ou idade. Founding members escolhem casa primeiro. Fundadora e CEO: Stephanie Fleury (Teti). Bruna Infurna (Bru) cuida de estratégia, marca e do Bench News. O projeto chegou a ser chamado Ma Haven (versão anterior em Mairinque, 15 casas); o nome atual é Haven, em Porto Feliz, com cerca de 75 casas no masterplan em validação.
Pilares: longevidade e bem-estar como rotina da porta de casa; future living (casa pronta, tecnologia discreta, House of AI); comunidade curada; repertório como critério; natureza no comando, mais de 70% da gleba preservada como mata, jardim ou cultivo (hipótese do masterplan).
As casas (The Havens, specs em fechamento com engenharia): Nest (1 suíte, 100 m², lote 1.000 m²), Duet (2 suítes, 200 m², lote 1.500 m²), Tribe (3 suítes, 300 m², lote 2.000 m²), Family (4 suítes, 400 m², lote 2.000 m²), Estates (lotes de 5.000 m² pra projeto próprio). Entregues prontas: marcenaria, marmoraria, ar e aquecimento, esquadrias, louças e metais, iluminação, kit tech, paisagismo, garagem solar. Opcionais: piscina, sauna, adega, automação, banheira, piso aquecido, enxoval premium, acessibilidade. Preços de referência de versões anteriores (hipótese): a partir de R$ 5,5 milhões (Duet) a R$ 8 milhões (Family).
O clube (Haven Club, cerca de 2.800 m² de áreas comuns, programação o ano inteiro): Wellness (academia, sauna, banheira de gelo, massagem, yoga, sound healing); Wine & Dine (cozinha gourmet, pool bar, chefs convidados, adega); Lazer & Sports (piscinas, tênis, beach tennis, vôlei, SUP, wake surf); Cultivo (horta e pomar do canteiro à mesa); Little Haven (brinquedoteca e playground); Cine ao ar livre, fire pit, picnic; Listening Bar (vinil, DJs, karaokê, estúdio de podcast); House of AI ("inteligência nada artificial", conversas sobre o futuro, coworking, espresso bar); Empório e conveniência.
Membership, cinco formas de pertencer, todas pelo mesmo comitê: Founding (entra antes, ajuda a moldar o clube, escolhe casa primeiro, assento na curadoria), Resident (dono de casa, acesso completo), Social (sem casa, usa o clube e tem diárias de hospedagem incluídas), Guest (frequenta programação e eventos, sem diárias), Corporate (empresas: offsites, retiros, hospedagem de time). Business case do clube (junho de 2026, hipóteses de partida): o clube é a isca e a residência é a pesca; a sala mira gente interessante com poder aquisitivo, núcleo de empresários e executivos que paga, alma cultural parcialmente subsidiada (teto de 15%), sensibilidade centro-esquerda humanista, anti-perfil é ostentação sem repertório. Faixas hipótese: Círculo Fundador R$ 60 mil de adesão e R$ 30 mil por ano (cohort pequeno, fecha); Membro R$ 20 mil e R$ 26 mil por ano; Jovem sub-35 R$ 5 mil e R$ 13 mil por ano; Assento Cultural de R$ 0 a 6 mil por ano, curado; Parceiro/Casa corporativo a partir de R$ 150 mil por ano, poucos. Diárias por categoria na operação e na rede de parceiros, com blackout em alta temporada. Recomendação vigente: lançar o Círculo Fundador primeiro como teste de preço e densidade.
Ownspitality: o dono vira anfitrião. Quem quiser coloca a casa no pool de hospedagem do clube quando não está usando; gestão com padrão de hotel; hóspede também passa pela curadoria. Adesão opcional; social members usam diárias nessas casas.
Curadoria e embaixadores (nomes pendentes de autorização de uso, não publicar fora do time): curadores Tatiana Foresta (arte e cultura), Renata Vanzetto (gastronomia), Michelle Schneider (wellness), Gaby e Nat Graf (música), Nat Brandão (House of AI), Mary Olivetti (drinks e vinho); embaixadores Alice Braga, Glenda Kozlowski, Ronaldo Lemos, German Carmona, Lara D'avila, Pedro Bookster.
Vizinhança e mercado: Porto Feliz tem Fazenda Boa Vista e Boa Vista Village (JHSF) e a chegada da Cyrela com o Heritage Riviera; o Haven lê isso como validação da região e se diferencia falando de quem você vai encontrar, não do que vai ter. Referências globais: Aman, Six Senses, 1 Hotel, Serenbe; no Brasil não há wellness residence consolidada. Vocabulário a evitar: superlativos, "exclusivo", "inimaginável", lista de amenities como manchete.
Times do Bench News: parcerias, marketing, vendas e clube. O Bench News é o radar diário (site em projetorepertorio.com.br/benchnews) com itens verificados na fonte, destaques, Pra prestar atenção e o Bench pro Haven (ideias aplicadas ao projeto).
`;
const RULES = `Você ajuda o time do Haven, um projeto de wellness residence com clube de membership em Porto Feliz, SP (75 casas, membership curado, longevidade, future living, comunidade). Stephanie Fleury (Teti) é founder e CEO; Bruna Infurna (Bru) edita o Bench News. Responda em português brasileiro, direto, em prosa curta (no máximo 180 palavras, a não ser que peçam lista), capitalização normal, sem travessão, sem "não é X, é Y", sem pergunta retórica, sem fechamento moralizante, sem jargão de marketing (alavancar, desbloquear, empoderar). Use só os fatos do briefing e do contexto abaixo; não invente número, fonte ou data; trate números marcados como hipótese como hipótese. Se faltar dado, diga que não está no material e sugira o que pedir na caixa Pra pauta, que a Bru responde na edição seguinte com pesquisa.\n\n`;
async function askHandle(key, act, box){
  const q = box.querySelector("[data-ask=q]"), out = box.querySelector("[data-ask=out]"), note = box.querySelector("[data-ask=note]");
  const go = box.querySelector("[data-act=askgo]"), stop = box.querySelector("[data-act=askstop]"), save = box.querySelector("[data-act=asksave]");
  if (act==="askstop"){ asks[key]?.ctl?.abort(); return; }
  if (act==="asksave"){
    const a = asks[key]; if (!a||!a.text||!db||!uid) return;
    save.disabled=true;
    try { await db.collection("comentarios").add({key, uid, texto:`Pergunta: ${a.q}\nResposta: ${a.text}`, t:Date.now(), tipo:"claude"}); note.textContent="Salvo como comentário."; } catch(err){ onWriteError(err); } finally { save.disabled=false; }
    return;
  }
  const question = (q.value||"").trim(); if (!question||!sample) return;
  const ctl = new AbortController(); asks[key]={ctl,q:question,text:""};
  go.disabled=true; stop.hidden=false; save.hidden=true; note.textContent=""; out.textContent="Pensando...";
  try {
    const r = await sample(RULES + contextFor(key) + `\nPergunta de alguém do time: ${question}`, {signal:ctl.signal, cache:false, onText:({text})=>{ out.textContent=text; asks[key].text=text; }});
    asks[key].text = r.text; out.textContent = r.text; save.hidden=false;
    if (r.truncated) note.textContent="Resposta cortada no limite. Pergunte em partes menores.";
  } catch(err){
    const c = err && err.code;
    out.textContent = err && err.text ? err.text : "";
    if (c==="cancelled") note.textContent="Interrompido.";
    else if (c==="not_granted"||c==="sampling_disabled"||c==="not_declared"||c==="capability_disabled"){ note.textContent="O Claude não está liberado nesta visualização."; sample=null; }
    else if (c==="rate_limited") note.textContent="Muitas perguntas por agora. Tente de novo em alguns minutos.";
    else if (c==="refused") note.textContent="O Claude não respondeu a essa pergunta. Reformule.";
    else note.textContent="Falhou no meio. Tente de novo.";
    if (asks[key].text) save.hidden=false;
  } finally { go.disabled=false; stop.hidden=true; }
}

/* conversa geral sobre o Haven */
const chat = {turns:[], ctl:null};
function edicaoResumo(){
  const d = RADAR.dias.find(x=>x.data===state.day) || RADAR.dias[0];
  let t = `\nEdição de hoje (${d.data}).\nManchete: ${d.manchete}\nEditorial: ${d.editorial}\nPra prestar atenção: ${(d.atencao||[]).join(" | ")}\nBench pro Haven: ${(d.bench||[]).map((b,i)=>`${i+1}. [${b.area}] ${b.ideia}`).join(" ")}\nItens: ${(d.itens||[]).map(i=>`${i.title} (${i.source}, ${i.date})`).join("; ")}\n`;
  const pend = shared.pautas.filter(p=>p.status!=="respondida").slice(0,8).map(p=>"- "+p.texto).join("\n");
  if (pend) t += `\nPautas abertas do time:\n${pend}\n`;
  return t;
}
function chatRender(){
  const log = document.getElementById("chat-log");
  log.innerHTML = chat.turns.map(t=>`<div class="msg ${t.role==="user"?"me":"ai"}"><i>${t.role==="user"?esc(meName||"você"):"Claude"}</i>${esc(t.content)}</div>`).join("");
  document.getElementById("chat-clear").hidden = !chat.turns.length;
}
document.getElementById("chat-clear").addEventListener("click", ()=>{ chat.turns=[]; chatRender(); });
document.getElementById("chat-stop").addEventListener("click", ()=>{ chat.ctl?.abort(); });
document.getElementById("chat-form").addEventListener("submit", async e => {
  e.preventDefault(); if (!sample) return;
  const ta = document.getElementById("chat-txt"); const q = ta.value.trim(); if (!q) return;
  const btn=document.getElementById("chat-btn"), stop=document.getElementById("chat-stop"), note=document.getElementById("chat-note");
  chat.turns.push({role:"user", content:q}); ta.value=""; chatRender();
  const live = document.createElement("div"); live.className="msg ai"; live.innerHTML="<i>Claude</i>Pensando..."; document.getElementById("chat-log").appendChild(live);
  btn.disabled=true; stop.hidden=false; note.textContent="";
  chat.ctl = new AbortController();
  const input = [{role:"user", content: RULES + BRIEF + edicaoResumo() + "\nA conversa abaixo é com uma pessoa do time do Haven. Responda à última mensagem."}, ...chat.turns.slice(-12)];
  try {
    const r = await sample(input, {cache:false, signal:chat.ctl.signal, onText:({text})=>{ live.innerHTML="<i>Claude</i>"+esc(text); }});
    chat.turns.push({role:"assistant", content:r.text}); chatRender();
    if (r.truncated) note.textContent="Resposta cortada no limite. Pergunte em partes.";
  } catch(err){
    const c = err && err.code; live.remove();
    if (err && err.text) { chat.turns.push({role:"assistant", content:err.text}); chatRender(); }
    if (c==="cancelled") note.textContent="Interrompido.";
    else if (c==="not_granted"||c==="sampling_disabled"||c==="not_declared"||c==="capability_disabled"){ note.textContent="O Claude não está liberado nesta visualização."; sample=null; document.getElementById("chat").hidden=true; }
    else if (c==="rate_limited") note.textContent="Muitas perguntas por agora. Tente em alguns minutos.";
    else if (c==="refused") note.textContent="O Claude não respondeu a essa. Reformule.";
    else note.textContent="Falhou no meio. Tente de novo.";
  } finally { btn.disabled=false; stop.hidden=true; }
});

/* liga as capacidades */
render();
(async () => {
  const [u, d, s] = await Promise.all([claude.use("user"), claude.use("db"), claude.use("sample")]);
  user=u; db=d; sample=s;
  if (sample) document.getElementById("chat").hidden=false;
  if (user){ const me = await user.me(); uid = me.id; meName = me.name; canWrite = await user.can("data.write");
    document.getElementById("me").innerHTML = uid ? `Você: <b>${esc(meName||"sem nome")}</b>` : ""; }
  if (!db || !uid || canWrite===false){ canWrite=false; document.getElementById("ro").hidden=false; }
  if (db){
    const onErr = e => { if (e && e.code==="revoked") onWriteError(e); };
    db.collection("votos").onSnapshot(snap => { shared.votos={}; snap.docs.forEach(x=>{ if(x.exists) shared.votos[x.id]=x.data(); }); render(); }, onErr);
    db.collection("comentarios").onSnapshot(snap => { shared.comentarios=snap.docs.filter(x=>x.exists).map(x=>({id:x.id,...x.data()})); render(); }, onErr);
    db.collection("pautas").onSnapshot(snap => { shared.pautas=snap.docs.filter(x=>x.exists).map(x=>({id:x.id,...x.data()})); render(); }, onErr);
    db.collection("ideias").onSnapshot(snap => { shared.ideias={}; snap.docs.forEach(x=>{ if(x.exists) shared.ideias[x.id]=x.data(); }); render(); }, onErr);
  } else render();
})();
</script>
"""

out = TEMPLATE.replace("__CSS__", css + EXTRA_CSS).replace("__DATA__", data_js)
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
open(dest, "w", encoding="utf-8").write(out)
print("sala gerada:", dest, len(out), "bytes")
