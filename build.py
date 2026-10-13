#!/usr/bin/env python3
"""Gera index.html do Daily Haven Bench News a partir de radar-data.json.
Uso: python3 build.py  (lê radar-data.json e escreve index.html no mesmo diretório)
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
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
  :root{--bg:#EDE9E0;--card:#FBF9F5;--ink:#1C1A17;--soft:#45423C;--mute:#6B675F;--rule:rgba(28,26,23,.12);--green:#2F4634;--green-ink:#3E5A42;
    --p-wellness-residence:#3E5A42;--p-membership:#8A6A3F;--p-longevidade:#4A5A7A;--p-lifestyle:#7A4A5A;--p-comunidade:#5A6A4A}
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:var(--bg);color:var(--ink);font-family:'Manrope',system-ui,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}
  .serif{font-family:'Marcellus',serif;font-weight:400}
  a{color:inherit;text-decoration:none}
  a:focus-visible,button:focus-visible,select:focus-visible{outline:2px solid var(--green-ink);outline-offset:3px}
  .page{max-width:1240px;margin:0 auto;padding:24px 16px 64px}
  @media(min-width:760px){.page{padding:32px 40px 80px}}

  .top{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;flex-wrap:wrap;margin-bottom:22px}
  .top h1{font-size:30px;line-height:1}
  @media(min-width:760px){.top h1{font-size:36px}}
  .top .sub{font-size:13.5px;color:var(--mute);margin-top:8px;display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
  .top select{font-family:'Marcellus',serif;font-size:15px;color:var(--ink);background:transparent;border:0;border-bottom:1px solid var(--ink);padding:1px 0;cursor:pointer;-webkit-appearance:none;appearance:none}

  .chips{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
  .chips .lbl{font-size:12.5px;color:var(--mute);margin-right:2px}
  .chip{font:inherit;font-size:13px;padding:8px 14px;border:1px solid rgba(28,26,23,.3);background:transparent;color:var(--soft);border-radius:999px;cursor:pointer;min-height:36px}
  .chip:hover{border-color:var(--ink)}
  .chip.on{background:var(--ink);color:#F5F1EA;border-color:var(--ink)}
  .chip.p-wellness-residence.on{background:var(--p-wellness-residence);border-color:var(--p-wellness-residence)}
  .chip.p-membership.on{background:var(--p-membership);border-color:var(--p-membership)}
  .chip.p-longevidade.on{background:var(--p-longevidade);border-color:var(--p-longevidade)}
  .chip.p-lifestyle.on{background:var(--p-lifestyle);border-color:var(--p-lifestyle)}
  .chip.p-comunidade.on{background:var(--p-comunidade);border-color:var(--p-comunidade)}
  .filterbar{display:flex;flex-direction:column;gap:10px;padding:14px 0 18px;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:18px}
  @media(min-width:900px){.filterbar{flex-direction:row;gap:26px;align-items:center;flex-wrap:wrap}}
  .filterbar .n{font-size:12.5px;color:var(--mute);margin-left:auto}

  .grid{display:grid;grid-template-columns:1fr;gap:16px;align-items:start}
  @media(min-width:700px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(min-width:1040px){.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}

  .lead{background:var(--green);color:#F5F1EA;padding:28px 30px;border-radius:4px;display:flex;flex-direction:column;gap:14px}
  @media(min-width:700px){.lead{grid-column:span 2}}
  .lead h2{font-size:28px;line-height:1.12}
  @media(min-width:760px){.lead h2{font-size:36px}}
  .lead p{font-size:15px;line-height:1.65;opacity:.92;max-width:70ch}
  .watch{background:var(--card);padding:22px 24px;border-radius:4px;border-top:4px solid var(--green);display:flex;flex-direction:column;gap:10px}
  .watch h2{font-size:19px}
  .watch div{font-size:13.5px;line-height:1.55;color:var(--soft);padding-top:10px;border-top:1px solid var(--rule)}

  .card{background:var(--card);padding:22px 24px 18px;border-radius:4px;border-top:4px solid var(--green-ink);display:flex;flex-direction:column;gap:10px}
  .card.p-wellness-residence{border-top-color:var(--p-wellness-residence)}
  .card.p-membership{border-top-color:var(--p-membership)}
  .card.p-longevidade{border-top-color:var(--p-longevidade)}
  .card.p-lifestyle{border-top-color:var(--p-lifestyle)}
  .card.p-comunidade{border-top-color:var(--p-comunidade)}
  .card .kick{font-size:12.5px;font-weight:600;display:flex;justify-content:space-between;gap:8px}
  .card .kick span{font-weight:400;color:var(--mute)}
  .card.p-wellness-residence .kick{color:var(--p-wellness-residence)}
  .card.p-membership .kick{color:var(--p-membership)}
  .card.p-longevidade .kick{color:var(--p-longevidade)}
  .card.p-lifestyle .kick{color:var(--p-lifestyle)}
  .card.p-comunidade .kick{color:var(--p-comunidade)}
  .card h3{font-size:21px;line-height:1.25}
  .card h3 a:hover{text-decoration:underline;text-underline-offset:4px}
  .card .txt{font-size:13.5px;line-height:1.6;color:var(--soft)}
  .card .use{font-size:13.5px;line-height:1.6;color:var(--ink);padding:10px 12px;background:rgba(62,90,66,.07)}
  .card .use i{font-family:'Marcellus',serif;font-style:normal;color:var(--green-ink)}
  .card .foot{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;font-size:12px;color:var(--mute);padding-top:8px;border-top:1px solid var(--rule)}
  .card .foot a{text-decoration:underline;text-underline-offset:3px}
  .card.hl{box-shadow:0 0 0 1px var(--green-ink)}
  .empty{grid-column:1/-1;padding:40px 0;color:var(--mute);font-size:14px}
  footer{margin-top:48px;font-size:12.5px;color:var(--mute);line-height:1.7;max-width:72ch}
</style>
</head>
<body>
<div class="page">
  <header class="top">
    <div>
      <h1 class="serif">Daily Haven Bench News</h1>
      <div class="sub"><span>Edição de</span><select id="day" aria-label="Escolher edição"></select><span id="tally"></span></div>
    </div>
    <div class="chips" data-f="para"><span class="lbl">Pra quem</span><button class="chip on" data-v="">tudo</button><button class="chip" data-v="parcerias">parcerias</button><button class="chip" data-v="marketing">marketing</button><button class="chip" data-v="vendas">vendas</button><button class="chip" data-v="clube">clube</button></div>
  </header>

  <div class="filterbar">
    <div class="chips" data-f="escopo"><span class="lbl">Onde</span><button class="chip on" data-v="">tudo</button><button class="chip" data-v="brasil">Brasil</button><button class="chip" data-v="mundo">mundo</button></div>
    <div class="chips" data-f="pilar"><span class="lbl">Pilar</span><button class="chip on" data-v="">todos</button><button class="chip p-wellness-residence" data-v="wellness-residence">wellness residence</button><button class="chip p-membership" data-v="membership">membership</button><button class="chip p-longevidade" data-v="longevidade">longevidade</button><button class="chip p-comunidade" data-v="comunidade">comunidade</button><button class="chip p-lifestyle" data-v="lifestyle">lifestyle</button></div>
    <span class="n" id="count"></span>
  </div>

  <div class="grid" id="grid"></div>

  <footer>Cada item foi aberto e conferido na fonte no dia da edição. Conteúdo patrocinado está marcado junto ao veículo. O radar roda toda manhã e manda um resumo por email; as edições anteriores ficam no seletor do topo.</footer>
</div>
<script>
const RADAR = __DATA__;
const PILAR = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade"};
const M=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = d => { const [y,m,dd]=d.split("-"); return `${+dd} de ${M[+m-1]} de ${y}`; };
const fmtShort = d => { const [y,m,dd]=d.split("-"); return `${+dd} ${M[+m-1]}`; };
const state = {day: RADAR.dias[0].data, escopo:"", pilar:"", para:""};

const sel = document.getElementById("day");
RADAR.dias.forEach(d => { const o=document.createElement("option"); o.value=d.data; o.textContent=fmt(d.data); sel.appendChild(o); });
sel.addEventListener("change", e => { state.day=e.target.value; render(); });
document.querySelectorAll(".chips[data-f]").forEach(g => g.querySelectorAll(".chip").forEach(b => b.addEventListener("click", () => {
  g.querySelectorAll(".chip").forEach(x=>x.classList.remove("on")); b.classList.add("on"); state[g.dataset.f]=b.dataset.v; render();
})));

function render(){
  const day = RADAR.dias.find(d=>d.data===state.day) || RADAR.dias[0];
  const items = day.itens || [];
  const br=items.filter(i=>i.escopo==="brasil").length;
  document.getElementById("tally").textContent = `${items.length} itens conferidos, ${br} do Brasil e ${items.length-br} do mundo`;
  const list = items.filter(i => (!state.escopo||i.escopo===state.escopo) && (!state.pilar||i.pilar===state.pilar) && (!state.para||(i.para||[]).includes(state.para)))
    .sort((a,b)=> (b.destaque?1:0)-(a.destaque?1:0) || b.date.localeCompare(a.date));
  document.getElementById("count").textContent = `${list.length} de ${items.length}`;
  const unfiltered = !state.escopo && !state.pilar && !state.para;
  const head = unfiltered ? `
    <section class="lead"><h2 class="serif">${esc(day.manchete||"")}</h2><p>${esc(day.editorial||"")}</p></section>
    <aside class="watch"><h2 class="serif">Pra prestar atenção</h2>${(day.atencao||[]).map(a=>`<div>${esc(a)}</div>`).join("")}</aside>` : "";
  const cards = list.map(i => `
    <article class="card p-${esc(i.pilar)} ${i.destaque?'hl':''}">
      <div class="kick">${esc(PILAR[i.pilar]||i.pilar)}<span>${i.escopo==="brasil"?"Brasil":"Mundo"}, ${esc(i.region||"")}</span></div>
      <h3 class="serif"><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)}</a></h3>
      <p class="txt">${esc(i.resumo)}</p>
      <div class="use"><i>O que o Haven faz com isso. </i>${esc(i.por_que_importa)}</div>
      <div class="foot"><span><a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.source)}</a>, ${fmtShort(i.date)}</span><span>${(i.para||[]).map(esc).join(", ")}</span></div>
    </article>`).join("");
  document.getElementById("grid").innerHTML = head + (cards || '<div class="empty">Nenhum item com esses filtros. Escolha outro pilar ou veja tudo.</div>');
}
render();
</script>
</body>
</html>
"""

out = TEMPLATE.replace("__DATA__", data_js)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(out)
print("index.html gerado:", len(out), "bytes;", sum(len(d["itens"]) for d in data["dias"]), "itens em", len(data["dias"]), "edição(ões)")
