"""import asyncio
#from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_from_options


async def generate_as_pdf_binder_options():
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        # Use shared navigation function
        if not await navigate_to_binder(page):
            await browser.close()
            return None

        # Use shared setup function for "from options" workflow
        if not await setup_download_from_options(page):
            await browser.close()
            return None

        # Use shared download function
        save_path = await manage_download(
            page,
            button_selector="#layout_optionsButton_generatePDFLink_txt_0",
            download_path="downloads",
            file_name="fromoptionPDF.pdf"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            await browser.close()
            return save_path
        else:
            print("❌ Download failed.")
            await browser.close()
            return None


if __name__ == "__main__":
    result = asyncio.run(generate_as_pdf_binder_options())
    if result:
        print(f"✅ Result: {result}")
"""
import asyncio
import sys

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

from binder_common import (
    manage_download,
    navigate_to_binder,
    setup_download_from_options
)

# Windows asyncio stability fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )


async def generate_as_pdf_binder_options():

    playwright = None
    browser = None

    try:

        # LOGIN
        playwright, browser, page = await login()

        print("✅ Login successful.")

        # DEBUG EVENTS
        page.on(
            "download",
            lambda d: print(
                f"📥 Download started: {d.suggested_filename}"
            )
        )

        page.on(
            "popup",
            lambda p: print("🪟 Popup opened")
        )

        # HANDLE COOKIE
        await handle_cookie_popup(page)

        await page.wait_for_timeout(5000)

        # NAVIGATE TO BINDER
        if not await navigate_to_binder(page):

            print("❌ Failed to navigate to binder.")

            return None

        # SETUP DOWNLOAD OPTIONS
        if not await setup_download_from_options(page):

            print("❌ Failed to setup download options.")

            return None

        # DOWNLOAD PDF
        save_path = await manage_download(
            page=page,
            button_selector="#layout_optionsButton_generatePDFLink_txt_0",
            download_path="downloads",
            file_name="fromoptionPDF.pdf"
        )

        if save_path:

            print(f"🎉 Download complete: {save_path}")

            return save_path

        else:

            print("❌ Download failed.")

            return None

    except Exception as e:

        print(f"❌ Error occurred: {e}")

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


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_pdf_binder_options()
    )

    if result:

        print(f"✅ Result: {result}")

    else:

        print("❌ No file downloaded.")