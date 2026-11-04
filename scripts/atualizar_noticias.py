"""Busca manchetes RSS, publica apenas metadados e links; não copia artigos."""
import datetime as dt
import email.utils
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "noticias.json"
FEEDS = [
    ("Agência Brasil", "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml"),
]
RIO = re.compile(r"\b(rio de janeiro|carioca|fluminense|copacabana|ipanema|leblon|zona sul|zona norte|zona oeste|maracanã|niterói|são gonçalo|baixada fluminense|são conrado)\b", re.I)
TECH = re.compile(r"\b(tecnologia|inteligência artificial|software|internet|aplicativo|digital|inovação|computador|pesquisa científica)\b", re.I)
HEALTH = re.compile(r"\b(saúde|vacina|hospital|sus|doença|dengue|medicamento|epidemia)\b", re.I)
DAILY = re.compile(r"\b(emprego|trabalho|salário|transporte|metrô|ônibus|economia|inflação|preço|consumidor|educação|concurso)\b", re.I)

def categoria(text):
    if RIO.search(text): return "rio"
    if TECH.search(text): return "tecnologia"
    if HEALTH.search(text): return "saude"
    if DAILY.search(text): return "cotidiano"
    return "brasil"

def data_item(raw):
    try:
        return email.utils.parsedate_to_datetime(raw).astimezone(dt.timezone.utc).isoformat()
    except (TypeError, ValueError, IndexError):
        return ""

def carregar():
    try:
        dados = json.loads(OUTPUT.read_text(encoding="utf-8"))
        return dados.get("noticias", [])
    except (FileNotFoundError, ValueError, AttributeError):
        return []

def main():
    antigas = carregar()
    coletadas = []
    for nome, feed in FEEDS:
        try:
            req = urllib.request.Request(feed, headers={"User-Agent": "CriaRJ-RSS/1.0 (leitor de manchetes)", "Accept": "application/rss+xml, application/xml, text/xml"})
            with urllib.request.urlopen(req, timeout=25) as response:
                root = ET.fromstring(response.read(3_000_000))
            items = root.findall(".//channel/item")
            if not items:
                print(f"Sem itens RSS em {nome}")
                continue
            for item in items[:90]:
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                if not title or len(title) > 220 or not link.startswith("https://"):
                    continue
                host = (urlsplit(link).hostname or "").lower()
                if host != "agenciabrasil.ebc.com.br":
                    continue
                # Não republicar corpo, descrição nem imagens do veículo.
                coletadas.append({
                    "titulo": title,
                    "resumo": "",
                    "fonte": link,
                    "veiculo": nome,
                    "data": data_item(item.findtext("pubDate")),
                    "categoria": categoria(title),
                })
            print(f"{nome}: {len(items)} itens encontrados")
        except Exception as exc:
            print(f"Falha em {nome}: {type(exc).__name__}: {exc}")
    if not coletadas and antigas:
        print("Sem notícias novas: preservando dados existentes")
        return
    unicas = {}
    for item in coletadas + antigas:
        url = item.get("fonte", "")
        if url.startswith("https://") and urlsplit(url).hostname == "agenciabrasil.ebc.com.br":
            unicas.setdefault(url, item)
    recentes = sorted(unicas.values(), key=lambda n: n.get("data", ""), reverse=True)[:90]
    payload = {"noticias": recentes}
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Gravadas {len(recentes)} manchetes")

if __name__ == "__main__":
    main()
