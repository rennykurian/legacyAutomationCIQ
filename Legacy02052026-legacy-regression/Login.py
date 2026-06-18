import os
from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        # Launch browser (UNCHANGED as you requested)
        headless_env = os.getenv("PLAYWRIGHT_HEADLESS", "1")
        headless = False if headless_env == "0" else True

        browser = p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"]
        )

        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        page.goto("https://www.stagingciq.com", wait_until="domcontentloaded")

        # =========================
        # LOGIN FLOW (UNCHANGED LOCATORS)
        # =========================

        page.locator("//*[@id='input28']").fill(
            os.getenv("APP_USERNAME", "test.user124@spglobal.com")
        )

        page.locator("//*[@id='form20']/div[2]/input").click()

        page.locator(
            "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input"
        ).fill(
            os.getenv("APP_PASSWORD", "Testuser123")
        )

        page.locator(
            "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[2]/input"
        ).click()

        # =========================
        # SAFE WAIT (REPLACES sleep)
        # =========================
        page.wait_for_load_state("networkidle")

        print("Login successful!")

        browser.close()


if __name__ == "__main__":
    main()
