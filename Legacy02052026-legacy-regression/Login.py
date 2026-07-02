"""import os
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

"""
import os
import asyncio
from playwright.async_api import async_playwright


async def login():
    """
    Launch browser, login to the application,
    and return playwright, browser, page.
    """

    # =========================
    # READ FROM GITHUB SECRETS ONLY
    # =========================
    url = os.getenv("APP_URL")
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    # Safety check
    if not url or not username or not password:
        raise Exception(
            "Missing required environment variables: "
            "APP_URL / APP_USERNAME / APP_PASSWORD"
        )

    playwright = await async_playwright().start()

    headless_env = os.getenv("PLAYWRIGHT_HEADLESS", "1")
    headless = False if headless_env == "0" else True

    browser = await playwright.chromium.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-gpu"
        ]
    )

    context = await browser.new_context()

    page = await context.new_page()

    # =========================
    # LOGIN
    # =========================

    await page.goto(
        url,
        wait_until="domcontentloaded"
    )

    await page.locator(
        "//*[@id='input28']"
    ).fill(username)

    await page.locator(
        "//*[@id='form20']/div[2]/input"
    ).click()

    await page.locator(
        "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[1]/div[4]/div/div[2]/span/input"
    ).fill(password)

    await page.locator(
        "xpath=/html/body/div[1]/div[3]/div[2]/div[1]/div/main/div[2]/div/div/div[2]/form/div[2]/input"
    ).click()

    await page.wait_for_load_state("networkidle")

    print("✅ Login successful!")

    return playwright, browser, page


async def main():
    """
    Allows this file to be run directly.
    """

    playwright = None
    browser = None

    try:
        playwright, browser, page = await login()

        print("✅ Login script completed successfully.")

        # Keep browser open for a few seconds if running headed
        if os.getenv("PLAYWRIGHT_HEADLESS", "1") == "0":
            await page.wait_for_timeout(5000)

    finally:
        if browser:
            await browser.close()

        if playwright:
            await playwright.stop()


if __name__ == "__main__":
    asyncio.run(main())
