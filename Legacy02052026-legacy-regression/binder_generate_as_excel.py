# this script is about download all excel files within folders 
import asyncio
import os
from playwright.async_api import async_playwright   
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download


async def generate_as_excel_binder_document():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        documentsAndReports = "https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
        await page.goto(
            documentsAndReports,
            timeout=60000,
            wait_until="domcontentloaded"
        )
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel", timeout=30000)
        print(" ✅ redirected to Documents and Reports successfully")

        await page.wait_for_selector("#folderTreeScroller > div > div:nth-child(2) > div:nth-child(2)")
        binder = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder successfully")

        # Example usage: works for PDF, Excel, Word, etc.
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink3 > img",  # Example: download button
            download_path=r"downloads",
            custom_name="Ganesha_excel"   # Extension will be auto-added
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            await browser.close()
            return save_path
        else:
            print("❌ Download failed.")
            await browser.close()
            return None

        await browser.close()


if __name__ == "__main__":
    asyncio.run(generate_as_excel_binder_document())

"""
import asyncio
import os
from pathlib import Path

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_all_documents


async def generate_as_excel_binder_all_document():

    playwright = None
    browser = None
    page = None

    try:

        # login() already starts playwright/browser
        playwright, browser, page = await login()

        print("✅ Login successful.")

        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        # Use shared navigation function
        if not await navigate_to_binder(page):
            await browser.close()
            return None

        # Use shared setup function
        if not await setup_download_all_documents(page):
            await browser.close()
            return None

        # Download Binder using shared function with new error handling
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink3 > img",
            download_path=r"downloads",
            custom_name="Ganesha_excel"
        )

        if save_path:

            print(f"🎉 Download complete: {save_path}")

            return save_path

        else:

            print("❌ Download failed.")

            return None

    except Exception as e:

        print(f"❌ Script failed: {e}")

        return None

    finally:

        print("🔒 Cleaning up resources...")

        try:
            if page:
                await page.close()
        except Exception as e:
            print(f"⚠ Page close error: {e}")

        try:
            if browser:
                await browser.close()
        except Exception as e:
            print(f"⚠ Browser close error: {e}")

        try:
            if playwright:
                await playwright.stop()
        except Exception as e:
            print(f"⚠ Playwright stop error: {e}")

        # Helps cleanup subprocesses on Windows
        await asyncio.sleep(2)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_excel_binder_all_document()
    )

    if result:

        print(f"✅ Final Result: {result}")
#####
import asyncio
import os
from pathlib import Path

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def manage_download(
    page,
    button_selector: str,
    download_path: str = "downloads",
    custom_name: str = None,
    timeout: int = 300000
):
    """"""
    Handles Binder download with:
    - popup handling
    - BinderWaitingIndicator handling
    - automatic extension detection
    - actual file download saving
    """"""

    os.makedirs(download_path, exist_ok=True)

    popup = None

    try:

        print(f"📥 Clicking download button: {button_selector}")

        # Wait for popup tab
        try:

            async with page.context.expect_page(timeout=20000) as popup_info:

                await page.click(button_selector)

            popup = await popup_info.value

            print("🪟 Popup detected.")

        except Exception:

            print("ℹ️ No popup detected. Using current page.")

            popup = page

        # Wait for popup page load
        await popup.wait_for_load_state("domcontentloaded")

        print(f"🌐 Current URL: {popup.url}")

        # Wait while binder is generating
        start_time = asyncio.get_event_loop().time()

        while "BinderWaitingIndicator.aspx" in popup.url:

            elapsed = asyncio.get_event_loop().time() - start_time

            if elapsed > timeout / 1000:

                print("❌ Conversion timeout.")

                return None

            print("⌛ Binder generation in progress...")

            await popup.wait_for_timeout(5000)

            try:
                await popup.reload(timeout=60000)
            except:
                pass

        print("✅ Binder generation completed.")

        # Wait for actual file download
        async with popup.expect_download(timeout=timeout) as download_info:

            try:
                # Some pages need manual click
                await popup.click("text=Download", timeout=5000)
            except:
                # Many pages auto-download
                await popup.wait_for_timeout(5000)

        download = await download_info.value

        # Actual filename from server
        suggested_name = download.suggested_filename

        ext = Path(suggested_name).suffix

        # Preserve actual extension
        if custom_name:

            filename = f"{Path(custom_name).stem}{ext}"

        else:

            filename = suggested_name

        save_path = os.path.join(download_path, filename)

        await download.save_as(save_path)

        print(f"✅ Download saved: {save_path}")

        return save_path

    except Exception as e:

        print(f"❌ Download failed for selector {button_selector}: {e}")

        return None


async def generate_as_excel_binder_all_document():

    playwright = None
    browser = None
    page = None

    try:

        # login() already starts playwright/browser
        playwright, browser, page = await login()

        print("✅ Login successful.")

        await handle_cookie_popup(page)

        await page.wait_for_timeout(10000)

        # Navigate to Reports Center
        documentsAndReports = (
            "https://www.capitaliq.com/"
            "CIQDotNet/DocManagement/ReportsCenter.aspx"
        )

        await page.goto(
            documentsAndReports,
            wait_until="domcontentloaded",
            timeout=120000
        )

        await page.wait_for_timeout(10000)

        await page.wait_for_selector(
            "#_pageHeader_PageHeaderLabel",
            timeout=120000
        )

        print("✅ Redirected to Documents and Reports successfully")

        # Open binder
        binder = (
            "#layout_folder_frb-90308440 > "
            "table > tbody > tr > td.fldrName"
        )

        await page.wait_for_selector(
            binder,
            timeout=120000
        )

        await page.click(binder)

        await page.wait_for_timeout(5000)

        print("✅ Clicked on binder successfully")

        # Download Binder
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink3 > img",
            download_path=r"downloads",
            custom_name="Ganesha_excel"
        )

        if save_path:

            print(f"🎉 Download complete: {save_path}")

            return save_path

        else:

            print("❌ Download failed.")

            return None

    except Exception as e:

        print(f"❌ Script failed: {e}")

        return None

    finally:

        print("🔒 Cleaning up resources...")

        try:
            if page:
                await page.close()
        except Exception as e:
            print(f"⚠ Page close error: {e}")

        try:
            if browser:
                await browser.close()
        except Exception as e:
            print(f"⚠ Browser close error: {e}")

        try:
            if playwright:
                await playwright.stop()
        except Exception as e:
            print(f"⚠ Playwright stop error: {e}")

        # Helps cleanup subprocesses on Windows
        await asyncio.sleep(2)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_excel_binder_all_document()
    )

    if result:

        print(f"✅ Final Result: {result}")
"""