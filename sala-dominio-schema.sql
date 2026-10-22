-- Sala do Time · Haven Bench News · esquema Supabase (Postgres)
-- Rodar inteiro no SQL Editor do projeto Supabase. Idempotente o suficiente pra rodar duas vezes.

create extension if not exists pgcrypto;

-- Quem pode entrar na sala. Email em minúsculas. Nome é o que aparece nos comentários.
create table if not exists membros (
  email text primary key,
  nome  text not null,
  papel text not null default 'editor' check (papel in ('editor','admin'))
);

insert into membros (email, nome, papel) values
  ('brusna@gmail.com',        'Bru',      'admin'),
  ('bruna@infurna.com',       'Bru',      'admin'),
  ('teti@haven.com.br',       'Teti',     'editor'),
  ('tetifleury@hotmail.com',  'Teti',     'editor'),
  ('carolinaveira@gmail.com', 'Carolina', 'editor'),
  ('i@omi.ooo',               'Omi',      'editor'),
  ('julia.sobral@gmail.com',  'Julia',    'editor')
on conflict (email) do update set nome = excluded.nome, papel = excluded.papel;

-- Reações por item ou ideia (chave = e<data>-i<n> ou e<data>-b<n>)
create table if not exists votos (
  chave text not null,
  email text not null,
  v     text not null check (v in ('sim','nao')),
  t     timestamptz not null default now(),
  primary key (chave, email)
);

create table if not exists comentarios (
  id    uuid primary key default gen_random_uuid(),
  chave text not null,
  email text not null,
  texto text not null check (length(texto) between 1 and 4000),
  tipo  text not null default 'comentario' check (tipo in ('comentario','claude')),
  t     timestamptz not null default now()
);
create index if not exists comentarios_chave on comentarios (chave);

create table if not exists pautas (
  id       uuid primary key default gen_random_uuid(),
  email    text not null,
  texto    text not null check (length(texto) between 1 and 4000),
  status   text not null default 'aberta' check (status in ('aberta','respondida')),
  edicao   date,
  resposta text,
  t        timestamptz not null default now()
);

create table if not exists ideias (
  chave  text primary key,
  status text not null default 'nova' check (status in ('nova','avaliando','andamento','feita','descartada')),
  dono   text,
  t      timestamptz not null default now()
);

-- Segredo que a rotina da manhã usa pra ler e responder. Troque o valor antes de rodar.
create table if not exists config (k text primary key, v text not null);
insert into config (k, v) values ('token_rotina', 'TROQUE-POR-UM-SEGREDO-LONGO')
on conflict (k) do nothing;

-- Helpers
create or replace function eu_email() returns text language sql stable as $$
  select lower(coalesce(auth.jwt() ->> 'email', ''));
$$;
create or replace function sou_membro() returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from membros where email = eu_email());
$$;
create or replace function sou_admin() returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from membros where email = eu_email() and papel = 'admin');
$$;

-- RLS: só membro logado lê e escreve; cada um edita o que é seu; admin edita tudo.
alter table membros     enable row level security;
alter table votos       enable row level security;
alter table comentarios enable row level security;
alter table pautas      enable row level security;
alter table ideias      enable row level security;
alter table config      enable row level security;

drop policy if exists membros_select on membros;
create policy membros_select on membros for select to authenticated using (sou_membro());

drop policy if exists votos_select on votos;
drop policy if exists votos_write  on votos;
create policy votos_select on votos for select to authenticated using (sou_membro());
create policy votos_write  on votos for all    to authenticated using (sou_membro() and email = eu_email()) with check (sou_membro() and email = eu_email());

drop policy if exists com_select on comentarios;
drop policy if exists com_insert on comentarios;
drop policy if exists com_modify on comentarios;
create policy com_select on comentarios for select to authenticated using (sou_membro());
create policy com_insert on comentarios for insert to authenticated with check (sou_membro() and email = eu_email());
create policy com_modify on comentarios for all    to authenticated using (sou_membro() and (email = eu_email() or sou_admin()));

drop policy if exists pautas_select on pautas;
drop policy if exists pautas_insert on pautas;
drop policy if exists pautas_modify on pautas;
create policy pautas_select on pautas for select to authenticated using (sou_membro());
create policy pautas_insert on pautas for insert to authenticated with check (sou_membro() and email = eu_email());
create policy pautas_modify on pautas for all    to authenticated using (sou_membro() and (email = eu_email() or sou_admin()));

drop policy if exists ideias_select on ideias;
drop policy if exists ideias_write  on ideias;
create policy ideias_select on ideias for select to authenticated using (sou_membro());
create policy ideias_write  on ideias for all    to authenticated using (sou_membro()) with check (sou_membro());

-- config: ninguém lê pela API; só as funções abaixo (security definer).

-- Leitura pela rotina da manhã: select sala_export('TOKEN');
create or replace function sala_export(p_token text) returns jsonb
language plpgsql security definer set search_path = public as $$
declare ok boolean;
begin
  select exists (select 1 from config where k = 'token_rotina' and v = p_token) into ok;
  if not ok then raise exception 'token invalido'; end if;
  return jsonb_build_object(
    'votos',       (select coalesce(jsonb_agg(to_jsonb(x)), '[]'::jsonb) from (select chave, v, t from votos) x),
    'comentarios', (select coalesce(jsonb_agg(to_jsonb(x)), '[]'::jsonb) from (select c.id, c.chave, m.nome, c.texto, c.tipo, c.t from comentarios c left join membros m on m.email = c.email order by c.t) x),
    'pautas',      (select coalesce(jsonb_agg(to_jsonb(x)), '[]'::jsonb) from (select p.id, m.nome, p.texto, p.status, p.edicao, p.resposta, p.t from pautas p left join membros m on m.email = p.email order by p.t) x),
    'ideias',      (select coalesce(jsonb_agg(to_jsonb(x)), '[]'::jsonb) from (select i.chave, i.status, m.nome as dono, i.t from ideias i left join membros m on m.email = i.dono) x)
  );
