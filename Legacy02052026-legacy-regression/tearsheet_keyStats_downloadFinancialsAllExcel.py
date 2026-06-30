import asyncio
import os

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_save_excel_report_tearsheetKeyStats_downloadFinancials():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        # Login
        playwright, browser, page = await login()

        await handle_cookie_popup(page)

        # Dashboard
        await page.wait_for_selector(
            "#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader",
            timeout=10000
        )
        print("✅ Dashboard page loaded.")

        # Search entity
        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill(
            "#SearchTopBar",
            "Bank of America Corporation"
        )
        await page.wait_for_timeout(3000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        # Open first result
        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to entity page.")

        # Wait for entity page
        await page.wait_for_selector("#ll_7_48_406", timeout=15000)
        print("✅ Entity page loaded.")

        tearsheet_page = page.locator("#ll_7_48_406")

        if not await tearsheet_page.is_visible():
            print("❌ Tearsheets page is not visible.")
            return None

        print("✅ Entity page verified.")

        # ----------------------------
        # STEP: KEY STATS PAGE
        # ----------------------------
        key_stats_link = page.locator("#ll_7_123_2083")

        await key_stats_link.wait_for(state="visible", timeout=10000)
        await key_stats_link.click()

        print("✅ Key Stats page opened.")

        # ✅ FIX: Proper wait added (IMPORTANT)
        await page.wait_for_selector(
            "#_pageHeader__singleTabReport",
            timeout=15000
        )

        print("📄 Key Stats fully loaded.")

        # ----------------------------
        # DOWNLOAD
        #<img title="Download Financials to Excel" src="https://www.capitaliq.com/CIQDOTNET/images/BinderToolbar/ico_reportImg_Sprite.gif?urwvid=3774410752" alt="">
        # ----------------------------
        download_link = page.locator("#_pageHeader__excelReport")
        

        await download_link.wait_for(state="visible", timeout=10000)
       
        print("📥 Starting Excel download...")

        async with page.expect_download(timeout=120000) as download_info:
            await download_link.click(no_wait_after=True)
            

        download = await download_info.value

        # Save file with ORIGINAL filename
        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

        file_name = download.suggested_filename or "KeyStats.xlsx"
        save_path = os.path.join(save_folder, file_name)

        await download.save_as(save_path)

        print(f"🎉 Excel downloaded successfully: {save_path}")

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
    asyncio.run(generate_save_excel_report_tearsheetKeyStats_downloadFinancials())
