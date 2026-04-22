from datetime import datetime
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urljoin

import pandas as pd
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.instagram.com"
MAX_POSTS = 10
PUBLIC_DIR = Path("frontend/public")

# Patrones para detectar metricas tanto en texto visible como en HTML.
LIKE_PATTERNS = (
    r"(\d[\d.,]*)\s+likes?",
    r"(\d[\d.,]*)\s+me gusta",
    r"a\s+(\d[\d.,]*)\s+personas\s+les\s+gusta",
)
COMMENT_PATTERNS = (
    r"(\d[\d.,]*)\s+comments?",
    r"(\d[\d.,]*)\s+comentarios?",
    r"view all\s+(\d[\d.,]*)\s+comments?",
    r"ver los\s+(\d[\d.,]*)\s+comentarios?",
)
HTML_LIKE_PATTERNS = (
    r'"like_count"\s*:\s*(\d+)',
    r'"likers_count"\s*:\s*(\d+)',
    r'"edge_media_preview_like"\s*:\s*\{"count"\s*:\s*(\d+)',
)
HTML_COMMENT_PATTERNS = (
    r'"comment_count"\s*:\s*(\d+)',
    r'"edge_media_to_comment"\s*:\s*\{"count"\s*:\s*(\d+)',
    r'"edge_media_to_parent_comment"\s*:\s*\{"count"\s*:\s*(\d+)',
)


def clean_text(value):
    # Normaliza espacios y caracteres especiales del texto que devuelve Instagram.
    return re.sub(r"\s+", " ", str(value or "").replace("\xa0", " ")).strip()


def parse_metric(value):
    # Convierte formatos como "1.2k" o "60 M" a enteros.
    text = clean_text(value).lower()
    if not text:
        return None

    match = re.search(r"(\d+(?:[.,]\d+)?)\s*(k|m|mil)?", text)
    if not match:
        digits = re.sub(r"\D", "", text)
        return int(digits) if digits else None

    number = float(match.group(1).replace(",", "."))
    factor = {"k": 1_000, "mil": 1_000, "m": 1_000_000}.get(match.group(2), 1)
    return int(number * factor) if factor > 1 else int(re.sub(r"\D", "", match.group(1)))


def format_date(value):
    # Convierte la fecha ISO de Instagram a un formato mas legible.
    value = clean_text(value)
    if not value:
        return "N/A"

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00")) if value.endswith("Z") else datetime.fromisoformat(value)
        if parsed.tzinfo:
            parsed = parsed.astimezone()
        return parsed.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value


def match_metric(text, patterns, parser=parse_metric, flags=0):
    # Prueba varios patrones hasta encontrar una coincidencia valida.
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return parser(match.group(1))
    return None


def hashtags_from_text(text):
    # Extrae hashtags unicos desde texto libre.
    hashtags, seen = [], set()
    for tag in re.findall(r"#\w+", clean_text(text)):
        if tag.lower() not in seen:
            seen.add(tag.lower())
            hashtags.append(tag)
    return hashtags[:10]


def extract_hashtags(page, fallback_text, article_text):
    # Primero busca links reales de hashtags; si no hay, usa el texto visible.
    links = page.locator("a[href*='/explore/tags/']")
    hashtags, seen = [], set()

    for i in range(links.count()):
        href = clean_text(links.nth(i).get_attribute("href"))
        text = clean_text(links.nth(i).inner_text())
        if not text.startswith("#") and href:
            slug = href.rstrip("/").split("/")[-1]
            text = f"#{slug}" if slug else ""
        if text.startswith("#") and text.lower() not in seen:
            seen.add(text.lower())
            hashtags.append(text)

    if hashtags:
        return hashtags[:10]

    hashtags = hashtags_from_text(article_text)
    return hashtags or hashtags_from_text(fallback_text)


