import asyncio
import os

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def download_financials_excel_tearsheet_allFinancials():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        # Login
        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        # Wait for dashboard
        await page.wait_for_selector(
            "#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader",
            timeout=10000
        )
        print("✅ Dashboard loaded.")

        # Search entity
        await page.click("#SearchTopBar")
        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        # Open first result
        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Entity page opened.")

        # Wait for entity page
        await page.wait_for_selector("#ll_7_48_406", timeout=15000)
        print("✅ Entity loaded.")

        # ----------------------------
        # CLICK FINANCIALS EXCEL
        # ----------------------------
        excel_btn = page.locator("#_pageHeader__excelReport")

        await excel_btn.wait_for(state="visible", timeout=10000)

        print("📥 Downloading Financials Excel...")

        async with page.expect_download(timeout=120000) as download_info:
            await excel_btn.click()

        download = await download_info.value

        # Save file with original name
        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

        file_name = download.suggested_filename or "Financials.xlsx"
        save_path = os.path.join(save_folder, file_name)

        await download.save_as(save_path)

        print(f"🎉 Download successful: {save_path}")

        return save_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        print("🔒 Closing browser...")
        if browser:
            try:
                await browser.close()
            except Exception:
                pass
        if playwright:
            try:
                await playwright.stop()
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(download_financials_excel_tearsheet_allFinancials())