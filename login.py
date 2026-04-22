from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.instagram.com/")

    print(" Please log in manually in the browser")
    input("Press ENTER after logging in...")

    context.storage_state(path="cookies.json")

    print(" Cookies saved successfully")
    browser.close()