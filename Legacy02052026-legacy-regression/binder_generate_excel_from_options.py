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


async def generate_as_excel_binder_options():

    playwright = None
    browser = None
    page = None

    try:

        # LOGIN
        playwright, browser, page = await login()

        print("✅ Login successful.")

        # DEBUG EVENTS
        page.on(
            "download",
            lambda d: print(
                f"📥 Download started: "
                f"{d.suggested_filename}"
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

        # WAIT FOR EXCEL OPTION
        await page.wait_for_selector(
            "#layout_optionsButton_generateExcelLink_txt_0",
            state="visible",
            timeout=60000
        )

        print("✅ Excel option visible")

        # IMPORTANT FOR LEGACY UI
        await page.wait_for_timeout(3000)

        # DOWNLOAD EXCEL
        save_path = await manage_download(
            page=page,
            button_selector=(
                "#layout_optionsButton_"
                "generateExcelLink_txt_0"
            ),
            download_path="downloads",
            file_name="Report_Excel.xlsx",
            source="options"
        )

        if save_path:

            print(
                f"🎉 Download complete: "
                f"{save_path}"
            )

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
        generate_as_excel_binder_options()
    )

    if result:

        print(f"✅ Final Result: {result}")

    else:

        print("❌ No file downloaded.")