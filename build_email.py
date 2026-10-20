#!/usr/bin/env python3
"""Gera o email HTML da edição mais recente do Daily Haven Bench News.
Uso: python3 build_email.py [URL_DO_DASHBOARD]  -> escreve email-AAAA-MM-DD.html e imprime o assunto na 1a linha
Layout: revista Haven, tabela compatível com Gmail e Apple Mail, estilos inline.
"""
import json, os, sys, html, urllib.parse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else "https://brusna-infurna.github.io/daily-haven-bench-news/"
data = json.load(open(os.path.join(HERE, "radar-data.json"), encoding="utf-8"))
day = data["dias"][0]
NUM = len(data["dias"])
M = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
ML = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]
W = ["segunda-feira","terça-feira","quarta-feira","quinta-feira","sexta-feira","sábado","domingo"]
y, m, d = (int(x) for x in day["data"].split("-"))
data_fmt = f"{d} {M[m-1]}"
data_long = f"{W[datetime.date(y,m,d).weekday()]}, {d} de {ML[m-1]} de {y}"
e = html.escape
PIL = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade","estudos":"Estudos","eventos":"Eventos","marcas":"Marcas"}
PC = {"wellness-residence":"#2F6400","membership":"#C75937","longevidade":"#45958D","lifestyle":"#74386B","comunidade":"#DA9321","estudos":"#174900","eventos":"#3F3832","marcas":"#C3BFA8"}

# tokens
IVORY, PAPER, INK, ESPRESSO, SOFT, MUTE, RULE, TERRA = "#ECE8E4", "#F4F1ED", "#2B2622", "#3F3832", "#5B544D", "#857D74", "#D9D4CC", "#C75937"
SERIF = "'Playfair Display',Georgia,'Times New Roman',serif"
SERIF2 = "'Cormorant Garamond',Georgia,'Times New Roman',serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"
KICK = f"font-family:{SANS};font-size:10px;letter-spacing:2.4px;text-transform:uppercase;color:{INK}"
KICK_MUTE = f"font-family:{SANS};font-size:10px;letter-spacing:1.6px;text-transform:uppercase;color:{MUTE}"

items = day["itens"]
leads = [i for i in items if i.get("destaque")]
rest = [i for i in items if not i.get("destaque")]
br = [i for i in rest if i["escopo"] == "brasil"]
wd = [i for i in rest if i["escopo"] == "mundo"]
n_br = sum(1 for i in items if i["escopo"] == "brasil")
n_wd = len(items) - n_br

subject = f"Daily Haven Bench News · {data_fmt} · {day.get('manchete','').rstrip('.')}"
wa_text = f"*Daily Haven Bench News, {data_fmt}*\n\n{day.get('manchete','')}\n\nPra prestar atenção:\n" + "\n".join(f"• {a}" for a in day.get('atencao',[])) + f"\n\nDashboard: {URL}"
wa_link = "https://wa.me/?text=" + urllib.parse.quote(wa_text)

def fmt_short(dt):
    yy, mm, dd = dt.split("-")
    return f"{int(dd)} {M[int(mm)-1]}"

def tag(i):
    return (f'<table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>'
            f'<td style="{KICK};padding:0"><span style="display:inline-block;width:22px;height:3px;background:{PC.get(i["pilar"],ESPRESSO)};vertical-align:middle;margin-right:9px"></span>{e(PIL.get(i["pilar"],i["pilar"]))}</td>'
            f'<td align="right" style="{KICK_MUTE};padding:0;white-space:nowrap">{"Brasil" if i["escopo"]=="brasil" else "Mundo"} · {e(i["region"])}</td></tr></table>')

def lead_html(i):
    return f"""
  <tr><td style="padding:26px 0 28px;border-bottom:1px solid {RULE}">
    {tag(i)}
    <div style="font-family:{SERIF};font-weight:500;font-size:24px;line-height:1.2;color:{INK};margin:12px 0 10px"><a href="{e(i['url'])}" style="color:{INK};text-decoration:none">{e(i['title'])}</a></div>
    <div style="font-family:{SERIF2};font-size:17px;line-height:1.5;color:{ESPRESSO}">{e(i['resumo'])}</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top:14px"><tr>
      <td style="width:2px;background:{TERRA}"></td>
      <td style="padding:4px 0 2px 14px"><div style="font-family:{SANS};font-size:10px;letter-spacing:2.2px;text-transform:uppercase;color:{TERRA};margin-bottom:5px">O que o Haven faz com isso</div>
      <div style="font-family:{SERIF2};font-size:16.5px;line-height:1.45;color:{INK}">{e(i['por_que_importa'])}</div></td>
    </tr></table>
    <div style="{KICK_MUTE};margin-top:14px"><a href="{e(i['url'])}" style="color:{SOFT};text-decoration:underline">{e(i['source'])}</a> · {fmt_short(i['date'])} · {e(' · '.join(i.get('para',[])))}</div>
  </td></tr>"""

