// Integração nativa com o Basecamp pro Brainstorm do Haven Bench News.
// Rotas (todas em /functions/v1/basecamp/...):
//   GET  /authorize            -> manda pro login do Basecamp (OAuth, uma vez)
//   GET  /callback?code=...    -> troca o código por tokens e guarda em basecamp_auth
//   GET  /status               -> { connected, account }
//   GET  /projects             -> projetos e listas de to-do da conta
//   POST /config               -> { area, bucket_id, todolist_id, projeto, lista }
//   POST /todo                 -> { area, content, description, tabela, id, por } cria o to-do e grava o link
// Segredos (Supabase > Edge Functions > Secrets): BASECAMP_CLIENT_ID, BASECAMP_CLIENT_SECRET.
import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const SB_URL = Deno.env.get("SUPABASE_URL")!;
const SB_SERVICE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const CLIENT_ID = Deno.env.get("BASECAMP_CLIENT_ID") || "";
const CLIENT_SECRET = Deno.env.get("BASECAMP_CLIENT_SECRET") || "";
const UA = "Haven Bench News (brusna@gmail.com)";
const REDIRECT = `${SB_URL}/functions/v1/basecamp/callback`;
const LAUNCHPAD = "https://launchpad.37signals.com";

const db = createClient(SB_URL, SB_SERVICE, { auth: { persistSession: false } });

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...CORS, "Content-Type": "application/json" } });
const html = (body: string, status = 200) =>
  new Response(`<!doctype html><meta charset="utf-8"><body style="font-family:Georgia,serif;max-width:560px;margin:60px auto;padding:0 20px;color:#2B2622;background:#F4F1ED;line-height:1.5">${body}</body>`, { status, headers: { "Content-Type": "text/html; charset=utf-8" } });

async function getAuth() {
  const { data } = await db.from("basecamp_auth").select("*").eq("id", 1).maybeSingle();
  return data;
}

async function saveTokens(tok: any, account?: { id: string; nome: string }) {
  const expires_at = new Date(Date.now() + (tok.expires_in ?? 1209600) * 1000).toISOString();
  const row: any = { id: 1, access_token: tok.access_token, refresh_token: tok.refresh_token, expires_at, updated_at: new Date().toISOString() };
  if (account) { row.account_id = account.id; row.account_nome = account.nome; }
  const { error } = await db.from("basecamp_auth").upsert(row);
  if (error) throw new Error("não consegui guardar os tokens: " + error.message);
}

async function accessToken(): Promise<{ token: string; account: string }> {
  const a = await getAuth();
  if (!a?.access_token || !a.account_id) throw new Error("Basecamp não conectado. Abra /authorize primeiro.");
  if (a.expires_at && new Date(a.expires_at).getTime() - Date.now() < 24 * 3600 * 1000) {
    const r = await fetch(`${LAUNCHPAD}/authorization/token?type=refresh&refresh_token=${encodeURIComponent(a.refresh_token)}&client_id=${encodeURIComponent(CLIENT_ID)}&client_secret=${encodeURIComponent(CLIENT_SECRET)}`, { method: "POST", headers: { "User-Agent": UA } });
    if (!r.ok) throw new Error("não consegui renovar a autorização do Basecamp (" + r.status + "). Abra /authorize de novo.");
    const tok = await r.json();
    if (!tok.refresh_token) tok.refresh_token = a.refresh_token;
    await saveTokens(tok);
    return { token: tok.access_token, account: a.account_id };
  }
  return { token: a.access_token, account: a.account_id };
}