def extract_post(page):
    # Reune texto visible y metadatos para sacar likes, comentarios, fecha y hashtags.
    description = ""
    for selector in ("meta[name='description']", "meta[property='og:description']"):
        locator = page.locator(selector)
        if locator.count():
            description = clean_text(locator.first.get_attribute("content"))
            if description:
                break

    article = page.locator("article")
    article_text = clean_text(article.first.inner_text()) if article.count() else ""
    text = f"{description} {article_text}".lower()

    likes = match_metric(text, LIKE_PATTERNS)
    comments = match_metric(text, COMMENT_PATTERNS)

    if comments is None:
        items = page.locator("article ul li")
        comments = max(items.count() - 1, 0) if items.count() else 0

    if likes is None or comments == 0:
        # Algunas cuentas grandes esconden metricas en HTML embebido.
        html = page.content()
        if likes is None:
            likes = match_metric(html, HTML_LIKE_PATTERNS, parser=int, flags=re.IGNORECASE)
        if comments == 0:
            html_comments = match_metric(html, HTML_COMMENT_PATTERNS, parser=int, flags=re.IGNORECASE)
            if html_comments is not None:
                comments = html_comments

    time_locator = page.locator("time")
    raw_date = clean_text(time_locator.first.get_attribute("datetime")) if time_locator.count() else ""

    return {
        "likes": likes,
        "comments": comments,
        "date": format_date(raw_date),
        "hashtags": extract_hashtags(page, description, article_text),
    }


def collect_post_urls(page):
    # Hace scroll en el perfil hasta reunir las URLs de los primeros posts.
    urls, seen = [], set()

    for _ in range(6):
        links = page.locator("a[href*='/p/']")
        for i in range(links.count()):
            href = links.nth(i).get_attribute("href")
            if not href:
                continue

            post_url = urljoin(BASE_URL, href.split("?")[0])
            if post_url not in seen:
                seen.add(post_url)
                urls.append(post_url)
            if len(urls) >= MAX_POSTS:
                return urls

        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(1200)

    return urls


def save_data(username, data):
    # Actualiza un solo JSON consolidado y un Excel sin duplicar publicaciones por URL.
    unified_file = Path("scraping_data.json")
    excel_file = Path("scraping_data.xlsx")

    try:
        users = {
            item["username"]: item
            for item in json.loads(unified_file.read_text(encoding="utf-8"))
            if isinstance(item, dict) and item.get("username")
        }
    except Exception:
        users = {}

    users[username] = data
    unified_file.write_text(json.dumps(list(users.values()), indent=4, ensure_ascii=False), encoding="utf-8")

    try:
        rows_by_url = {
            str(row["URL"]): row
            for row in pd.read_excel(excel_file).to_dict("records")
            if isinstance(row, dict) and row.get("URL")
        }
    except Exception:
        rows_by_url = {}

    for post in data["posts"]:
        rows_by_url[post["url"]] = {
            "Username": username,
            "URL": post["url"],
            "Likes": post["likes"],
            "Comments": post["comments"],
            "Date": post["date"],
            "Hashtags": ", ".join(post["hashtags"]),
            "Scraping Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        }

    pd.DataFrame(list(rows_by_url.values())).to_excel(excel_file, index=False)

    if PUBLIC_DIR.exists():
        for file in (unified_file, excel_file):
            shutil.copy(file, PUBLIC_DIR / file.name)

    print(f"JSON: {unified_file}")
    print(f"Excel: {excel_file}")


def scrape_instagram(username):
    # Flujo principal: abre el perfil, visita cada post y guarda el resultado.
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()
        page.goto(f"{BASE_URL}/{username}/", wait_until="domcontentloaded")

        try:
            page.wait_for_selector("header", timeout=15000)
        except Exception:
            print("Failed to load page")
            browser.close()
            return

        print("Page loaded successfully")
        header = page.locator("header").inner_text().split("\n")
        post_urls = collect_post_urls(page)
        print(f"Posts found: {len(post_urls)}")

        posts = []
        for index, post_url in enumerate(post_urls, start=1):
            try:
                print(f"Opening post {index}")
                page.goto(post_url, wait_until="domcontentloaded")
                page.wait_for_selector("main", timeout=10000)
                page.wait_for_timeout(1800)

                post = extract_post(page)
                post["url"] = post_url
                posts.append(post)

                likes_text = post["likes"] if post["likes"] is not None else "No visible"
                print(f"Likes {likes_text} | Comments {post['comments']} | Date {post['date']} | Hashtags {len(post['hashtags'])}")
            except Exception as error:
                print(f"Error in post {index}: {str(error)[:80]}")

        save_data(
            username,
            {
                "username": username,
                "name": header[1] if len(header) > 1 else "",
                "posts_count": header[2].split(" ")[0] if len(header) > 2 else "0",
                "followers": header[3].split(" ")[0] if len(header) > 3 else "0",
                "bio": header[5] if len(header) > 5 else "",
                "scraped_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "posts": posts,
            },
        )

        print("\nScraping completed")
        browser.close()


if __name__ == "__main__":
    username = input("Enter Instagram username: ").strip()
    if username:
        scrape_instagram(username)
