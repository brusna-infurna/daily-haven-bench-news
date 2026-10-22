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
  .bs-tabs{display:flex;gap:6px;flex-wrap:wrap;padding:10px 0 14px;border-bottom:1px solid var(--rule-strong)}
  .bs-tabs button{font-family:var(--sans);font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:600;background:transparent;border:1px solid var(--rule);color:var(--soft);padding:8px 12px;cursor:pointer}
  .bs-tabs button.on{background:var(--espresso);color:var(--paper);border-color:var(--espresso)}
  .bs-tabs button em{font-style:normal;font-variant-numeric:tabular-nums;margin-left:6px;opacity:.75}
  .bs-grid{display:grid;grid-template-columns:1fr;gap:22px;padding-top:22px}
  @media(min-width:1100px){.bs-grid{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.bs-tabs{display:none}}
  @media(max-width:1099px){.bs-col{display:none}.bs-col.on{display:flex}}
  .bs-col{display:flex;flex-direction:column;background:var(--paper);border:1px solid var(--rule);border-top:3px solid var(--terracotta);min-height:520px;max-height:78vh}
  .bs-col.a-vendas{border-top-color:var(--forest)} .bs-col.a-membership{border-top-color:var(--terracotta)} .bs-col.a-parcerias{border-top-color:var(--teal)} .bs-col.a-marketing{border-top-color:var(--plum)}
  .bs-col h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:22px;line-height:1.1;padding:14px 16px 8px;border-bottom:1px solid var(--rule)}
  .bs-col h2 small{display:block;font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin-top:6px}
  .bs-feed{flex:1 1 auto;overflow-y:auto;padding:6px 16px 10px;display:flex;flex-direction:column;gap:12px;scroll-behavior:smooth}
  .bs-msg{font-family:var(--serif2);font-size:16.5px;line-height:1.42;color:var(--espresso);padding:8px 0 10px;border-bottom:1px solid var(--rule);white-space:pre-wrap;word-break:break-word}
  .bs-msg.me{color:var(--ink)}
  .bs-msg .who{font-family:var(--sans);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);margin-bottom:4px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;white-space:normal}
  .bs-msg .who b{color:var(--ink);font-weight:700}
  .bs-msg .ref{display:block;font-family:var(--sans);font-size:11px;color:var(--mute);margin-top:6px;white-space:normal}
  .bs-msg .ref a{text-decoration:underline;color:var(--soft)}
  .bs-msg .apagar{font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;background:none;border:0;color:var(--mute);cursor:pointer;padding:0}
  .bs-msg .apagar:hover{color:var(--terracotta)}
  .bs-vazio{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute);padding:16px 0}
  .bs-form{padding:10px 16px 14px;border-top:1px solid var(--rule);display:flex;flex-direction:column;gap:8px;background:var(--paper)}
  .bs-form textarea{min-height:52px}
  .bs-form .row{justify-content:space-between}
  .bs-form .hint{font-family:var(--sans);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
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
    <p class="bs-intro">Quatro mesas, uma por área. Entram aqui os comentários que o time deixa nos itens da sala, já separados pela área do item, e o que for escrito direto nestas mesas. Tudo aparece na hora pra quem estiver com a página aberta.</p>
    <nav class="bs-tabs" id="tabs" aria-label="Áreas"></nav>
    <div class="bs-grid" id="grid"></div>
  </div>

  <footer>
    <p>Cada mensagem traz autor, edição do Bench a que se refere e hora. A Bru lê este quadro na rotina da manhã. A sala do time fica em <a href="../sala/" style="text-decoration:underline">benchnews/sala</a>.</p>
    <span class="sig">Bru</span>
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
let me = "", isAdmin = false, tab = "vendas";
const data = {brainstorm:[], comentarios:[]};

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
  montar(); await carregar(); assinar(); setInterval(carregar, 30000);
}
function montar(){
  $("tabs").innerHTML = AREAS.map(([k,l]) => `<button data-a="${k}" class="${k===tab?'on':''}">${esc(l)}<em id="n-${k}"></em></button>`).join("");
  $("tabs").addEventListener("click", e => { const b=e.target.closest("button"); if(!b) return; tab=b.dataset.a; document.querySelectorAll(".bs-tabs button").forEach(x=>x.classList.toggle("on",x.dataset.a===tab)); document.querySelectorAll(".bs-col").forEach(c=>c.classList.toggle("on",c.dataset.a===tab)); });
  $("grid").innerHTML = AREAS.map(([k,l,sub]) => `
    <section class="bs-col a-${k} ${k===tab?'on':''}" data-a="${k}">
      <h2>${esc(l)}<small>${esc(sub)} e conversa direta</small></h2>
      <div class="bs-feed" id="feed-${k}"></div>
      <form class="bs-form" data-a="${k}"><textarea rows="2" placeholder="Escreva pra mesa de ${esc(l)}"></textarea><div class="row"><span class="hint">assina como ${esc(me)}</span><button class="btn sm" type="submit">Enviar</button></div></form>
    </section>`).join("");
  $("grid").addEventListener("submit", async e => {
    e.preventDefault(); const f=e.target; const ta=f.querySelector("textarea"); const txt=ta.value.trim(); if(!txt) return;
    const btn=f.querySelector("button"); btn.disabled=true;
    const edicao = (RADAR.dias && RADAR.dias[0]) ? RADAR.dias[0].data : null;
    const { error } = await sb.from("brainstorm").insert({area:f.dataset.a, autor:me, texto:txt, edicao});
    btn.disabled=false; if (error) { note("Não deu pra enviar: " + (error.message||"erro")); return; }
    ta.value=""; await carregar();
  });
  $("grid").addEventListener("click", async e => {
    const b=e.target.closest(".apagar"); if(!b) return;
    const { error } = await sb.from("brainstorm").delete().eq("id", b.dataset.id);
    if (error) note("Não deu pra apagar: " + (error.message||"erro")); else await carregar();
  });
  $("grid").addEventListener("keydown", e => { if (e.key==="Enter" && (e.metaKey||e.ctrlKey) && e.target.tagName==="TEXTAREA") e.target.form.requestSubmit(); });
}
async function carregar(){
  const [b,c] = await Promise.all([sb.from("brainstorm").select("*").order("t"), sb.from("comentarios").select("*").order("t")]);
  if (b.data) data.brainstorm=b.data; if (c.data) data.comentarios=c.data;
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
    por[a].push({id:"c"+c.id, autor:c.email, texto:c.texto, t:c.t, edicao:L.day.data, ref:{titulo: L.tipo==="item"?L.obj.title:L.obj.ideia, url: L.tipo==="item"?L.obj.url:null}, origem:"sala"}); });
  data.brainstorm.forEach(m => por[m.area].push({id:m.id, autor:m.autor, texto:m.texto, t:m.t, edicao:m.edicao, origem:"mesa"}));
  for (const k of Object.keys(por)){
    const lista = por[k].sort((x,y)=>new Date(x.t)-new Date(y.t));
    const n=$("n-"+k); if(n) n.textContent = lista.length||"";
    const feed=$("feed-"+k); const atBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 60;
    feed.innerHTML = lista.length ? lista.map(m => `
      <div class="bs-msg ${m.autor===me?'me':''}">
        <div class="who"><b>${esc(m.autor||"Alguém do time")}</b><span>${m.edicao?"edição "+fmtShort(m.edicao):""}</span><span>${fmtTs(m.t)}</span>${m.origem==="mesa"&&(m.autor===me||isAdmin)?`<button class="apagar" data-id="${esc(m.id)}">apagar</button>`:""}</div>${esc(m.texto)}${m.ref?`<span class="ref">sobre: ${m.ref.url?`<a href="${esc(m.ref.url)}" target="_blank" rel="noopener">${esc(m.ref.titulo)}</a>`:esc(m.ref.titulo)}</span>`:""}
      </div>`).join("") : `<div class="bs-vazio">Mesa vazia. Comece a conversa.</div>`;
    if (atBottom || !feed.dataset.init) { feed.scrollTop = feed.scrollHeight; feed.dataset.init="1"; }
  }
}
function assinar(){
  const ch = sb.channel("brainstorm-live")
    .on("postgres_changes", {event:"*", schema:"public", table:"brainstorm"}, () => carregar())
    .on("postgres_changes", {event:"*", schema:"public", table:"comentarios"}, () => carregar())
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
