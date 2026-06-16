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


async def generate_as_word_binder_options_alt():

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

        save_path = await manage_download(
            page=page,
            button_selector="#layout_optionsButton_generateWordLink_txt_0",
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

        await asyncio.sleep(1)


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_word_binder_options_alt()
    )

    if result:

        print(f"✅ Result: {result}")

    else:

        print("❌ No file downloaded.")
