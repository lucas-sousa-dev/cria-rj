"""Coleta metadados de RSS públicos; não republica textos nem imagens protegidos."""
import datetime as dt
import email.utils
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "noticias.json"
BASE = "https://news.google.com/rss/search?q={}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
SEARCHES = [
    ("famosos", '(site:gshow.globo.com OR site:leodias.com OR site:caras.com.br OR site:revistaquem.globo.com OR site:ofuxico.com.br OR site:sbt.com.br) (famosos OR atriz OR cantor OR celebridades OR novela) when:7d'),
    ("famosos", '(site:metropoles.com OR site:odia.ig.com.br OR site:terra.com.br OR site:extra.globo.com) (celebridades OR famosos OR entretenimento) when:7d'),
    ("rio", '(site:g1.globo.com OR site:odia.ig.com.br OR site:extra.globo.com OR site:prefeitura.rio) "Rio de Janeiro" when:7d'),
    ("brasil", '(site:agenciabrasil.ebc.com.br OR site:g1.globo.com OR site:cnnbrasil.com.br OR site:correiobraziliense.com.br) Brasil when:7d'),
    ("politica", '(site:senado.leg.br OR site:camara.leg.br OR site:agenciabrasil.ebc.com.br OR site:estadao.com.br) política when:7d'),
    ("esportes", '(site:ge.globo.com OR site:espn.com.br OR site:terra.com.br) futebol when:7d'),
    ("economia", '(site:valor.globo.com OR site:infomoney.com.br OR site:agenciabrasil.ebc.com.br) economia when:7d'),
    ("bemestar", '(site:fiocruz.br OR site:saude.gov.br OR site:bbc.com OR site:g1.globo.com) saúde bem-estar when:7d'),
    ("mundo", '(site:bbc.com OR site:dw.com OR site:cnnbrasil.com.br) internacional when:7d'),
    ("tecnologia", '(site:tecnoblog.net OR site:canaltech.com.br OR site:olhardigital.com.br) tecnologia when:7d'),
]
FEEDS = [("Agência Brasil", "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml", None)]
for category, query in SEARCHES:
    FEEDS.append(("Google Notícias", BASE.format(quote(query)), category))

def published(value):
    try:
        return email.utils.parsedate_to_datetime(value).astimezone(dt.timezone.utc).isoformat()
    except (TypeError, ValueError, IndexError):
        return ""

def category_for(title):
    t = title.lower()
    if re.search(r"\b(rio de janeiro|carioca|niterói|copacabana|maracanã)\b", t): return "rio"
    if re.search(r"\b(atriz|ator|cantor|celebridade|famosos|novela|influenciador)\b", t): return "famosos"
    if re.search(r"\b(futebol|campeonato|flamengo|vasco|botafogo|fluminense)\b", t): return "esportes"
    if re.search(r"\b(vacina|saúde|hospital|doença|bem-estar)\b", t): return "bemestar"
    if re.search(r"\b(tecnologia|software|inteligência artificial|celular)\b", t): return "tecnologia"
    if re.search(r"\b(senado|congresso|deputado|presidente|eleição)\b", t): return "politica"
    if re.search(r"\b(economia|inflação|juros|dólar|pib)\b", t): return "economia"
    return "brasil"

def load_old():
    try:
        data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        return data.get("noticias", []) if isinstance(data.get("noticias"), list) else []
    except (OSError, ValueError, AttributeError):
        return []

def collect():
    result = []
    for feed_name, url, assigned in FEEDS:
        try:
            request = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; CentralDeNoticiasRSS/1.0)",
                "Accept": "application/rss+xml, application/xml, text/xml",
            })
            with urllib.request.urlopen(request, timeout=18) as response:
                xml = response.read(2_500_000)
            root = ET.fromstring(xml)
            items = root.findall("./channel/item")
            count = 0
            for item in items[:30]:
                title = " ".join((item.findtext("title") or "").split())
                link = (item.findtext("link") or "").strip()
                if not title or len(title) > 220 or not link.startswith("https://"):
                    continue
                host = (urlsplit(link).hostname or "").lower()
                if host not in ("news.google.com", "agenciabrasil.ebc.com.br", "www.agenciabrasil.ebc.com.br"):
                    continue
                source = item.find("source")
                publisher = (source.text or "").strip() if source is not None else feed_name
                if host == "news.google.com" and not publisher:
                    continue
                if host == "news.google.com" and title.endswith(" - " + publisher):
                    title = title[:-(len(publisher) + 3)]
                result.append({
                    "titulo": title,
                    "resumo": "",
                    "fonte": link,
                    "veiculo": publisher,
                    "data": published(item.findtext("pubDate")),
                    "categoria": assigned or category_for(title),
                })
                count += 1
            print(f"{assigned or feed_name}: {count} manchetes")
        except Exception as exc:
            print(f"Falha {assigned or feed_name}: {type(exc).__name__}: {exc}")
    return result

def main():
    old = load_old()
    fresh = collect()
    unique = {}
    for item in fresh + old:
        link = item.get("fonte", "")
        if isinstance(link, str) and link.startswith("https://") and item.get("titulo") and item.get("veiculo"):
            unique.setdefault(link, item)
    ordered = sorted(unique.values(), key=lambda item: item.get("data", ""), reverse=True)
    # Reservar manchetes de cada editoria para que categorias menores não desapareçam.
    selected, used = [], set()
    for cat in ("famosos", "rio", "brasil", "politica", "esportes", "economia", "bemestar", "mundo", "tecnologia"):
        for item in (x for x in ordered if x.get("categoria") == cat):
            if sum(x.get("categoria") == cat for x in selected) >= 20:
                break
            if item["fonte"] not in used:
                selected.append(item)
                used.add(item["fonte"])
    selected = sorted(selected, key=lambda item: item.get("data", ""), reverse=True)[:180]
    if not selected and old:
        print("Nenhuma manchete recebida: preservando arquivo existente")
        return
    OUTPUT.write_text(json.dumps({"noticias": selected}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Total: {len(selected)} manchetes")

if __name__ == "__main__":
    main()