end $$;

-- Resposta da rotina a uma pauta: select sala_responder('TOKEN', 'uuid', '2026-10-23', 'texto');
create or replace function sala_responder(p_token text, p_id uuid, p_edicao date, p_resposta text) returns void
language plpgsql security definer set search_path = public as $$
declare ok boolean;
begin
  select exists (select 1 from config where k = 'token_rotina' and v = p_token) into ok;
  if not ok then raise exception 'token invalido'; end if;
  update pautas set status = 'respondida', edicao = p_edicao, resposta = p_resposta where id = p_id;
end $$;

revoke all on function sala_export(text) from public;
revoke all on function sala_responder(text, uuid, date, text) from public;
grant execute on function sala_export(text) to anon, authenticated;
grant execute on function sala_responder(text, uuid, date, text) to anon, authenticated;

-- 22/10/2026: sala aberta. Quem tem o link lê e escreve, identificado pelo nome escolhido na página
-- (coluna email passa a guardar o nome). Aplicado direto no projeto; registrado aqui pra referência.
create policy votos_anon  on votos       for all to anon using (true) with check (true);
create policy com_anon    on comentarios for all to anon using (true) with check (true);
create policy pautas_anon on pautas      for all to anon using (true) with check (true);
create policy ideias_anon on ideias      for all to anon using (true) with check (true);
-- sala_export: nome = coalesce(membros.nome, registro.email)

-- 22/10/2026: Brainstorm do time (benchnews/brainstorm/), mesas por área com Supabase Realtime.
create table if not exists brainstorm (
  id    uuid primary key default gen_random_uuid(),
  area  text not null check (area in ('vendas','membership','parcerias','marketing')),
  autor text not null check (length(autor) between 1 and 40),
  texto text not null check (length(texto) between 1 and 4000),
  edicao date,
  t     timestamptz not null default now()
);
create index if not exists brainstorm_area_t on brainstorm (area, t);
alter table brainstorm enable row level security;
create policy brainstorm_anon on brainstorm for all to anon using (true) with check (true);
create policy brainstorm_auth on brainstorm for all to authenticated using (true) with check (true);
alter publication supabase_realtime add table brainstorm;
alter publication supabase_realtime add table comentarios;
-- 22/10/2026: estado das conversas do brainstorm (aberta, andamento, finalizada, descartada), inclusive comentários da sala.
alter table brainstorm  add column if not exists status text not null default 'aberta' check (status in ('aberta','andamento','finalizada','descartada'));
alter table brainstorm  add column if not exists status_por text;
alter table brainstorm  add column if not exists status_t timestamptz;
alter table comentarios add column if not exists bs_status text not null default 'aberta' check (bs_status in ('aberta','andamento','finalizada','descartada'));
alter table comentarios add column if not exists bs_status_por text;
alter table comentarios add column if not exists bs_status_t timestamptz;
-- 22/10/2026: Basecamp por email (cada lista de to-dos do Basecamp tem endereço próprio). Cadastro por área:
create table if not exists basecamp_listas (area text primary key check (area in ('vendas','membership','parcerias','marketing')), email text not null, projeto text);
alter table basecamp_listas enable row level security;
create policy basecamp_listas_anon on basecamp_listas for select to anon using (true);
create policy basecamp_listas_auth on basecamp_listas for all to authenticated using (true) with check (true);
alter table brainstorm  add column if not exists basecamp_t timestamptz;
alter table brainstorm  add column if not exists basecamp_por text;
alter table comentarios add column if not exists bs_basecamp_t timestamptz;
alter table comentarios add column if not exists bs_basecamp_por text;
-- 22/10/2026: integração nativa com o Basecamp (edge function supabase/functions/basecamp/index.ts).
create table if not exists basecamp_auth (id int primary key default 1 check (id=1), account_id text, account_nome text, access_token text, refresh_token text, expires_at timestamptz, updated_at timestamptz default now());
alter table basecamp_auth enable row level security; -- sem políticas: só a função (service role) lê
alter table basecamp_listas alter column email drop not null;
alter table basecamp_listas add column if not exists bucket_id bigint;
alter table basecamp_listas add column if not exists todolist_id bigint;
alter table basecamp_listas add column if not exists lista text;
alter table brainstorm  add column if not exists basecamp_url text;
alter table comentarios add column if not exists bs_basecamp_url text;
-- Segredos da função: BASECAMP_CLIENT_ID e BASECAMP_CLIENT_SECRET (registro em launchpad.37signals.com/integrations,
-- redirect URI = <SUPABASE_URL>/functions/v1/basecamp/callback). Autorizar uma vez em /functions/v1/basecamp/authorize.

-- 22/10 (tarde): Basecamp por mesa. basecamp_listas ganhou account_id (conta do Basecamp da lista).
-- Mapa definitivo (rota /setup-mapa): vendas -> projeto "Vendas" (conta Haven 6302304); parcerias -> "Parcerias" (Haven);
-- membership -> "Membership Club" (Haven); marketing -> "Haven - MKT" (conta Omi 5696129). Lista "Brainstorm Bench News" em cada um.
alter table public.basecamp_listas add column if not exists account_id text;
create policy membros_anon on public.membros for select to anon using (true); -- 22/10: nomes no brainstorm v2
