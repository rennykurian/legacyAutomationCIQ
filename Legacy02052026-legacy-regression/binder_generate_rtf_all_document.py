import asyncio
import os
import sys

from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import (
    navigate_to_binder,
    setup_download_all_documents
)

# Windows asyncio stability fix
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )


async def generate_as_rtf_binder_all_document():

    playwright = None
    browser = None

    try:

        # --------------------------------
        # LOGIN
        # --------------------------------
        playwright, browser, page = await login()

        print("✅ Login successful.")

        # --------------------------------
        # DEBUG EVENTS
        # --------------------------------
        page.on(
            "popup",
            lambda p: print("🪟 POPUP DETECTED")
        )

        page.on(
            "download",
            lambda d: print(
                f"📥 DOWNLOAD EVENT: "
                f"{d.suggested_filename}"
            )
        )

        page.on(
            "response",
            lambda r: print(
                f"🌐 RESPONSE: "
                f"{r.status} {r.url}"
            )
        )

        # --------------------------------
        # HANDLE COOKIE
        # --------------------------------
        await handle_cookie_popup(page)

        await page.wait_for_timeout(5000)

        # --------------------------------
        # NAVIGATE TO BINDER
        # --------------------------------
        if not await navigate_to_binder(page):

            print("❌ Failed to navigate to binder.")

            return None

        # --------------------------------
        # OPEN DROPDOWN
        # --------------------------------
        if not await setup_download_all_documents(page):

            print("❌ Failed to open dropdown.")

            return None

        # --------------------------------
        # RTF SELECTOR
        # --------------------------------
        selector = "#rc_genRTF"

        await page.wait_for_selector(
            selector,
            state="visible",
            timeout=10000
        )

        print("✅ RTF option visible.")

        # --------------------------------
        # CLICK + EXPECT POPUP
        # --------------------------------
        print("⏳ Waiting for popup/download page...")

        async with page.context.expect_page(
            timeout=120000
        ) as popup_info:

            await page.click(selector)

        popup = await popup_info.value

        print("✅ Popup page opened.")

        # --------------------------------
        # WAIT FOR POPUP LOAD
        # --------------------------------
        await popup.wait_for_load_state(
            "networkidle"
        )

        await popup.wait_for_timeout(10000)

        print(f"🌐 Popup URL: {popup.url}")

        # --------------------------------
        # CHECK FOR DOWNLOAD EVENT
        # --------------------------------
        try:

            async with popup.expect_download(
                timeout=30000
            ) as download_info:

                await popup.wait_for_timeout(5000)

            download = await download_info.value

            print(
                "✅ Download event captured."
            )

            # --------------------------------
            # SAVE FILE
            # --------------------------------
            download_folder = os.path.abspath(
                "downloads"
            )

            os.makedirs(
                download_folder,
                exist_ok=True
            )

            save_path = os.path.join(
                download_folder,
                "BinderReportword.rtf"
            )

            await download.save_as(save_path)

            print(
                f"🎉 Download complete: "
                f"{save_path}"
            )

            return save_path

        except Exception as download_error:

            print(
                f"❌ No Playwright download event: "
                f"{download_error}"
            )

            print(
                "ℹ️ CIQ may be using direct "
                "browser download or inline file."
            )

            print(
                "🌐 Final popup URL:",
                popup.url
            )

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


if __name__ == "__main__":

    result = asyncio.run(
        generate_as_rtf_binder_all_document()
    )

    if result:

        print(f"✅ Result: {result}")

    else:

        print("❌ No file downloaded.")