import os
from playwright.sync_api import sync_playwright


def main():
    # =========================
    # READ FROM GITHUB SECRETS ONLY
    # =========================
    url = os.getenv("APP_URL")
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    # Safety check (fail fast if secrets missing)
    if not url or not username or not password:
        raise Exception("Missing required environment variables: APP_URL / APP_USERNAME / APP_PASSWORD")

    with sync_playwright() as p:
        # Launch browser (UNCHANGED as requested)
        headless_env = os.getenv("PLAYWRIGHT_HEADLESS", "1")
        headless = False if headless_env == "0" else True

        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
        )

        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        page.goto(url, wait_until="domcontentloaded")

        # =========================
        # LOGIN FLOW
        # =========================
        page.locator("//*[@id='input28']").fill(username)

        page.locator("//*[@id='form20']/div[2]/input").click()

        page.locator(
            "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input"
        ).fill(password)

        page.locator(
            "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[2]/input"
        ).click()

        # Wait for page load
        page.wait_for_load_state("networkidle")

        print("Login successful!")

        browser.close()


if __name__ == "__main__":
    main()
