"""import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_from_options


async def generate_as_word_binder_options():
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
            button_selector="#layout_optionsButton_generateRTFLink_0",
            download_path="downloads",
            file_name="fromoptionword.rtf"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            return save_path
        else:
            print("❌ Download failed.")
            return None

        await browser.close()


if __name__ == "__main__":
    result = asyncio.run(generate_as_word_binder_options())
    if result:
        print(f"✅ Result: {result}")
"""
#22052026
import asyncio
import sys

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

from binder_common import (
    manage_download,
    navigate_to_binder,
    setup_download_from_options
)

# Windows asyncio stability
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )


async def generate_as_word_binder_options():

    playwright = None
    browser = None
    page = None

    try:

        # LOGIN
        playwright, browser, page = await login()

        print("✅ Login successful.")

        await handle_cookie_popup(page)

        await page.wait_for_timeout(5000)

        # NAVIGATE TO BINDER
        success = await navigate_to_binder(page)

        if not success:

            print("❌ Failed to navigate to binder.")

            return None

        # SETUP DOWNLOAD OPTIONS
        success = await setup_download_from_options(page)

        if not success:

            print(
                "❌ Failed to setup "
                "download options."
            )

            return None

        print("📥 Starting Word download from options...")

        selector_candidates = [
            "#layout_optionsButton_generateWordLink_txt_0",
            "#layout_optionsButton_generateWordLink_0",
            "#layout_optionsButton_generateWordLink",
            "[id*='generateWordLink']",
            "[id*='generateWord']",
            "[id*='generateRTFLink']",
            "text=Generate Word",
            "text=Word Document",
            "text=Download Word",
            "text=Word",
            "button:has-text(\"Word\")",
            "a:has-text(\"Word\")",
            "span:has-text(\"Word\")",
        ]

        button_selector = None
        for candidate in selector_candidates:
            try:
                await page.wait_for_selector(candidate, timeout=5000)
                button_selector = candidate
                print(f"✅ Found button selector: {candidate}")
                break
            except Exception:
                continue

        if not button_selector:
            # Additional fallback: inspect page for Word link-like IDs and text nodes.
            word_candidates = await page.evaluate(
                "() => Array.from(document.querySelectorAll('[id*=\\\"WordLink\\\"], [id*=\\\"Word\\\"], [id*=\\\"RTFLink\\\"]')).map(e => ({id: e.id, className: e.className, text: e.textContent && e.textContent.trim().slice(0, 80)})).slice(0, 20)"
            )
            text_candidates = await page.evaluate(
                "() => Array.from(document.querySelectorAll('body *')).filter(e => e.textContent && e.textContent.includes('Word')).map(e => ({tag: e.tagName, id: e.id, className: e.className, text: e.textContent.trim().slice(0, 80)})).slice(0, 20)"
            )
            print(f"🔍 Word-like elements found by ID pattern: {word_candidates}")
            print(f"🔍 Word-like text nodes found: {text_candidates}")
            print("❌ Could not locate Word download button after options.")
            return None

        save_path = await manage_download(
            page=page,
            button_selector=button_selector,
            download_path="downloads",
            file_name="Report_Word.docx",
            source="options"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            return save_path

        print("❌ Download failed.")
        return None

    except Exception as e:

        print(f"❌ Error occurred: {e}")

        return None

    finally:

        print("🔒 Closing browser...")

        try:
            if page:
                await page.close()
        except:
            pass

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

        await asyncio.sleep(2)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_word_binder_options()
    )

    if result:

        print(f"✅ Result: {result}")

    else:

        print("❌ No file downloaded.")