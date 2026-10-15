#!/usr/bin/env python3
"""Gera index.html do Daily Haven Bench News a partir de radar-data.json.
Uso: python3 build.py  (lê radar-data.json e escreve index.html no mesmo diretório)
Layout: revista Haven. Paleta do brandbook, serifa de revista, grade de jornal.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "radar-data.json"), encoding="utf-8"))
data_js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")

TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Daily Haven Bench News</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
<style>
  :root{
    --ivory:#ECE8E4;--paper:#F4F1ED;--espresso:#3F3832;--ink:#2B2622;--soft:#5B544D;--mute:#857D74;--sand:#C3BFA8;
    --terracotta:#C75937;--ochre:#DA9321;--teal:#45958D;--plum:#74386B;--forest:#2F6400;--pine:#174900;
    --rule:rgba(63,56,50,.18);--rule-strong:var(--espresso);
    --p-wellness-residence:var(--forest);--p-membership:var(--terracotta);--p-longevidade:var(--teal);--p-lifestyle:var(--plum);
    --p-comunidade:var(--ochre);--p-estudos:var(--pine);--p-eventos:var(--espresso);--p-marcas:var(--sand);
    --serif:'Playfair Display',Georgia,'TeX Gyre Pagella','Times New Roman',serif;--serif2:'Cormorant Garamond',Georgia,'TeX Gyre Pagella',serif;--sans:'Helvetica Neue',Helvetica,'TeX Gyre Heros',Arial,system-ui,sans-serif;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{background:var(--ivory)}
  body{background:var(--ivory);color:var(--ink);font-family:var(--sans);line-height:1.5;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
  a{color:inherit;text-decoration:none}
  a:focus-visible,button:focus-visible,select:focus-visible{outline:2px solid var(--terracotta);outline-offset:3px}
  .page{max-width:1280px;margin:0 auto;padding:22px 16px 72px}
  @media(min-width:760px){.page{padding:30px 44px 96px}}

  /* masthead */
  .mast{text-align:center;border-top:1px solid var(--rule-strong);border-bottom:1px solid var(--rule-strong);position:relative;padding:14px 0 12px}
  .mast:before{content:"";position:absolute;left:0;right:0;top:3px;border-top:1px solid var(--rule-strong)}
  .mast:after{content:"";position:absolute;left:0;right:0;bottom:3px;border-bottom:1px solid var(--rule-strong)}
  .mast h1{font-family:var(--serif);font-weight:500;font-size:40px;line-height:1;letter-spacing:-.01em;margin:8px 0 10px}
  @media(max-width:759px){.mast .kicker{font-size:9.5px;letter-spacing:.2em}}
  @media(min-width:760px){.mast h1{font-size:64px}}
  @media(min-width:1100px){.mast h1{font-size:76px}}
  .kicker{font-family:var(--sans);font-size:11px;letter-spacing:.26em;text-transform:uppercase;color:var(--espresso)}
  .folio{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid var(--rule);font-size:11.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--soft)}
  .folio select{font:inherit;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);background:transparent;border:0;border-bottom:1px solid var(--ink);padding:1px 18px 1px 0;cursor:pointer;-webkit-appearance:none;appearance:none;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'><path d='M1 1l4 4 4-4' fill='none' stroke='%232B2622' stroke-width='1.2'/></svg>");background-repeat:no-repeat;background-position:right 2px center}

  /* seções de navegação (filtros) */
  .nav{display:flex;flex-direction:column;gap:6px;padding:10px 0;border-bottom:1px solid var(--rule)}
  @media(min-width:960px){.nav{flex-direction:row;gap:34px;align-items:center}}
  .nav .grp{display:flex;align-items:center;gap:0 14px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch;padding-bottom:2px}
  .nav .grp::-webkit-scrollbar{display:none}
  @media(min-width:960px){.nav .grp{flex-wrap:wrap;overflow:visible}}
  .nav .lbl{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);margin-right:6px;flex:none}
  .nav button{font-family:var(--serif2);font-size:16.5px;font-weight:500;background:none;border:0;color:var(--soft);cursor:pointer;padding:6px 0;border-bottom:2px solid transparent;line-height:1;white-space:nowrap;flex:none}
  .nav button:hover{color:var(--ink)}
  .nav button.on{color:var(--ink);border-bottom-color:var(--terracotta)}
  .nav .n{margin-left:auto;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);white-space:nowrap}

  /* abertura */
  .open{display:grid;grid-template-columns:1fr;gap:28px;padding:30px 0 34px;border-bottom:1px solid var(--rule-strong)}
  @media(min-width:960px){.open{grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:56px;padding:40px 0 44px}}
  .open .manchete{font-family:var(--serif);font-weight:500;font-size:34px;line-height:1.1;letter-spacing:-.012em;color:var(--ink)}
  @media(min-width:760px){.open .manchete{font-size:50px}}
  @media(min-width:1100px){.open .manchete{font-size:58px}}
  .open .editorial{font-family:var(--serif2);font-size:20px;line-height:1.5;color:var(--espresso);margin-top:22px;max-width:66ch}
  .open .editorial::first-letter{font-family:var(--serif);font-size:3.1em;line-height:.82;float:left;padding:6px 10px 0 0;color:var(--terracotta)}
  .open .tally{margin-top:20px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}
  .watch{border-top:3px solid var(--terracotta);padding-top:14px;align-self:start}
  @media(min-width:960px){.watch{border-left:1px solid var(--rule);border-top:0;padding:4px 0 0 34px}}
  .watch h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:24px;line-height:1.1;margin:0 0 6px}
  @media(min-width:960px){.watch h2{font-size:28px}}
  .watch ol{list-style:none;counter-reset:w}
  .watch li{counter-increment:w;display:grid;grid-template-columns:30px 1fr;gap:10px;padding:16px 0;border-top:1px solid var(--rule);font-family:var(--serif2);font-size:18px;line-height:1.42;color:var(--espresso)}
  .watch li:first-child{border-top:0;padding-top:12px}
  .watch li:before{content:counter(w,decimal-leading-zero);font-family:var(--sans);font-size:11px;letter-spacing:.14em;color:var(--terracotta);padding-top:7px}
  .watch li b{font-family:var(--sans);font-weight:600;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--ink);display:block;margin-bottom:5px}

  /* seções */
  .sec{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin:34px 0 0;padding-bottom:8px;border-bottom:1px solid var(--rule-strong)}
  .sec h2{font-family:var(--sans);font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--ink)}
  .sec span{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute)}

  /* destaques: grade com fios */
  .grid{display:grid;grid-template-columns:1fr;gap:0}
  @media(min-width:700px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(min-width:1100px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
  .art{padding:26px 0 28px;border-bottom:1px solid var(--rule);display:flex;flex-direction:column;gap:12px;position:relative}
  @media(min-width:700px){.art{padding:28px 28px 32px}.art:nth-child(2n){border-left:1px solid var(--rule)}.art:nth-child(2n+1){padding-left:0}.art:nth-child(2n){padding-right:0}}
  @media(min-width:1100px){.art:nth-child(n){padding:28px 28px 32px;border-left:1px solid var(--rule)}.art:nth-child(3n+1){border-left:0;padding-left:0}.art:nth-child(3n){padding-right:0}}
  .art .tag{display:flex;justify-content:space-between;gap:10px;align-items:center;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink)}
  .art .tag:before{content:"";display:inline-block;width:26px;height:3px;background:var(--pc,var(--espresso));margin-right:10px;vertical-align:middle;flex:none}
  .art .tag span{margin-left:auto;color:var(--mute);letter-spacing:.14em;font-weight:400;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:58%}
  .art h3{font-family:var(--serif);font-weight:500;font-size:25px;line-height:1.18;letter-spacing:-.005em}
  .art h3 a:hover{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
  .art .txt{font-family:var(--serif2);font-size:17.5px;line-height:1.45;color:var(--espresso)}
  .art .use{font-family:var(--serif2);font-size:16.5px;line-height:1.42;color:var(--ink);padding:10px 0 2px 14px;border-left:2px solid var(--terracotta)}
  .art .use i{font-family:var(--sans);font-style:normal;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--terracotta);display:block;margin-bottom:5px}
  .art .foot{margin-top:auto;padding-top:10px;display:flex;flex-direction:column;gap:5px;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
  .art .foot a{color:var(--soft);border-bottom:1px solid var(--rule)}
  .art .foot a:hover{color:var(--ink);border-bottom-color:var(--ink)}
  .p-wellness-residence{--pc:var(--p-wellness-residence)}.p-membership{--pc:var(--p-membership)}.p-longevidade{--pc:var(--p-longevidade)}.p-lifestyle{--pc:var(--p-lifestyle)}
  .p-comunidade{--pc:var(--p-comunidade)}.p-estudos{--pc:var(--p-estudos)}.p-eventos{--pc:var(--p-eventos)}.p-marcas{--pc:var(--p-marcas)}

  /* em pauta: lista compacta em colunas */
  .pauta{columns:1;column-gap:48px;column-rule:1px solid var(--rule)}
  @media(min-width:760px){.pauta{columns:2}}
  @media(min-width:1100px){.pauta{columns:3}}
  .brief{break-inside:avoid;padding:18px 0;border-bottom:1px solid var(--rule);display:flex;flex-direction:column;gap:7px}
  .brief .tag{display:flex;align-items:center;gap:10px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink)}
  .brief .tag:before{content:"";display:inline-block;width:18px;height:3px;background:var(--pc,var(--espresso));flex:none}
  .brief .tag span{color:var(--mute);letter-spacing:.14em;margin-left:auto;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:55%}
  .brief h3{font-family:var(--serif);font-weight:500;font-size:19.5px;line-height:1.22}
  .brief h3 a:hover{text-decoration:underline;text-underline-offset:4px;text-decoration-thickness:1px}
  .brief .use{font-family:var(--serif2);font-size:16px;line-height:1.42;color:var(--espresso)}
  .brief .foot{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--mute)}
  .brief .foot a{color:var(--soft);border-bottom:1px solid var(--rule)}
  .brief .foot a:hover{color:var(--ink)}

  .empty{padding:48px 0;font-family:var(--serif2);font-size:19px;color:var(--mute)}
  footer{margin-top:56px;padding-top:14px;border-top:1px solid var(--rule-strong);display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:12.5px;line-height:1.6;color:var(--mute)}
  footer p{max-width:70ch}
  footer .sig{font-family:var(--serif);font-style:italic;font-size:18px;color:var(--espresso)}
</style>
</head>
<body>
<div class="page">
  <header class="mast">
    <div class="kicker">Radar diário de wellness residences, membership, longevidade e lifestyle</div>
    <h1>Daily Haven Bench News</h1>
    <div class="kicker">Pra parcerias, marketing, vendas e clube</div>
  </header>
  <div class="folio">
    <span id="folio-left"></span>
    <span><label for="day" style="margin-right:8px">Edição</label><select id="day" aria-label="Escolher edição"></select></span>
    <span id="tally"></span>
  </div>

  <nav class="nav" aria-label="Filtros">
    <div class="grp" data-f="para"><span class="lbl">Pra quem</span><button class="on" data-v="">Tudo</button><button data-v="parcerias">Parcerias</button><button data-v="marketing">Marketing</button><button data-v="vendas">Vendas</button><button data-v="clube">Clube</button></div>
    <div class="grp" data-f="escopo"><span class="lbl">Onde</span><button class="on" data-v="">Tudo</button><button data-v="brasil">Brasil</button><button data-v="mundo">Mundo</button></div>
    <div class="grp" data-f="pilar"><span class="lbl">Pilar</span><button class="on" data-v="">Todos</button><button data-v="wellness-residence">Wellness residence</button><button data-v="membership">Membership</button><button data-v="longevidade">Longevidade</button><button data-v="comunidade">Comunidade</button><button data-v="lifestyle">Lifestyle</button><button data-v="estudos">Estudos</button><button data-v="eventos">Eventos</button><button data-v="marcas">Marcas</button></div>
    <span class="n" id="count"></span>
  </nav>

  <main id="main"></main>

  <footer>
    <p>Cada item foi aberto e conferido na fonte no dia da edição. Conteúdo patrocinado está marcado junto ao veículo. O radar roda toda manhã e manda um resumo por email; as edições anteriores ficam no seletor do topo.</p>
    <span class="sig">Bru</span>
  </footer>
</div>
<script>
const RADAR = __DATA__;
const PILAR = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade","estudos":"Estudos","eventos":"Eventos","marcas":"Marcas"};
const M=["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"];
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const W=["domingo","segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtLong = d => { const [y,m,dd]=d.split("-").map(Number); const w=new Date(Date.UTC(y,m-1,dd)).getUTCDay(); return `${W[w]}, ${dd} de ${M[m-1]} de ${y}`; };
const fmtSel = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]} ${y}`; };
const fmtShort = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${MS[+m-1]}`; };
const state = {day: RADAR.dias[0].data, escopo:"", pilar:"", para:""};

const sel = document.getElementById("day");
RADAR.dias.forEach(d => { const o=document.createElement("option"); o.value=d.data; o.textContent=fmtSel(d.data); sel.appendChild(o); });
sel.addEventListener("change", e => { state.day=e.target.value; render(); });
document.querySelectorAll(".grp[data-f]").forEach(g => g.querySelectorAll("button").forEach(b => b.addEventListener("click", () => {
  g.querySelectorAll("button").forEach(x=>x.classList.remove("on")); b.classList.add("on"); state[g.dataset.f]=b.dataset.v; render();
})));

const tagHtml = i => `<div class="tag">${esc(PILAR[i.pilar]||i.pilar)}<span>${i.escopo==="brasil"?"Brasil":"Mundo"} · ${esc(i.region||"")}</span></div>`;
const artHtml = i => `
  <article class="art p-${esc(i.pilar)}">
    ${tagHtml(i)}
    <h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3>
    <p class="txt">${esc(i.resumo)}</p>
    <div class="use"><i>O que o Haven faz com isso</i>${esc(i.por_que_importa)}</div>
    <div class="foot"><span><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)}</span><span>${(i.para||[]).map(esc).join(" · ")}</span></div>
  </article>`;
const briefHtml = i => `
  <article class="brief p-${esc(i.pilar)}">
    ${tagHtml(i)}
    <h3><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3>
    <p class="use">${esc(i.por_que_importa)}</p>
    <div class="foot"><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a> · ${fmtShort(i.date)} · ${(i.para||[]).map(esc).join(" · ")}</div>
  </article>`;
const splitWatch = a => { const m = String(a).match(/^([^:]{2,24}):\s*(.*)$/s); return m ? `<span><b>${esc(m[1])}</b>${esc(m[2])}</span>` : `<span>${esc(a)}</span>`; };

function render(){
  const idx = RADAR.dias.findIndex(d=>d.data===state.day);
  const day = RADAR.dias[idx] || RADAR.dias[0];
  const num = RADAR.dias.length - (idx<0?0:idx);
  const items = day.itens || [];
  const br=items.filter(i=>i.escopo==="brasil").length;
  document.getElementById("folio-left").textContent = `Nº ${num} · ${fmtLong(day.data)}`;
  document.getElementById("tally").textContent = `${items.length} itens conferidos · ${br} Brasil · ${items.length-br} mundo`;
  const list = items.filter(i => (!state.escopo||i.escopo===state.escopo) && (!state.pilar||i.pilar===state.pilar) && (!state.para||(i.para||[]).includes(state.para)));
  document.getElementById("count").textContent = `${list.length} de ${items.length}`;
  const unfiltered = !state.escopo && !state.pilar && !state.para;
  const leads = list.filter(i=>i.destaque);
  const rest = list.filter(i=>!i.destaque);
  const restBr = rest.filter(i=>i.escopo==="brasil"), restWd = rest.filter(i=>i.escopo==="mundo");
  let html = "";
  if (unfiltered) html += `
    <section class="open">
      <div><h2 class="manchete">${esc(day.manchete||"")}</h2><p class="editorial">${esc(day.editorial||"")}</p><div class="tally">${items.length} itens conferidos na fonte · ${br} do Brasil · ${items.length-br} do mundo</div></div>
      <aside class="watch"><h2>Pra prestar atenção</h2><ol>${(day.atencao||[]).map(a=>`<li>${splitWatch(a)}</li>`).join("")}</ol></aside>
    </section>`;
  if (leads.length) html += `<div class="sec"><h2>Destaques</h2><span>o que merece leitura inteira</span></div><div class="grid">${leads.map(artHtml).join("")}</div>`;
  if (unfiltered) {
    if (restBr.length) html += `<div class="sec"><h2>Em pauta · Brasil</h2><span>${restBr.length} ${restBr.length>1?"itens":"item"}</span></div><div class="pauta">${restBr.map(briefHtml).join("")}</div>`;
    if (restWd.length) html += `<div class="sec"><h2>Em pauta · Mundo</h2><span>${restWd.length} ${restWd.length>1?"itens":"item"}</span></div><div class="pauta">${restWd.map(briefHtml).join("")}</div>`;
  } else if (rest.length) {
    html += `<div class="sec"><h2>Em pauta</h2><span>${rest.length} ${rest.length>1?"itens":"item"}</span></div><div class="pauta">${rest.map(briefHtml).join("")}</div>`;
  }
  if (!list.length) html += `<div class="empty">Nenhum item com esses filtros. Escolha outro pilar ou volte pra tudo.</div>`;
  document.getElementById("main").innerHTML = html;
}
render();
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__DATA__", data_js)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("index.html gerado:", len(out), "bytes;", sum(len(d["itens"]) for d in data["dias"]), "itens em", len(data["dias"]), "edição(ões)")
