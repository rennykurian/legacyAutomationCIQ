import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_all_documents


async def generate_as_word_binder_all_document():
    async with async_playwright():
        playwright, browser, page = await login()
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

        # Use shared download function
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink2 > img",
            download_path=r"downloads",
            custom_name="Ganesha_word"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        await browser.close()
        return save_path


if __name__ == "__main__":
    result = asyncio.run(generate_as_word_binder_all_document())
    if result:
        print(f"✅ Result: {result}")
"""
import asyncio

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import (
    manage_download,
    navigate_to_binder,
    setup_download_all_documents
)


async def generate_as_word_binder_all_document():

    playwright = None
    browser = None

    try:

        # login() already starts playwright/browser
        playwright, browser, page = await login()

        await handle_cookie_popup(page)

        await page.wait_for_timeout(10000)

        # Navigate to Binder
        if not await navigate_to_binder(page):

            print("❌ Failed to navigate to binder.")

            return None

        # Setup download menu
        if not await setup_download_all_documents(page):

            print("❌ Failed to setup download menu.")

            return None

        print("📥 Starting Word Binder download...")

        # Download Word Binder
        save_path = await manage_download(
            page,
            button_selector="#GenerateBinderLink2 > img",
            download_path=r"downloads",
            custom_name="Ganesha_word"
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
            if browser:
                await browser.close()
        except Exception as e:
            print(f"⚠ Browser close error: {e}")

        try:
            if playwright:
                await playwright.stop()
        except Exception as e:
            print(f"⚠ Playwright stop error: {e}")

        # Helps Windows cleanup asyncio subprocesses
        await asyncio.sleep(2)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_word_binder_all_document()
    )

    if result:

        print(f"✅ Result: {result}")
"""