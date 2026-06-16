import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_all_documents


async def generate_as_pdf_binder_all_document():
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
            button_selector="#GenerateBinderLink1 > img",
            download_path="downloads",
            custom_name="Ganesha_pdf"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        await browser.close()
        return save_path


if __name__ == "__main__":
    result = asyncio.run(generate_as_pdf_binder_all_document())
    if result:
        print(f"✅ Result: {result}")