def brief_html(i):
    return f"""
  <tr><td style="padding:18px 0;border-bottom:1px solid {RULE}">
    {tag(i)}
    <div style="font-family:{SERIF};font-weight:500;font-size:19px;line-height:1.25;color:{INK};margin:9px 0 6px"><a href="{e(i['url'])}" style="color:{INK};text-decoration:none">{e(i['title'])}</a></div>
    <div style="font-family:{SERIF2};font-size:16px;line-height:1.45;color:{ESPRESSO}">{e(i['por_que_importa'])}</div>
    <div style="{KICK_MUTE};margin-top:8px"><a href="{e(i['url'])}" style="color:{SOFT};text-decoration:underline">{e(i['source'])}</a> · {fmt_short(i['date'])} · {e(' · '.join(i.get('para',[])))}</div>
  </td></tr>"""

def sec(title, note=""):
    return (f'<tr><td style="padding:34px 0 0"><table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>'
            f'<td style="{KICK};letter-spacing:3px;padding-bottom:8px;border-bottom:1px solid {ESPRESSO}">{e(title)}</td>'
            f'<td align="right" style="font-family:{SERIF2};font-style:italic;font-size:16px;color:{MUTE};padding-bottom:8px;border-bottom:1px solid {ESPRESSO}">{e(note)}</td></tr></table></td></tr>')

def watch_html(a):
    a = str(a)
    if ":" in a and len(a.split(":",1)[0]) <= 24:
        lab, txt = a.split(":",1)
        lab = f'<div style="{KICK};font-weight:bold;margin-bottom:4px">{e(lab.strip())}</div>'
        txt = txt.strip()
    else:
        lab, txt = "", a
    return lab, txt

watch_rows = ""
for n, a in enumerate(day.get("atencao", []), 1):
    lab, txt = watch_html(a)
    watch_rows += (f'<tr><td valign="top" style="width:28px;padding:14px 0 0;border-top:1px solid {RULE};font-family:{SANS};font-size:10px;letter-spacing:1.5px;color:{TERRA}">{n:02d}</td>'
                   f'<td valign="top" style="padding:12px 0 14px;border-top:1px solid {RULE}">{lab}<div style="font-family:{SERIF2};font-size:17.5px;line-height:1.42;color:{ESPRESSO}">{e(txt)}</div></td></tr>')

bench_rows = ""
for n, b in enumerate(day.get("bench", []), 1):
    ref = ""
    if b.get("ref"):
        link = f'<a href="{e(b["url"])}" style="color:{SOFT};text-decoration:underline">{e(b["ref"])}</a>' if b.get("url") else e(b["ref"])
        ref = f'<div style="{KICK_MUTE};margin-top:7px"><span style="color:{INK};font-weight:bold">A partir de</span> {link}</div>'
    bench_rows += (f'<tr><td valign="top" style="width:28px;padding:14px 0 0;border-top:1px solid {RULE};font-family:{SANS};font-size:10px;letter-spacing:1.5px;color:{TERRA}">{n:02d}</td>'
                   f'<td valign="top" style="padding:12px 0 14px;border-top:1px solid {RULE}"><div style="{KICK};color:{TERRA};font-weight:bold;margin-bottom:4px">{e(b.get("area") or b.get("para",""))}</div>'
                   f'<div style="font-family:{SERIF2};font-size:17.5px;line-height:1.42;color:{ESPRESSO}">{e(b["ideia"])}</div>{ref}</td></tr>')
bench_block = f"""
  <!-- bench pro Haven -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top:30px;border-top:3px solid {TERRA}">
    <tr><td colspan="2" style="font-family:{SERIF};font-style:italic;font-weight:500;font-size:26px;line-height:1.1;color:{INK};padding:16px 0 2px">Bench pro Haven</td></tr>
    <tr><td colspan="2" style="font-family:{SERIF2};font-style:italic;font-size:16px;color:{MUTE};padding:0 0 8px">referências do dia aplicadas ao projeto: produto, membership, comercialização, comunicação, parcerias</td></tr>
    {bench_rows}
  </table>""" if bench_rows else ""

body = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(subject)}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400;1,500&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap" rel="stylesheet"></head>
<body style="margin:0;padding:0;background:{IVORY};color:{INK};font-family:{SANS}">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{IVORY}"><tr><td align="center" style="padding:24px 12px 40px">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:640px;background:{PAPER}">
<tr><td style="padding:26px 30px 30px">

  <!-- masthead -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
    <tr><td style="border-top:1px solid {ESPRESSO};height:2px;line-height:2px;font-size:2px">&nbsp;</td></tr>
    <tr><td style="border-top:1px solid {ESPRESSO};padding:14px 0 0;text-align:center;{KICK}">Radar diário de wellness, membership e longevidade</td></tr>
    <tr><td align="center" style="font-family:{SERIF};font-weight:500;font-size:40px;line-height:1;letter-spacing:-0.5px;color:{INK};padding:12px 0 10px">Daily Haven Bench News</td></tr>
    <tr><td style="text-align:center;padding:0 0 12px;border-bottom:1px solid {ESPRESSO};{KICK}">Pra parcerias, marketing, vendas e clube</td></tr>
    <tr><td style="border-bottom:1px solid {ESPRESSO};height:2px;line-height:2px;font-size:2px">&nbsp;</td></tr>
  </table>
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0"><tr>
    <td style="padding:10px 0;border-bottom:1px solid {RULE};{KICK_MUTE}">Nº {NUM} · {e(data_long)}</td>
    <td align="right" style="padding:10px 0;border-bottom:1px solid {RULE};{KICK_MUTE}">{len(items)} itens · {n_br} Brasil · {n_wd} mundo</td>
  </tr></table>

  <!-- abertura -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
    <tr><td style="font-family:{SERIF};font-weight:500;font-size:34px;line-height:1.12;letter-spacing:-0.3px;color:{INK};padding:30px 0 18px">{e(day.get('manchete',''))}</td></tr>
    <tr><td style="font-family:{SERIF2};font-size:19px;line-height:1.5;color:{ESPRESSO};padding:0 0 22px">{e(day.get('editorial',''))}</td></tr>
    <tr><td style="{KICK_MUTE};padding:0 0 14px"><a href="{e(URL)}" style="color:{TERRA};text-decoration:none;border-bottom:1px solid {TERRA}">Abrir a edição completa no site</a></td></tr>
    <tr><td style="padding:0 0 26px"><a href="{e(wa_link)}" style="display:inline-block;background:{ESPRESSO};color:#F5F1EA;text-decoration:none;font-family:{SANS};font-size:13px;padding:11px 18px;border-radius:4px">Mandar pro grupo no WhatsApp</a><span style="font-family:{SANS};font-size:12px;color:{MUTE};margin-left:10px">abre o WhatsApp com a mensagem pronta, é só escolher o grupo</span></td></tr>
  </table>

  <!-- pra prestar atenção -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-top:3px solid {TERRA}">
    <tr><td colspan="2" style="font-family:{SERIF};font-style:italic;font-weight:500;font-size:26px;line-height:1.1;color:{INK};padding:16px 0 10px">Pra prestar atenção</td></tr>
    {watch_rows}
  </table>
{bench_block}

  <!-- destaques -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
    {sec('Destaques', 'o que merece leitura inteira') if leads else ''}
    {''.join(lead_html(i) for i in leads)}
    {sec('Em pauta · Brasil', f"{len(br)} {'itens' if len(br)>1 else 'item'}") if br else ''}
    {''.join(brief_html(i) for i in br)}
    {sec('Em pauta · Mundo', f"{len(wd)} {'itens' if len(wd)>1 else 'item'}") if wd else ''}
    {''.join(brief_html(i) for i in wd)}
  </table>

  <!-- rodapé -->
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin-top:36px;border-top:1px solid {ESPRESSO}"><tr>
    <td style="padding:14px 0 0;font-family:{SANS};font-size:12px;line-height:1.6;color:{MUTE}">Cada item foi aberto e conferido na fonte hoje. Conteúdo patrocinado está marcado junto ao veículo. Edições anteriores e filtros por time ficam no <a href="{e(URL)}" style="color:{TERRA}">site</a>.</td>
    <td align="right" valign="top" style="padding:12px 0 0 20px;font-family:{SERIF};font-style:italic;font-size:20px;color:{ESPRESSO}">Bru</td>
  </tr></table>

</td></tr></table>
</td></tr></table></body></html>"""

out = os.path.join(HERE, f"email-{day['data']}.html")
open(out, "w", encoding="utf-8").write(body)
print(subject)
print(out)
