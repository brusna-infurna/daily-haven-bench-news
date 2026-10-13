#!/usr/bin/env python3
"""Gera o email HTML da edição mais recente do Radar Haven.
Uso: python3 build_email.py [URL_DO_DASHBOARD]  -> escreve email-AAAA-MM-DD.html e imprime o assunto na 1a linha
"""
import json, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
URL = sys.argv[1] if len(sys.argv) > 1 else "https://brusna-infurna.github.io/daily-haven-bench-news/"
data = json.load(open(os.path.join(HERE, "radar-data.json"), encoding="utf-8"))
day = data["dias"][0]
M = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"]
y, m, d = day["data"].split("-")
data_fmt = f"{int(d)} {M[int(m)-1]}"
e = html.escape
PIL = {"wellness-residence":"Wellness residence","membership":"Membership","longevidade":"Longevidade","lifestyle":"Lifestyle","comunidade":"Comunidade"}

items = day["itens"]
leads = [i for i in items if i.get("destaque")]
rest = [i for i in items if not i.get("destaque")]
br = [i for i in rest if i["escopo"] == "brasil"]
wd = [i for i in rest if i["escopo"] == "mundo"]

subject = f"Daily Haven Bench News · {data_fmt} · {day.get('manchete','').rstrip('.')}"

def lead_html(i):
    return f"""
    <tr><td style="padding:0 0 26px 0;border-bottom:1px solid #e3ded4">
      <div style="font-size:12px;color:#3E5A42;font-weight:600;margin:22px 0 6px">{e(PIL.get(i['pilar'],i['pilar']))} <span style="color:#8a8680;font-weight:400">{'Brasil' if i['escopo']=='brasil' else 'Mundo'}</span></div>
      <div style="font-family:Georgia,'Times New Roman',serif;font-size:21px;line-height:1.3;color:#1C1A17;margin-bottom:8px"><a href="{e(i['url'])}" style="color:#1C1A17;text-decoration:none">{e(i['title'])}</a></div>
      <div style="font-size:14.5px;line-height:1.6;color:#45423C">{e(i['resumo'])}</div>
      <div style="margin-top:10px;padding:10px 14px;border-left:2px solid #3E5A42;font-size:14px;line-height:1.55;color:#1C1A17"><span style="font-family:Georgia,serif;color:#3E5A42;display:block;font-size:13px;margin-bottom:3px">O que o Haven faz com isso</span>{e(i['por_que_importa'])}</div>
      <div style="font-size:12.5px;color:#8a8680;margin-top:10px">{e(i['source'])}, {e(i['region'])}. Pra {e(', '.join(i.get('para',[])))}. <a href="{e(i['url'])}" style="color:#3E5A42">Ler na fonte</a></div>
    </td></tr>"""

def brief_html(i):
    return f"""
    <tr><td style="padding:14px 0;border-bottom:1px solid #e3ded4">
      <div style="font-family:Georgia,'Times New Roman',serif;font-size:17px;line-height:1.35;color:#1C1A17"><a href="{e(i['url'])}" style="color:#1C1A17;text-decoration:none">{e(i['title'])}</a></div>
      <div style="font-size:13.5px;line-height:1.55;color:#45423C;margin-top:4px">{e(i['por_que_importa'])}</div>
      <div style="font-size:12px;color:#8a8680;margin-top:4px">{e(PIL.get(i['pilar'],i['pilar']))}, {e(i['source'])}, {e(i['region'])}. Pra {e(', '.join(i.get('para',[])))}.</div>
    </td></tr>"""

body = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{e(subject)}</title></head>
<body style="margin:0;background:#F5F1EA;font-family:Calibri,'Segoe UI',Helvetica,Arial,sans-serif;color:#1C1A17">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#F5F1EA"><tr><td align="center" style="padding:28px 14px">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:660px;background:#FBF9F5;padding:34px 34px 28px;border-top:3px solid #3E5A42">
  <tr><td style="font-family:Georgia,'Times New Roman',serif;font-size:19px;padding-bottom:4px">Daily Haven Bench News <span style="font-family:Calibri,Arial,sans-serif;font-size:13px;color:#8a8680">edição de {data_fmt} de {y}</span></td></tr>
  <tr><td style="font-family:Georgia,'Times New Roman',serif;font-size:28px;line-height:1.18;padding:18px 0 14px;border-bottom:1px solid #1C1A17">{e(day.get('manchete',''))}</td></tr>
  <tr><td style="font-size:15px;line-height:1.65;color:#45423C;padding:18px 0 6px">{e(day.get('editorial',''))}</td></tr>
  <tr><td style="font-size:13px;color:#8a8680;padding:6px 0 20px">{len(items)} itens conferidos na fonte, {sum(1 for i in items if i['escopo']=='brasil')} do Brasil e {sum(1 for i in items if i['escopo']=='mundo')} do mundo. <a href="{e(URL)}" style="color:#3E5A42">Abrir o dashboard</a></td></tr>

  <tr><td style="background:#eef0ea;border-top:2px solid #3E5A42;padding:16px 20px 6px">
    <div style="font-family:Georgia,serif;font-size:17px;color:#2E4431;margin-bottom:8px">Pra prestar atenção</div>
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">{''.join(f'<tr><td style="padding:9px 0;border-top:1px solid #d9d6cc;font-size:14px;line-height:1.55;color:#45423C">{e(a)}</td></tr>' for a in day.get('atencao',[]))}</table>
  </td></tr>

  <tr><td style="padding-top:26px;font-size:13px;color:#8a8680;border-bottom:1px solid #1C1A17;padding-bottom:6px">Destaques</td></tr>
  {''.join(lead_html(i) for i in leads)}

  {'<tr><td style="padding-top:30px;font-size:13px;color:#8a8680;border-bottom:1px solid #1C1A17;padding-bottom:6px">Em pauta, Brasil</td></tr>' + ''.join(brief_html(i) for i in br) if br else ''}
  {'<tr><td style="padding-top:30px;font-size:13px;color:#8a8680;border-bottom:1px solid #1C1A17;padding-bottom:6px">Em pauta, mundo</td></tr>' + ''.join(brief_html(i) for i in wd) if wd else ''}

  <tr><td style="padding-top:28px;font-size:12.5px;line-height:1.6;color:#8a8680">Cada item foi aberto e conferido na fonte hoje. Conteúdo patrocinado está marcado junto ao veículo. Edições anteriores e filtros por time ficam no <a href="{e(URL)}" style="color:#3E5A42">dashboard</a>.</td></tr>
  <tr><td style="padding-top:18px;font-size:14px">Bru</td></tr>
</table>
</td></tr></table></body></html>"""

out = os.path.join(HERE, f"email-{day['data']}.html")
open(out, "w", encoding="utf-8").write(body)
print(subject)
print(out)
