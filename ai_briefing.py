import requests, xml.etree.ElementTree as ET, os
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

TOKENS_FILE = os.path.expanduser("~/colmena/keys/TOKENS.md")
BOT_TOKEN = "8498803967:AAEeq_jSQwOiWDXWLBYXXpzep18MVrCebj8"
CHAT_ID = "6392026932"

def load_tokens():
    global BOT_TOKEN
    try:
        with open(TOKENS_FILE) as f:
            for line in f:
                if "AAE" in line and len(line.strip()) > 30:
                    for part in line.split():
                        if part.startswith("8") and "AAE" in part:
                            BOT_TOKEN = part.strip().strip('"').strip("'")
    except:
        pass
    BOT_TOKEN = BOT_TOKEN or os.environ.get("BOT_TOKEN", "8498803967:AAEeq_jSQwOiWDXWLBYXXpzep18MVrCebj8")

FEEDS = [
    ("Anthropic", "https://raw.githubusercontent.com/taobojlen/anthropic-rss-feed/main/anthropic_news_rss.xml"),
    ("OpenAI", "https://openai.com/blog/rss.xml"),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml"),
    ("MIT Tech Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("The Verge AI", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("VentureBeat AI", "https://venturebeat.com/category/ai/feed/"),
    ("Reuters Tech", "https://feeds.reuters.com/reuters/technologyNews"),
    ("Xataka IA", "https://www.xataka.com/tag/inteligencia-artificial/feed"),
    ("Import AI", "https://importai.substack.com/feed"),
]

def parse_feed(source, url, cutoff):
    arts = []
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(r.content)
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
        for item in items[:3]:
            title = (item.findtext("title") or item.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
            link_el = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
            link = (item.findtext("link") or (link_el.get("href") if link_el is not None else "") or "").strip()
            pub_str = item.findtext("pubDate") or item.findtext("{http://www.w3.org/2005/Atom}updated") or ""
            try:
                pub_dt = parsedate_to_datetime(pub_str).astimezone(timezone.utc) if pub_str else None
                if pub_dt and pub_dt < cutoff:
                    continue
            except:
                pass
            if title and link:
                arts.append({"source": source, "title": title, "link": link})
    except:
        pass
    return arts

def get_top5(hours=28):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    all_arts = []
    for source, url in FEEDS:
        all_arts.extend(parse_feed(source, url, cutoff))
    return all_arts[:5]

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": False},
        timeout=10
    )

if __name__ == "__main__":
    load_tokens()
    if not BOT_TOKEN:
        print("ERROR: No BOT_TOKEN")
        exit(1)
    arts = get_top5()
    if not arts:
        send_telegram("_(sin noticias nuevas en las ultimas 28h)_")
    else:
        lines = []
        for a in arts:
            lines.append(f"[{a['title']}]({a['link']})")
        send_telegram("\n\n".join(lines))
    print("Listo")
