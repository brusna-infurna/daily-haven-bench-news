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
