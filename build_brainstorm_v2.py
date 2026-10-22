#!/usr/bin/env python3
"""Variações de UX do Brainstorm (mesmos dados e mesma lógica do build_brainstorm.py).
  abas      -> barra de mesas no topo com contador; uma mesa aberta por vez; composer fixo no pé da mesa
  compacta  -> mesas empilhadas, fechadas por padrão (linha com contador e última fala); abrem ao toque
Uso: python3 build_brainstorm_v2.py SUPABASE_URL SUPABASE_ANON_KEY MODO destino
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 5:
    print("uso: build_brainstorm_v2.py SUPABASE_URL SUPABASE_ANON_KEY abas|compacta destino"); sys.exit(1)
SB_URL, SB_KEY, MODE, dest = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert MODE in ("abas", "compacta")

site = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
css = re.search(r"<style>(.*?)</style>", site, re.S).group(1)
sala = open(os.path.join(HERE, "build_sala.py"), encoding="utf-8").read()
extra = re.search(r'EXTRA_CSS = r"""(.*?)"""', sala, re.S).group(1)

extra += r"""
  /* ---- brainstorm v2: base comum ---- */
  .page{max-width:1000px}
  .login{max-width:520px;margin:40px auto;padding:28px;background:var(--paper);border:1px solid var(--rule)}
  .login h2{font-family:var(--serif);font-weight:500;font-style:italic;font-size:26px;margin-bottom:8px}
  .login p{font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--espresso);margin-bottom:14px}
  select{font-family:var(--serif2);font-size:17px;color:var(--ink);background:var(--paper);border:1px solid var(--rule);padding:10px 12px;width:100%}
  .top{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 0 10px;border-bottom:2px solid var(--ink);flex-wrap:wrap}
  .top h1{font-family:var(--serif);font-weight:500;font-size:26px;line-height:1;margin:0;letter-spacing:-.01em}
  .top h1 span{font-style:italic;font-weight:400;color:var(--soft)}
  .top .r{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
  .top a.nav{font-family:var(--sans);font-size:12px;color:var(--soft);text-decoration:underline}
  .top .me{font-family:var(--sans);font-size:12px;color:var(--soft);letter-spacing:0;text-transform:none}
  .top .me b{color:var(--ink)}
  .top .btn.sm{font-size:10px;padding:6px 10px}

  .bs-resp{margin-top:8px;padding:8px 0 2px 12px;border-left:2px solid var(--teal);font-family:var(--serif2);font-size:16px;line-height:1.42;color:var(--ink);white-space:pre-wrap}
  .bs-resp i{font-family:var(--sans);font-style:normal;font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:4px}
  .live{font-family:var(--sans);font-size:11px;color:var(--mute);display:inline-flex;align-items:center;gap:6px}
  .live i{width:7px;height:7px;border-radius:50%;background:var(--sand);display:inline-block}
  .live.on i{background:var(--forest)}
  details.ajuda{margin:10px 0 0}
  details.ajuda summary{font-family:var(--sans);font-size:12px;color:var(--soft);cursor:pointer;list-style:none;display:inline-flex;gap:6px;align-items:center}
  details.ajuda summary::-webkit-details-marker{display:none}
  details.ajuda summary::before{content:"+";font-weight:700}
  details.ajuda[open] summary::before{content:"–"}
  details.ajuda p{font-family:var(--serif2);font-size:16px;line-height:1.5;color:var(--espresso);max-width:70ch;padding:8px 0 4px}

  .msg{padding:12px 0;border-bottom:1px solid var(--rule);word-break:break-word;position:relative}
  .msg:last-child{border-bottom:0}
  .msg .head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;font-family:var(--sans);font-size:12px;color:var(--mute);margin-bottom:3px}
  .msg .head b{color:var(--ink);font-weight:600;font-size:13px}
  .msg .txt{display:block;font-family:var(--serif2);font-size:17px;line-height:1.45;color:var(--espresso);white-space:pre-wrap}
  .msg.mine .txt{color:var(--ink)}
  .msg .ref{display:block;font-family:var(--sans);font-size:12px;color:var(--soft);margin-top:6px;line-height:1.4}
  .msg .ref a{text-decoration:underline;color:var(--soft)}
  .msg .tag{font-family:var(--sans);font-size:11px;padding:2px 7px;border:1px solid var(--rule);border-radius:2px;color:var(--soft);background:var(--paper)}
  .msg .tag.andamento{border-color:var(--forest);color:var(--forest)}
  .msg .tag.finalizada{border-color:var(--mute)}
  .msg .tag.descartada{border-color:var(--mute);text-decoration:line-through}
  .msg .tag.basecamp{border-color:var(--ochre);color:var(--ochre);text-decoration:none}
  .msg.st-andamento{box-shadow:inset 3px 0 0 var(--forest);padding-left:12px}
  .msg.encerrada{opacity:.55}
  .msg .acts{position:relative;margin-left:auto}
  .msg .acts summary{list-style:none;cursor:pointer;font-family:var(--sans);font-size:14px;color:var(--mute);padding:0 6px;line-height:1;letter-spacing:.1em}
  .msg .acts summary::-webkit-details-marker{display:none}
  .msg .acts summary:hover{color:var(--ink)}
  .msg .acts .menu{position:absolute;right:0;top:20px;z-index:5;background:var(--paper);border:1px solid var(--rule);box-shadow:0 8px 24px rgba(43,38,34,.12);min-width:200px;display:flex;flex-direction:column}
  .msg .acts .menu button{font-family:var(--sans);font-size:13px;text-align:left;background:none;border:0;border-bottom:1px solid var(--rule);padding:9px 12px;cursor:pointer;color:var(--ink)}
  .msg .acts .menu button:last-child{border-bottom:0}
  .msg .acts .menu button:hover{background:rgba(63,56,50,.05)}
  .msg .acts .menu button.bc{color:var(--ochre)}
  .msg .acts .menu button.apagar{color:var(--terracotta)}
  .vazio{font-family:var(--serif2);font-style:italic;font-size:16px;color:var(--mute);padding:18px 0}
  .enc{font-family:var(--sans);font-size:12px;color:var(--mute);background:transparent;border:0;border-bottom:1px solid var(--rule);padding:8px 0;cursor:pointer;text-align:left;width:100%}
  .enc:hover{color:var(--ink)}
  .composer{display:grid;grid-template-columns:1fr auto;gap:8px 10px;align-items:end;padding:10px 0 0;border-top:1px solid var(--rule);background:var(--paper)}
  .composer textarea{width:100%;min-height:44px;font-size:16px;padding:10px 12px;resize:none;box-sizing:border-box}
  .composer .btn{white-space:nowrap}
  .composer .hint{grid-column:1 / -1;font-family:var(--sans);font-size:11px;color:var(--mute)}

  .bc-foot{margin-top:28px;padding:14px 0 0;border-top:1px solid var(--rule);font-family:var(--sans);font-size:12px;color:var(--soft);line-height:1.6}
  .bc-foot b{color:var(--ink);font-weight:600}
  .bc-foot .grid{display:grid;grid-template-columns:1fr;gap:10px;margin-top:10px}
  @media(min-width:900px){.bc-foot .grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .bc-foot label{display:block;margin-bottom:4px}
  .bc-foot select{font-size:14px;padding:8px 10px}
  footer p{font-size:12px}
  .c-vendas{--mesa:var(--forest)} .c-membership{--mesa:var(--terracotta)} .c-parcerias{--mesa:var(--teal)} .c-marketing{--mesa:var(--plum)}
"""

if MODE == "abas":
    extra += r"""
  .tabs{display:flex;gap:0;border-bottom:1px solid var(--rule);margin-top:14px;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .tabs button{font-family:var(--serif);font-style:italic;font-weight:500;font-size:19px;background:none;border:0;border-bottom:3px solid transparent;padding:10px 14px 8px;cursor:pointer;color:var(--soft);white-space:nowrap;display:inline-flex;align-items:baseline;gap:8px;margin-bottom:-1px}
  .tabs button em{font-family:var(--sans);font-style:normal;font-size:11px;color:var(--paper);background:var(--mute);border-radius:10px;padding:1px 7px;min-width:18px;text-align:center}
  .tabs button.on{color:var(--ink);border-bottom-color:var(--mesa)}
  .tabs button.on em{background:var(--mesa)}
  .tabs button em:empty{display:none}
  .mesa{display:none;background:var(--paper);border:1px solid var(--rule);border-top:0;padding:0 18px 14px}
  .mesa.on{display:flex;flex-direction:column}
  .mesa .sub{font-family:var(--sans);font-size:12px;color:var(--mute);padding:10px 0 2px}
  .feed{overflow-y:auto;max-height:62vh;min-height:30vh;scroll-behavior:smooth;padding-bottom:6px}
  @media(max-width:600px){.mesa{padding:0 12px 12px}.feed{max-height:58vh}}
"""
else:
    extra += r"""
  .pilha{display:flex;flex-direction:column;gap:10px;margin-top:16px}
  .mesa{background:var(--paper);border:1px solid var(--rule);border-left:4px solid var(--mesa)}
  .mesa .cab{display:flex;align-items:center;gap:12px;padding:12px 16px;cursor:pointer;user-select:none}
  .mesa .cab:hover{background:rgba(63,56,50,.03)}
  .mesa .cab h2{font-family:var(--serif);font-style:italic;font-weight:500;font-size:21px;margin:0;line-height:1;display:flex;align-items:baseline;gap:8px}
  .mesa .cab h2 em{font-family:var(--sans);font-style:normal;font-size:11px;color:var(--paper);background:var(--mesa);border-radius:10px;padding:1px 7px}
  .mesa .cab h2 em:empty{display:none}
  .mesa .cab .ult{font-family:var(--serif2);font-size:15px;color:var(--mute);flex:1 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-style:italic}
  .mesa .cab .ult b{font-family:var(--sans);font-style:normal;font-size:12px;color:var(--soft);font-weight:600;margin-right:6px}
  .mesa .cab .seta{font-family:var(--sans);font-size:12px;color:var(--mute);transition:transform .15s}
  .mesa.on .cab .seta{transform:rotate(90deg)}
  .mesa.on .cab .ult{display:none}
  .mesa .corpo{display:none;padding:0 16px 14px}
  .mesa.on .corpo{display:block}
  .feed{overflow-y:auto;max-height:52vh;scroll-behavior:smooth}
  @media(max-width:600px){.mesa .cab{padding:10px 12px;flex-wrap:wrap}.mesa .cab .ult{flex-basis:100%;white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}.mesa .corpo{padding:0 12px 12px}}
"""

MESAS_ABAS = r"""
    <div class="tabs" id="tabs"></div>
    <div id="mesas"></div>
"""
MESAS_PILHA = r"""
    <div class="pilha" id="mesas"></div>
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
  <div class="top">
    <h1>Brainstorm <span>· Haven Bench News</span></h1>
    <div class="r"><span class="live" id="live"><i></i><span id="live-txt">conectando</span></span><a class="nav" href="../../sala/">Sala do time</a><span class="me" id="me"></span><button class="btn sm ghost" id="sair" hidden>Trocar nome</button></div>
  </div>
  <div class="ro" id="ro" hidden></div>

  <section class="login" id="login" hidden>
    <h2>Quem é você?</h2>
    <p>O brainstorm é aberto pra quem tem o link. Escolha seu nome uma vez; ele fica guardado neste aparelho e assina o que você escrever.</p>
    <form class="form" id="login-form"><select id="login-nome"><option value="">Escolher nome</option><option>Bru</option><option>Teti</option><option>Carolina</option><option>Omi</option><option>Julia</option><option>Julinha</option><option value="__outro">Outro nome</option></select><input type="text" id="login-outro" placeholder="Seu nome" maxlength="40" hidden><div class="row"><button class="btn" type="submit" id="login-btn">Entrar</button></div><div class="note" id="login-note"></div></form>
  </section>

  <div id="app" hidden>
    <details class="ajuda"><summary>como funciona</summary><p>Quatro mesas, uma por área. Entram aqui os comentários deixados nos itens da sala, já separados pela área do item, e o que for escrito direto nas mesas. Tudo aparece na hora pra quem estiver com a página aberta. Cada conversa fica na mesa até alguém marcar em andamento, finalizar ou desprezar; as encerradas ficam na dobra. "Levar pro Basecamp" cria a tarefa na lista Brainstorm Bench News do projeto da mesa.</p></details>
    __MESAS__
    <div class="bc-foot" id="bc-box" hidden><span id="bc-txt"></span><div class="grid" id="bc-grid" hidden></div></div>
  </div>

  <footer>
    <p>Cada mensagem traz autor, edição do Bench a que se refere e hora. O quadro é lido pela rotina da manhã do Bench. A sala do time fica em <a href="../../sala/" style="text-decoration:underline">benchnews/sala</a>.</p>
  </footer>
</div>
<script>
const MODE = "__MODE__";
const SB_URL = "__SB_URL__", SB_KEY = "__SB_KEY__";
const RADAR_URL = "https://brusna-infurna.github.io/daily-haven-bench-news/radar-data.json";
const sb = supabase.createClient(SB_URL, SB_KEY);
const AREAS = [["vendas","Vendas","itens marcados pra vendas"],["membership","Membership","itens marcados pra clube"],["parcerias","Parcerias","itens marcados pra parcerias"],["marketing","Marketing/Social","itens marcados pra marketing"]];
const PARA2AREA = {vendas:"vendas", clube:"membership", parcerias:"parcerias", marketing:"marketing"};
const MS=["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
const esc = s => String(s??"").replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtShort = d => { if(!d) return ""; const [y,m,dd]=String(d).slice(0,10).split("-"); return `${+dd} ${MS[+m-1]}`; };
const fmtTs = t => { const d=new Date(t); if (isNaN(d)) return ""; const hoje=new Date(); const mesmo=d.toDateString()===hoje.toDateString(); const hm=`${String(d.getHours()).padStart(2,"0")}h${String(d.getMinutes()).padStart(2,"0")}`; return mesmo ? `hoje ${hm}` : `${d.getDate()} ${MS[d.getMonth()]} ${hm}`; };
const $ = id => document.getElementById(id);
function note(msg){ const ro=$("ro"); ro.hidden=!msg; ro.innerHTML = msg ? `<b>Aviso.</b> ${esc(msg)}` : ""; }

let RADAR = {dias:[]}; const lookup = {}; const nomes = {};
let me = "", isAdmin = false, ativa = "vendas"; const abertas = {vendas:true};
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
const nome = a => { if(!a) return "Alguém do time"; const k=String(a).toLowerCase(); if (nomes[k]) return nomes[k]; if (k.includes("@")) return k.split("@")[0].replace(/[._]/g," ").replace(/\b\w/g,c=>c.toUpperCase()); return a; };

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
  try { const m = await sb.from("membros").select("email,nome"); (m.data||[]).forEach(x => { if (x.email && x.nome) nomes[String(x.email).toLowerCase()] = x.nome; }); } catch(e){}
  const n = lerNome(); if (n) await entrar(n); else $("login").hidden=false;
}
async function entrar(n){
  me = n; isAdmin = n === "Bru";
  $("me").innerHTML = `Você: <b>${esc(n)}</b>`; $("sair").hidden=false;
  $("login").hidden=true; $("app").hidden=false;
  montar(); await carregar(); assinar(); setInterval(carregar, 30000); bcInit();
}
const composer = (k,l) => `<form class="composer" data-a="${k}"><textarea rows="1" placeholder="Escreva pra mesa de ${esc(l)}"></textarea><button class="btn sm" type="submit">Enviar</button><span class="hint">assina como ${esc(me)} · ⌘/Ctrl+Enter envia</span></form>`;
function montar(){
  if (MODE==="abas"){
    $("tabs").innerHTML = AREAS.map(([k,l]) => `<button class="c-${k}" data-tab="${k}">${esc(l)}<em id="n-${k}"></em></button>`).join("");
    $("mesas").innerHTML = AREAS.map(([k,l,sub]) => `<section class="mesa c-${k}" data-a="${k}"><div class="sub">${esc(sub)} e conversa direta</div><div class="feed" id="feed-${k}"></div>${composer(k,l)}</section>`).join("");
    $("tabs").addEventListener("click", e => { const b=e.target.closest("button[data-tab]"); if(!b) return; ativa=b.dataset.tab; try{localStorage.setItem("benchnews-bs-aba",ativa);}catch(x){} aplicar(); });
    try { ativa = localStorage.getItem("benchnews-bs-aba") || "vendas"; } catch(e){}
  } else {
    $("mesas").innerHTML = AREAS.map(([k,l,sub]) => `<section class="mesa c-${k}" data-a="${k}"><div class="cab" data-tog="${k}"><h2>${esc(l)}<em id="n-${k}"></em></h2><span class="ult" id="ult-${k}"></span><span class="seta">▶</span></div><div class="corpo"><div class="feed" id="feed-${k}"></div>${composer(k,l)}</div></section>`).join("");
    $("mesas").addEventListener("click", e => { const c=e.target.closest(".cab[data-tog]"); if(!c) return; abertas[c.dataset.tog]=!abertas[c.dataset.tog]; aplicar(); });
  }
  aplicar();
  $("mesas").addEventListener("submit", async e => {
    e.preventDefault(); const f=e.target; const ta=f.querySelector("textarea"); const txt=ta.value.trim(); if(!txt) return;
    const btn=f.querySelector("button"); btn.disabled=true;
    const edicao = (RADAR.dias && RADAR.dias[0]) ? RADAR.dias[0].data : null;
    const { error } = await sb.from("brainstorm").insert({area:f.dataset.a, autor:me, texto:txt, edicao});
    btn.disabled=false; if (error) { note("Não deu pra enviar: " + (error.message||"erro")); return; }
    ta.value=""; ta.style.height=""; await carregar();
  });
  $("mesas").addEventListener("input", e => { if (e.target.tagName==="TEXTAREA"){ e.target.style.height="auto"; e.target.style.height=Math.min(e.target.scrollHeight,160)+"px"; } });
  $("mesas").addEventListener("keydown", e => { if (e.key==="Enter" && (e.metaKey||e.ctrlKey) && e.target.tagName==="TEXTAREA") e.target.form.requestSubmit(); });
  $("mesas").addEventListener("click", async e => {
    const enc=e.target.closest(".enc"); if (enc){ verEnc[enc.dataset.enc]=!verEnc[enc.dataset.enc]; render(); return; }
    const st=e.target.closest(".menu button[data-st]"); if (st){
      const msg=st.closest(".msg"); const tab=msg.dataset.tabela, id=msg.dataset.id, novo=st.dataset.st;
      const agora=new Date().toISOString();
      const patch = tab==="brainstorm" ? {status:novo, status_por:me, status_t:agora} : tab==="ideias" ? {status:IDST_BACK[novo]||"avaliando", status_por:me, status_t:agora} : {bs_status:novo, bs_status_por:me, bs_status_t:agora};
      const { error } = await sb.from(tab).update(patch).eq(tab==="ideias"?"chave":"id", id);
      if (error) note("Não deu pra mudar o estado: " + (error.message||"erro")); else await carregar();
      return; }
    const bc=e.target.closest(".menu button.bc"); if (bc){
      const msg=bc.closest(".msg"); const tab=msg.dataset.tabela, id=msg.dataset.id, area=msg.closest(".mesa").dataset.a;
      const cfg = bcListas[area]; if (!cfg || !cfg.todolist_id){ note("A mesa de " + area + " ainda não está ligada a uma lista do Basecamp."); return; }
      const texto = msg.dataset.texto||""; const autor = msg.dataset.autor||""; const edicao = msg.dataset.edicao||"";
      const content = texto.length>ASSUNTO_MAX ? texto.slice(0,ASSUNTO_MAX-1).trimEnd()+"…" : texto;
      const description = `<div>${esc(texto)}</div><div><br></div><div>Origem: Brainstorm do Bench News, mesa ${esc(area)}${edicao?", edição "+fmtShort(edicao):""}, por ${esc(nome(autor))}. <a href="${esc(location.href)}">Abrir o brainstorm</a></div>`;
      bc.disabled=true; bc.textContent="Criando no Basecamp...";
      try {
        const r = await fetch(FN + "/todo", {method:"POST", headers:{"Content-Type":"application/json","apikey":SB_KEY}, body: JSON.stringify({area, content, description, tabela:tab, id, por:me})});
        const j = await r.json();
        if (!r.ok || j.error) throw new Error(j.error || ("erro " + r.status));
        note(""); await carregar();
      } catch(err){ note("Não deu pra criar no Basecamp: " + err.message); bc.disabled=false; bc.textContent="Levar pro Basecamp"; }
      return; }
    const b=e.target.closest(".menu button.apagar"); if(!b) return;
    const { error } = await sb.from("brainstorm").delete().eq("id", b.dataset.id);
    if (error) note("Não deu pra apagar: " + (error.message||"erro")); else await carregar();
  });
  document.addEventListener("click", e => { document.querySelectorAll("details.acts[open]").forEach(d => { if (!d.contains(e.target)) d.open=false; }); });
}
function aplicar(){
  if (MODE==="abas"){
    document.querySelectorAll("#tabs button").forEach(b => b.classList.toggle("on", b.dataset.tab===ativa));
    document.querySelectorAll(".mesa").forEach(m => m.classList.toggle("on", m.dataset.a===ativa));
  } else {
    document.querySelectorAll(".mesa").forEach(m => m.classList.toggle("on", !!abertas[m.dataset.a]));
  }
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
    const mine = m.autor===me || nome(m.autor)===me;
    const acts = enc ? `<button data-st="aberta">Reabrir</button>`
      : (m.status==="andamento" ? `<button data-st="finalizada">Finalizar</button><button data-st="descartada">Desprezar</button><button data-st="aberta">Voltar pra aberta</button>`
                                : `<button data-st="andamento">Marcar em andamento</button><button data-st="finalizada">Finalizar</button><button data-st="descartada">Desprezar</button>`);
    const bcBtn = enc ? "" : `<button class="bc" type="button">${m.basecamp?"Reenviar pro Basecamp":"Levar pro Basecamp"}</button>`;
    const del = m.origem==="mesa"&&(mine||isAdmin) ? `<button class="apagar" data-id="${esc(m.id)}">Apagar</button>` : "";
    return `<div class="msg ${mine?'mine':''} st-${m.status} ${enc?'encerrada':''}" data-id="${esc(m.id)}" data-tabela="${m.tabela}" data-texto="${esc(m.texto)}" data-autor="${esc(m.autor||"")}" data-edicao="${esc(m.edicao||"")}">
      <div class="head"><b>${esc(nome(m.autor))}</b><span>${fmtTs(m.t)}</span>${m.edicao?`<span>· ed. ${fmtShort(m.edicao)}</span>`:""}${m.status!=="aberta"?`<span class="tag ${esc(m.status)}">${esc(ST[m.status])}</span>`:""}${m.basecamp?(m.basecampUrl?`<a class="tag basecamp" href="${esc(m.basecampUrl)}" target="_blank" rel="noopener">no Basecamp ↗</a>`:`<span class="tag basecamp">no Basecamp</span>`):""}<details class="acts"><summary title="ações">···</summary><div class="menu">${acts}${bcBtn}${del}</div></details></div>
      <span class="txt">${esc(m.texto)}</span>${m.ref?`<span class="ref">sobre: ${m.ref.url?`<a href="${esc(m.ref.url)}" target="_blank" rel="noopener">${esc(m.ref.titulo)}</a>`:esc(m.ref.titulo)}</span>`:""}${respDe(m)}
    </div>`; };
  for (const k of Object.keys(por)){
    const lista = por[k].sort((x,y)=>new Date(x.t)-new Date(y.t));
    const ab = lista.filter(m=>m.status==="aberta"||m.status==="andamento");
    const encerradas = lista.filter(m=>m.status==="finalizada"||m.status==="descartada");
    const n=$("n-"+k); if(n) n.textContent = ab.length ? String(ab.length) : "";
    const u=$("ult-"+k); if(u){ const last=ab[ab.length-1]; u.innerHTML = last ? `<b>${esc(nome(last.autor))}</b>${esc(last.texto.slice(0,140))}` : (encerradas.length?"nada em aberto":"mesa vazia"); }
    const feed=$("feed-"+k); const atBottom = feed.scrollHeight - feed.scrollTop - feed.clientHeight < 60;
    let h = "";
    if (encerradas.length) h += `<button class="enc" data-enc="${k}">${verEnc[k]?"esconder":"ver"} encerradas (${encerradas.length})</button>`;
    if (verEnc[k]) h += encerradas.map(msgHtml).join("");
    h += ab.length ? ab.map(msgHtml).join("") : `<div class="vazio">${encerradas.length?"Nada em aberto nesta mesa.":"Mesa vazia. Comece a conversa."}</div>`;
    feed.innerHTML = h;
    if (atBottom || !feed.dataset.init) { feed.scrollTop = feed.scrollHeight; feed.dataset.init="1"; }
  }
}
async function bcInit(){
  const box=$("bc-box"), txt=$("bc-txt"), grid=$("bc-grid");
  try { bcStatus = await (await fetch(FN + "/status", {headers:{"apikey":SB_KEY}})).json(); } catch(e){ bcStatus = null; }
  box.hidden=false;
  if (!bcStatus || !bcStatus.client_configured){ txt.innerHTML = "Basecamp: integração ainda não configurada."; return; }
  if (!bcStatus.connected){ txt.innerHTML = `Basecamp ainda não autorizado. <a href="${esc(FN)}/authorize" style="text-decoration:underline">Autorizar</a> (uma vez, por quem administra).`; return; }
  const ligadas = AREAS.filter(([k])=>bcListas[k]&&bcListas[k].todolist_id);
  const resumo = ligadas.map(([k,l])=>`${esc(l)} → <b>${esc(bcListas[k].projeto||"")}</b>`).join(" · ");
  txt.innerHTML = `Basecamp conectado. "Levar pro Basecamp" cria a tarefa na lista Brainstorm Bench News de: ${resumo || "nenhum projeto ainda"}.${isAdmin?` <button class="btn sm ghost" id="bc-cfg" type="button">Mudar listas</button>`:""}`;
  if (!isAdmin) return;
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

html = (TEMPLATE.replace("__CSS__", css + extra).replace("__SB_URL__", SB_URL).replace("__SB_KEY__", SB_KEY)
        .replace("__MODE__", MODE).replace("__MESAS__", MESAS_ABAS if MODE == "abas" else MESAS_PILHA))
os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
open(dest, "w", encoding="utf-8").write(html)
print("brainstorm", MODE, "gerado:", dest, len(html), "bytes")