async function bc(path: string, init: RequestInit = {}) {
  const { token, account } = await accessToken();
  const url = path.startsWith("http") ? path : `https://3.basecampapi.com/${account}${path}`;
  const r = await fetch(url, { ...init, headers: { ...(init.headers || {}), "Authorization": `Bearer ${token}`, "User-Agent": UA, "Content-Type": "application/json" } });
  if (!r.ok) throw new Error(`Basecamp respondeu ${r.status} em ${path}: ${(await r.text()).slice(0, 300)}`);
  return r.status === 204 ? null : await r.json();
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });
  const url = new URL(req.url);
  const route = url.pathname.replace(/^.*\/basecamp/, "") || "/";
  try {
    if (route === "/authorize") {
      if (!CLIENT_ID) return html("<h2>Falta o segredo BASECAMP_CLIENT_ID no Supabase.</h2>");
      const u = `${LAUNCHPAD}/authorization/new?type=web_server&client_id=${encodeURIComponent(CLIENT_ID)}&redirect_uri=${encodeURIComponent(REDIRECT)}`;
      return Response.redirect(u, 302);
    }
    if (route === "/callback") {
      const code = url.searchParams.get("code");
      if (!code) return html("<h2>Sem código de autorização.</h2>");
      const r = await fetch(`${LAUNCHPAD}/authorization/token?type=web_server&client_id=${encodeURIComponent(CLIENT_ID)}&redirect_uri=${encodeURIComponent(REDIRECT)}&client_secret=${encodeURIComponent(CLIENT_SECRET)}&code=${encodeURIComponent(code)}`, { method: "POST", headers: { "User-Agent": UA } });
      if (!r.ok) return html(`<h2>O Basecamp recusou a troca do código (${r.status}).</h2><p>${(await r.text()).slice(0, 300)}</p>`);
      const tok = await r.json();
      const ar = await fetch(`${LAUNCHPAD}/authorization.json`, { headers: { "Authorization": `Bearer ${tok.access_token}`, "User-Agent": UA } });
      const info = await ar.json();
      const contas = (info.accounts || []).filter((a: any) => a.product === "bc3");
      // Conta do Haven (6302304) tem prioridade; senão a primeira conta bc3 do login.
      const acc = contas.find((a: any) => String(a.id) === "6302304") || contas[0] || (info.accounts || [])[0];
      if (!acc) return html("<h2>Autorizou, mas não achei uma conta do Basecamp nesse login.</h2>");
      await saveTokens(tok, { id: String(acc.id), nome: acc.name });
      return html(`<h2>Basecamp conectado.</h2><p>Conta: <b>${acc.name}</b>. Pode fechar esta aba e voltar pro Brainstorm pra escolher as listas de cada mesa.</p>`);
    }
    if (route === "/accounts") {
      const a = await getAuth();
      const ar = await fetch(`${LAUNCHPAD}/authorization.json`, { headers: { "Authorization": `Bearer ${a?.access_token}`, "User-Agent": UA } });
      const info = await ar.json();
      return json({ atual: a?.account_id, contas: (info.accounts || []).map((x: any) => ({ id: x.id, name: x.name, product: x.product })) });
    }
    if (route === "/status") {
      const a = await getAuth();
      return json({ connected: !!(a?.access_token && a?.account_id), account: a?.account_nome || null, client_configured: !!CLIENT_ID });
    }
    if (route === "/trash") {
      // Manda pra lixeira as listas indicadas e desliga as mesas que apontavam pra elas.
      const bucket = Number(url.searchParams.get("bucket"));
      const ids = (url.searchParams.get("ids") || "").split(",").map((s) => Number(s.trim())).filter(Boolean);
      if (!bucket || !ids.length) return json({ error: "informe bucket e ids" }, 400);
      const feito: any[] = [];
      for (const id of ids) {
        await bc(`/buckets/${bucket}/recordings/${id}/status/trashed.json`, { method: "PUT" });
        await db.from("basecamp_listas").delete().eq("todolist_id", id);
        feito.push(id);
      }
      return json({ ok: true, lixeira: feito });
    }
    if (route === "/projects") {
      const todos = url.searchParams.get("all") === "1";
      const projects: any[] = await bc("/projects.json");
      const out = [];
      for (const p of projects) {
        const todoset = (p.dock || []).find((d: any) => d.name === "todoset" && d.enabled);
        if (!todoset) { if (todos) out.push({ id: p.id, name: p.name, todoset_id: null, lists: [], lists_error: "to-dos desligados nesse projeto" }); continue; }
        let lists: any[] = []; let lists_error: string | null = null;
        try { lists = await bc(`/buckets/${p.id}/todosets/${todoset.id}/todolists.json`); } catch (e) { lists = []; lists_error = String((e as Error).message || e); }
        out.push({ id: p.id, name: p.name, todoset_id: todoset.id, lists: lists.map((l: any) => ({ id: l.id, name: l.name })), lists_error });
      }
      return json({ projects: out });
    }
    if (route === "/setup") {
      // Cria (se faltar) uma lista por mesa no projeto indicado e liga as quatro mesas.
      const bucket = Number(url.searchParams.get("bucket") || (await req.json().catch(() => ({}))).bucket);
      if (!bucket) return json({ error: "informe bucket (id do projeto)" }, 400);
      const p = await bc(`/projects/${bucket}.json`);
      const todoset = (p.dock || []).find((d: any) => d.name === "todoset" && d.enabled);
      if (!todoset) return json({ error: "projeto sem to-dos habilitados" }, 400);
      const existentes: any[] = await bc(`/buckets/${bucket}/todosets/${todoset.id}/todolists.json`);
      const nomes: Record<string, string> = { vendas: "Brainstorm · Vendas", membership: "Brainstorm · Membership", parcerias: "Brainstorm · Parcerias", marketing: "Brainstorm · Marketing/Social" };
      const feito: any[] = [];
      for (const area of Object.keys(nomes)) {
        let l = existentes.find((x: any) => x.name === nomes[area]);
        if (!l) l = await bc(`/buckets/${bucket}/todosets/${todoset.id}/todolists.json`, { method: "POST", body: JSON.stringify({ name: nomes[area], description: "Conversas levadas do Brainstorm do Haven Bench News (mesa de " + area + ")." }) });
        await db.from("basecamp_listas").upsert({ area, bucket_id: bucket, todolist_id: l.id, projeto: p.name, lista: l.name });
        feito.push({ area, lista: l.name, id: l.id, url: l.app_url });
      }
      return json({ ok: true, projeto: p.name, listas: feito });
    }
    if (route === "/config" && req.method === "POST") {
      const b = await req.json();
      if (!["vendas", "membership", "parcerias", "marketing"].includes(b.area)) return json({ error: "área inválida" }, 400);
      const { error } = await db.from("basecamp_listas").upsert({ area: b.area, bucket_id: b.bucket_id, todolist_id: b.todolist_id, projeto: b.projeto, lista: b.lista });
      if (error) return json({ error: error.message }, 500);
      return json({ ok: true });
    }
    if (route === "/todo" && req.method === "POST") {
      const b = await req.json();
      const { data: cfg } = await db.from("basecamp_listas").select("*").eq("area", b.area).maybeSingle();
      if (!cfg?.bucket_id || !cfg?.todolist_id) return json({ error: `A mesa de ${b.area} ainda não está ligada a uma lista do Basecamp.` }, 400);
      const content = String(b.content || "").trim().slice(0, 200);
      if (!content) return json({ error: "sem texto" }, 400);
      const todo = await bc(`/buckets/${cfg.bucket_id}/todolists/${cfg.todolist_id}/todos.json`, { method: "POST", body: JSON.stringify({ content, description: b.description || "" }) });
      const app_url = todo?.app_url || null;
      if (b.tabela && b.id) {
        const patch = b.tabela === "brainstorm"
          ? { basecamp_t: new Date().toISOString(), basecamp_por: b.por || null, basecamp_url: app_url }
          : { bs_basecamp_t: new Date().toISOString(), bs_basecamp_por: b.por || null, bs_basecamp_url: app_url };
        await db.from(b.tabela === "brainstorm" ? "brainstorm" : "comentarios").update(patch).eq("id", b.id);
      }
      return json({ ok: true, url: app_url, lista: cfg.lista, projeto: cfg.projeto });
    }
    return json({ error: "rota desconhecida", route }, 404);
  } catch (e) {
    return json({ error: String((e as Error).message || e) }, 500);
  }
});
