import os
from playwright.async_api import async_playwright

USERNAME = "test_ciqmi@spglobal.com"
PASSWORD = "Monsoon@123"
URL = "https://www.capitaliq.com"


async def login():
    """Start Playwright and log into CapitalIQ.

    Defaults to headless mode. Set `PLAYWRIGHT_HEADLESS=0` to run headed locally.
    Returns: (playwright, browser, page)
    """

    playwright = await async_playwright().start()

    headless_env = os.getenv("PLAYWRIGHT_HEADLESS", "1")
    headless = False if headless_env == "0" else True
    slow_mo = 0 if headless else 50

    browser = await playwright.chromium.launch(
        headless=headless,
        slow_mo=slow_mo,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-gpu"],
    )

    # Enable downloads in context
    context = await browser.new_context(accept_downloads=True)
    page = await context.new_page()

    # Perform login
    await page.goto(URL)
    await page.wait_for_selector("#input28", timeout=30000)
    await page.fill("#input28", USERNAME)
    await page.click('#form20 input[type="submit"]')

    await page.wait_for_selector("#input60", timeout=30000)
    await page.fill("#input60", PASSWORD)
    await page.click('#form52 input[type="submit"]')

    await page.wait_for_selector("#ctl05_ciqImage", timeout=60000)
    print("✅ Login successful")

    return playwright, browser, page