# Sala do Time no domínio próprio

Versão da Sala do Time pra rodar em www.projetorepertorio.com.br/benchnews/sala/, com Supabase como banco. Desde 22/10 a sala é aberta: quem tem o link entra, escolhe o nome uma vez (fica no aparelho) e esse nome assina o que escreve. Login por email foi desligado. Mesmo layout do site e da sala do claude.ai. Sem a pergunta ao Claude por enquanto (segunda fase, precisa de chave de API e de uma função no meio).

A página é estática e lê o radar-data.json do GitHub Pages ao abrir, então não precisa ser regerada a cada edição. Só muda quando mudar o layout ou a lista de membros.

## Passo a passo (uma vez)

1. Criar conta em supabase.com (plano gratuito) e um projeto (região South America, São Paulo). Guardar a senha do banco.
2. No projeto, abrir SQL Editor, colar o conteúdo de `schema.sql` e rodar. Antes de rodar, trocar `TROQUE-POR-UM-SEGREDO-LONGO` por um segredo longo (é o token que a rotina da manhã usa pra ler a sala). Conferir a lista de membros e os nomes na tabela `membros`; é aí que entra ou sai gente.
3. Em Authentication > Providers > Email: deixar Email ligado, desligar "Confirm email" se quiser entrada mais rápida, e manter "Enable sign ups" ligado (quem não está em `membros` entra mas não vê nada).
4. Em Authentication > URL Configuration: Site URL = https://www.projetorepertorio.com.br/benchnews/sala/ e a mesma URL em Redirect URLs.
5. Em Project Settings > API, copiar Project URL e a chave `anon public`. Mandar as duas pra Bru/Claude numa conversa com o repositório projeto-repertorio conectado.
6. Gerar a página: no repositório daily-haven-bench-news, `python3 build_sala_dominio.py URL CHAVE_ANON benchnews/sala/index.html` e subir o arquivo em `benchnews/sala/index.html` no repositório projeto-repertorio. O arquivo `index.html` desta pasta já está gerado com placeholders; dá pra editar à mão as duas constantes no topo do script (`SB_URL`, `SB_KEY`) em vez de rodar o build.
7. Opcional: o email diário passa a apontar o botão "Entrar na sala do time" pra https://www.projetorepertorio.com.br/benchnews/sala/ (variável SALA em build_email.py).

## Rotina da manhã

Leitura (GET, funciona com WebFetch): `URL/rest/v1/rpc/sala_export?apikey=CHAVE_PUBLISHABLE&select=*&p_token=SEGREDO&limit=5`. A função precisa estar marcada `stable`.

Resposta a uma pauta: a rotina não grava no Supabase (só faz GET). Ela escreve em radar-data.json, no topo, `respostas_sala: {"<id da pauta>": {"edicao": "AAAA-MM-DD", "resposta": "texto"}}`, e a página cruza pelo id. A função sala_responder fica no banco como alternativa manual.

O segredo fica no prompt da tarefa agendada (privado da conta da Bru), nunca na página.

## Quem vê o quê

Só membro logado lê e escreve. Cada um apaga só o próprio comentário e a própria pauta; `admin` (Bru) apaga qualquer um. Status e responsável das ideias qualquer membro muda. Visitante sem login vê só a tela de entrada.

## 22/10, noite: v2 no ar
Home e sala passaram pra `build_v2.py` (régua fixa com atalhos de seção, filtros em chips, mural com cartão de estrutura fixa, faixa ao vivo com contadores na sala). As páginas leem o radar-data.json ao abrir, então não precisam ser regeradas a cada edição. `build.py` continua sendo rodado pela rotina da manhã e, no fim, gera a v2 como `index.html` (o template antigo fica só como base de CSS). Pra regerar à mão: `python3 build_v2.py home oficial destino` e `python3 build_v2.py sala oficial URL CHAVE_ANON destino`. `build_sala_dominio.py` ficou como referência; não é mais usado. Pendente: a rotina passar a gerar um campo `titulo` em cada item do bench, que a v2 mostra como manchete do bloco.
