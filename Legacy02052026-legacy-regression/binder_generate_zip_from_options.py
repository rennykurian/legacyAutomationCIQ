"""import asyncio
import os
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def manage_download(page, button_selector: str, download_path: str = "downloads", file_name: str = None):
    """"""
    Handles file download triggered by clicking a selector.
    Works even if a new popup tab opens (BinderWaitingIndicator.aspx).
    """"""

    os.makedirs(download_path, exist_ok=True)

    try:
        # Expect popup window when clicking download
        async with page.context.expect_page() as popup_info:
            await page.click(button_selector)

        popup = await popup_info.value
        await popup.wait_for_load_state("networkidle")

        # Now wait for actual file download in popup
        async with popup.expect_download() as download_info:
            # If popup auto-triggers download, nothing to click.
            # If a button exists in popup, you can click it here.
            await popup.wait_for_timeout(5000)

        download = await download_info.value

        # Get filename
        suggested_name = download.suggested_filename
        filename = file_name or suggested_name

        save_path = os.path.join(download_path, filename)
        await download.save_as(save_path)

        print(f"✅ Download saved: {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Download failed for selector {button_selector}: {e}")
        return None


async def generate_as_word_binder_options():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        documentsAndReports = "https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
        await page.goto(documentsAndReports)
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel")
        print(" ✅ redirected to Documents and Reports successfully")

        await page.wait_for_selector("#folderTreeScroller > div > div:nth-child(2) > div:nth-child(2)")
        binder = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder successfully")
        checkbox="#layout_documents > table.cTblListBody.docTable.ui-sortable > thead > tr > th.cbcol > input[type=checkbox]"
        await page.wait_for_selector(checkbox)
        await page.click(checkbox)
        print("checkbox selected")
        await page.wait_for_timeout(5000)
        binder_dropdown="#layout_optionsButton_MenuButton"
        await page.click(binder_dropdown)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder_dropdown successfully")

        # Call download manager
        save_path = await manage_download(
            page,
            button_selector="#layout_optionsButton_generateZipLink_txt_0",  # Excel/PDF download button
            download_path=r"D:\Legacy04082025\downloads",
            file_name="fromoptionword.zip"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(generate_as_word_binder_options())
"""
import asyncio
import os
import glob

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

from binder_common import (
    manage_download,
    navigate_to_binder,
    setup_download_from_options
)

async def generate_as_zip_binder_all_document():

    playwright = None
    browser = None
    page = None

    try:

        playwright, browser, page = await login()

        print("✅ Login successful.")

        await handle_cookie_popup(page)

        await page.wait_for_timeout(5000)

        # NAVIGATE
        if not await navigate_to_binder(page):
            return None

        # SETUP OPTIONS
        if not await setup_download_from_options(page):
            return None

        print("📥 Starting ZIP download from options...")

        # Use shared download helper
        save_path = await manage_download(
            page=page,
            button_selector="#layout_optionsButton_generateZipLink_txt_0",
            download_path="downloads",
            file_name="Report_ZIP.zip",
            source="options"
        )

        if save_path:
            print(f"🎉 ZIP Download complete: {save_path}")
            return save_path

        print("❌ ZIP download failed")
        return None

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        print("🔒 Closing browser...")
        try:
            if browser:
                await browser.close()
        except:
            pass

        try:
            if playwright:
                await playwright.stop()
        except:
            pass

        await asyncio.sleep(1)


if __name__ == "__main__":
    result = asyncio.run(generate_as_zip_binder_all_document())
    if result:
        print(f"✅ Final Result: {result}")
    else:
        print("❌ Failed")


async def generate_as_zip_binder_options():
    """Compatibility wrapper used by tests.

    The original module provides `generate_as_zip_binder_all_document`.
    Tests import `generate_as_zip_binder_options` — provide a thin
    wrapper that calls the main implementation.
    """
    return await generate_as_zip_binder_all_document()