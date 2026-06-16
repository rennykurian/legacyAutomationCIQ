import asyncio
import os
from TestLoginLegacy import login
from playwright.async_api import async_playwright


async def generate_ten_kWORD_from_tearsheet():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        playwright, browser, page = await login()

        await page.wait_for_selector(
            "#_pageHeader > div:nth-child(1) > span.cPageTitle_subHeader",
            timeout=10000
        )
        print("✅ Dashboard page loaded.")

        await page.click("#SearchTopBar")
        await page.wait_for_timeout(2000)

        await page.fill("#SearchTopBar", "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("Enter")
        await page.wait_for_timeout(5000)

        await page.click("#SR0 > td.NameCell > div > span > a")
        print("✅ Navigated to the entity page.")

        await page.wait_for_selector("#ll_7_48_406", timeout=20000)
        print("✅ Entity page loaded.")

        tearsheet_locator = page.locator("#ll_7_48_406")

        if not await tearsheet_locator.is_visible():
            print("❌ Tearsheets page is not visible.")
            return

        toolbar = page.locator("#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar")
        await toolbar.wait_for(timeout=10000)

        if await toolbar.is_visible():
            print("✅ Toolbar is visible.")
        else:
            print("❌ Toolbar is not visible.")
            return

        ten_k_button = page.locator(
            "#CompanyHeaderInfo_CompanyHeaderInfo_BinderToolbar > ul > li:nth-child(8) > a > div"
        )

        await ten_k_button.wait_for(state="visible", timeout=10000)

        # -------------------------------
        # STEP 1: OPEN 10-K POPUP
        # -------------------------------
        async with page.context.expect_page(timeout=15000) as popup_info:
            await ten_k_button.click()

        tenk_page = await popup_info.value
        await tenk_page.wait_for_load_state("domcontentloaded")

        print("✅ 10-K popup opened.")
        await tenk_page.wait_for_timeout(30000)  # wait for potential dynamic content to load

        # -------------------------------
        # STEP 2: FIND WORD BUTTON
        # -------------------------------
        print("📄 Searching for WORD button (#wordImg)...")

        word_button = tenk_page.locator("#wordImg")

        if await word_button.count() == 0:
            print("⚠️ Not found in popup, checking frames...")

            for frame in tenk_page.frames:
                candidate = frame.locator("#wordImg")
                if await candidate.count() > 0:
                    word_button = candidate
                    print(f"✅ Found in frame: {frame.url}")
                    break

        if await word_button.count() == 0:
            print("❌ WORD button not found anywhere.")
            return

        await word_button.wait_for(state="visible", timeout=15000)

        # -------------------------------
        # STEP 3: DOWNLOAD (ORIGINAL NAME)
        # -------------------------------
        print("📥 Starting download...")

        async with tenk_page.expect_download(timeout=120000) as download_info:
            await word_button.click()

        download = await download_info.value

        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

        # ✅ ORIGINAL FILE NAME + EXTENSION
        file_name = download.suggested_filename

        if not file_name:
            file_name = "10K_Report"

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
    asyncio.run(generate_ten_kWORD_from_tearsheet())