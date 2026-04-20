from playwright.sync_api import sync_playwright
import json

def scrape_instagram(usuario):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()

        url = f"https://www.instagram.com/{usuario}/"
        page.goto(url)

        # Esperar que cargue la página
        page.wait_for_selector("header", timeout=15000)

        print("✅ Página cargada")

        # Obtener TODO el header (más seguro)
        header_text = page.locator("header").inner_text()

        print("HEADER COMPLETO:")
        print(header_text)

        # Scroll para asegurar carga de posts
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

        # Buscar links de posts
        links = page.locator("a[href*='/p/']")
        count = links.count()

        print(f"Posts encontrados: {count}")

        posts = []
        for i in range(min(count, 10)):
            link = links.nth(i).get_attribute("href")
            if link:
                full_link = "https://instagram.com" + link
                print("Post:", full_link)
                posts.append(full_link)

        data = {
            "usuario": usuario,
            "info": header_text,
            "posts": posts
        }

        with open("datos.json", "w") as f:
            json.dump(data, f, indent=4)

        browser.close()

scrape_instagram("nasa")