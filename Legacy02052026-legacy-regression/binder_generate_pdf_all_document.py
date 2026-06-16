import asyncio
import os
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download


async def generate_as_pdf_binder_all_document():
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
        binder_dropdown="#layout_folder_frb-90308440 > table > tbody > tr > td.fldrMenu"
        await page.click(binder_dropdown)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder_dropdown successfully")

        # Call download manager
        save_path = await manage_download(
            page,
            button_selector="#rc_genPDF",  # Excel/PDF download button
            download_path="downloads",  
            file_name="BinderReport_dontknowWhatfor.pdf"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            return save_path
        else:
            print("❌ Download failed.")
            return None

        await browser.close()


if __name__ == "__main__":
    asyncio.run(generate_as_pdf_binder_all_document())
