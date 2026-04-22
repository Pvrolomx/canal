import requests, xml.etree.ElementTree as ET, os
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

# Leer tokens desde archivo local del RPi (nunca hardcodeados en repo)
TOKENS_FILE = os.path.expanduser("~/colmena/keys/TOKENS.md")
BOT_TOKEN = ""
CHAT_ID = "6392026932"
ANTHROPIC_KEY = ""

def load_tokens():
    global BOT_TOKEN, ANTHROPIC_KEY
    try:
        with open(TOKENS_FILE) as f:
            for line in f:
                if "BOT_TOKEN" in line or "ColmenaAgentes" in line:
                    parts = line.split(":")
                    if len(parts) >= 2:
                        candidate = line.split("=")[-1].strip().strip('"').strip("'")
                        if "AAE" in candidate and len(candidate) > 30:
                            BOT_TOKEN = candidate
                if "ANTHROPIC" in line and "sk-ant" in line:
                    ANTHROPIC_KEY = line.split("=")[-1].strip().strip('"').strip("'")
    except Exception as e:
        print(f"Error cargando tokens: {e}")
    # Fallback: variables de entorno
    BOT_TOKEN = BOT_TOKEN or os.environ.get("BOT_TOKEN", "")
    ANTHROPIC_KEY = ANTHROPIC_KEY or os.environ.get("ANTHROPIC_KEY", "")

FEEDS = [
    ("Anthropic", "https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml"),
    ("OpenAI", "https://openai.com/blog/rss.xml"),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml"),
    ("MIT Tech Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("Import AI", "https://importai.substack.com/feed"),
    ("The Batch", "https://www.deeplearning.ai/the-batch/rss/"),
    ("Xataka IA", "https://www.xataka.com/tag/inteligencia-artificial/feed"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("Reuters Tech", "https://feeds.reuters.com/reuters/technologyNews"),
]

SYSTEM_PROMPT = """Eres el duende Claude, asistente personal de Rolando Rolo Romero Garcia, abogado y asesor expat con 20 anos en Puerto Vallarta, Mexico.

CONTEXTO DE ROLO:
- Abogado especializado en fideicomisos, cesiones de derechos, inmigracion, testamentos y condominios en zona restringida de Mexico
- Clientes: 95% americanos y canadienses comprando propiedades en PV/Riviera Nayarit
- Marca: Expat Advisor MX (expatadvisormx.com)
- Su socia Claudia maneja Castle Bay PV: 20 propiedades de renta vacacional
- Ecosistema de 11 AIs llamado La Colmena, el es el Arquitecto
- Proyectos activos: FideicomisoGen, OfertaGen, AdminGen, Fantasma (USD/MXN), Castle Ops

MISION: Briefing de inteligencia personalizado. Traducir noticias IA a impacto REAL para Rolo.

ESTRUCTURA (espanol, max 3800 caracteres):
SECCION 1 - PANORAMA DEL DIA: 2-3 lineas del estado general
SECCION 2 - RIESGOS (solo si hay algo real): empleo expats tech, regulacion transfronteriza, fraude, cambios en plataformas
SECCION 3 - OPORTUNIDADES: herramientas que Rolo puede aprovechar en su practica o La Colmena
SECCION 4 - PARA ESTAR AL TANTO: 2-3 bullets sin urgencia
SECCION 5 - PARA LA COLMENA: modelos nuevos, APIs, pricing para la infraestructura

REGLAS:
- Directo, sin paja academica. Si una noticia no impacta a Rolo, ignorala.
- Prioriza: derecho, proptech, empleo expats americanos/canadienses, regulacion IA en US/Mexico/Canada, modelos nuevos
- Emojis con moderacion. Cierra con linea motivacional breve."""

def parse_feed(source, url, cutoff):
    arts = []
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(r.content)
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        for item in items[:5]:
            title = (item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
            link_el = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
            link = (item.findtext("link") or (link_el.get("href") if link_el is not None else "") or "").strip()
            desc = (item.findtext("description") or item.findtext("{http://www.w3.org/2005/Atom}summary") or "").strip()[:300]
            pub_str = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}updated") or ""
            try:
                pub_dt = parsedate_to_datetime(pub_str).astimezone(timezone.utc) if pub_str else None
                if pub_dt and pub_dt < cutoff:
                    continue
            except:
                pass
            if title:
                arts.append({"source": source, "title": title, "link": link, "summary": desc})
        print(f"OK {source}: {len(arts)} arts")
    except Exception as ex:
        print(f"SKIP {source}: {ex}")
    return arts

def get_articles(hours=28):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    arts = []
    for source, url in FEEDS:
        arts.extend(parse_feed(source, url, cutoff))
    return arts

def synthesize(arts):
    fecha = datetime.now().strftime("%d %b %Y")
    if not arts:
        user_content = "No hay articulos nuevos en feeds RSS hoy. Genera briefing con 2-3 tendencias macro de IA relevantes para Rolo."
    else:
        texto = "\n\n".join([f"[{a['source']}] {a['title']}\n{a['summary']}" for a in arts[:30]])
        user_content = f"Fecha: {fecha}\n\nNoticias IA ultimas 28 horas:\n\n{texto}\n\nGenera el briefing personalizado para Rolo."
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"},
        json={"model": "claude-sonnet-4-20250514", "max_tokens": 1500, "system": SYSTEM_PROMPT,
              "messages": [{"role": "user", "content": user_content}]},
        timeout=45
    )
    return r.json()["content"][0]["text"]

def send_telegram(text):
    for i in range(0, len(text), 4000):
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text[i:i+4000], "parse_mode": "Markdown"},
            timeout=10
        )
        print(r.status_code, r.text[:100])

if __name__ == "__main__":
    load_tokens()
    if not BOT_TOKEN or not ANTHROPIC_KEY:
        print("ERROR: No se pudieron cargar los tokens desde TOKENS.md")
        exit(1)
    print("Leyendo feeds...")
    arts = get_articles()
    print(f"Total: {len(arts)} articulos")
    print("Sintetizando con Claude Sonnet...")
    briefing = synthesize(arts)
    print("--- BRIEFING ---")
    print(briefing)
    print("Enviando Telegram...")
    send_telegram(briefing)
    print("Listo")
