import asyncio
import os

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_save_ciq_report_tearsheet():
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
        print("✅ Dashboard page loaded.")

        # Search entity
        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill(
            "#SearchTopBar",
            "Bank of America Corporation"
        )
        await page.wait_for_timeout(12000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        # Open first search result
        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to entity page.")

        # Wait for entity page
        await page.wait_for_selector(
            "#ll_7_48_406",
            timeout=15000
        )
        print("✅ Entity page loaded.")

        # Verify tearsheet page
        tearsheet_page = page.locator("#ll_7_48_406")

        if not await tearsheet_page.is_visible():
            print("❌ Tearsheets page is not visible.")
            return None

        print("✅ Tearsheets page is visible.")

        # Locate report button
        report_button = page.locator(
            "img[title='Company Report in Word']"
        )

        if not await report_button.is_visible():
            print("❌ 'CIQ Report' button is not visible.")
            return None

        print("✅ 'CIQ Report' button is visible.")

        await handle_cookie_popup(page)
        await page.wait_for_timeout(2000)

        print("📥 Generating report and waiting for download...")


        # Capture download event
        """async with page.expect_download(timeout=120000) as download_info:
            await report_button.click()
            await page.wait_for_timeout(60000)"""
        async with page.expect_download(timeout=180000) as download_info:
            await report_button.dispatch_event("click")

        #download = await download_info.value
        download = await download_info.value

        # Create downloads folder
        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

        # Save file
        filename = download.suggested_filename

        if not filename:
            filename = "CIQ_Report.rtf"

        save_path = os.path.join(save_folder, filename)

        await download.save_as(save_path)

        print(f"✅ Report downloaded successfully.")
        print(f"📂 Saved to: {save_path}")

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
    asyncio.run(generate_save_ciq_report_tearsheet())
