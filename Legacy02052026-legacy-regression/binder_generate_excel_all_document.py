# Generate Excel Binder Report (All Documents)
import asyncio
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_all_documents


async def generate_as_excel_binder_all_document():
    playwright = None
    browser = None
    page = None

    try:
        # Login
        playwright, browser, page = await login()
        print("✅ Login successful.")

        # Handle cookies
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        # Navigate to Binder
        if not await navigate_to_binder(page):
            print("❌ Failed to navigate to binder.")
            return None

        # Open binder dropdown
        if not await setup_download_all_documents(page):
            print("❌ Failed to setup binder dropdown.")
            return None

        print("📥 Starting Excel download...")

        # Download Excel Binder using menu item
        save_path = await manage_download(
            page=page,
            button_selector="#rc_genXLS",
            download_path="downloads",
            file_name="BinderReport.xls"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        return save_path

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

        await asyncio.sleep(1)


if __name__ == "__main__":
    result = asyncio.run(generate_as_excel_binder_all_document())
    if result:
        print(f"✅ Result: {result}")
"""
#22052026
import asyncio

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

from binder_common import (
    manage_download,
    navigate_to_binder,
    setup_download_all_documents
)


async def generate_as_excel_binder_all_document():

    playwright = None
    browser = None
    
    
    page = None

    try:

        # login() already starts playwright/browser
        playwright, browser, page = await login()

        print("✅ Login successful.")

        # Handle cookies
        await handle_cookie_popup(page)

        await page.wait_for_timeout(10000)

        # Navigate to Binder
        navigation_success = await navigate_to_binder(page)

        if not navigation_success:

            print("❌ Failed to navigate to binder.")

            return None

        # Open binder dropdown
        setup_success = await setup_download_all_documents(page)

        if not setup_success:

            print("❌ Failed to setup binder dropdown.")

            return None

        print("📥 Opening Excel menu item...")

        # IMPORTANT:
        # Wait for menu item visibility before clicking
        await page.wait_for_selector(
            "#rc_genXLS",
            state="visible",
            timeout=30000
        )

        print("✅ Excel menu item is visible.")

        # Download Excel Binder
        save_path = await manage_download(
            page=page,
            button_selector="#rc_genXLS",
            download_path="downloads",
            file_name="BinderReport.xls"
        )

        if save_path:

            print(f"🎉 Download complete: {save_path}")

        else:

            print("❌ Download failed.")

        return save_path

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

        # Helps Windows cleanup subprocesses
        await asyncio.sleep(2)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_excel_binder_all_document()
    )

    if result:

        print(f"✅ Result: {result}")
        """