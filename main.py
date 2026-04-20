from playwright.sync_api import sync_playwright
import json

def scrape_instagram(username):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state="cookies.json")
        page = context.new_page()

        url = f"https://www.instagram.com/{username}/"
        page.goto(url)

        # Wait for page to load
        page.wait_for_selector("header", timeout=15000)

        print("✅ Page loaded successfully")

        # Get full header info
        header_text = page.locator("header").inner_text()

        print("📄 FULL HEADER:")
        print(header_text)

        # Scroll to load posts
        page.mouse.wheel(0, 3000)
        page.wait_for_timeout(3000)

        # Get post links
        links = page.locator("a[href*='/p/']")
        count = links.count()

        print(f"📌 Posts found: {count}")

        posts = []
        for i in range(min(count, 10)):
            link = links.nth(i).get_attribute("href")
            if link:
                full_link = "https://instagram.com" + link
                print("🔗 Post:", full_link)
                posts.append(full_link)

        data = {
            "username": username,
            "profile_info": header_text,
            "posts": posts
        }

        with open("datos.json", "w") as f:
            json.dump(data, f, indent=4)

        browser.close()


scrape_instagram("nasa")