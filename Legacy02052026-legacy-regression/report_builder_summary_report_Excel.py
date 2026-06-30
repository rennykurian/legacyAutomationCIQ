import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_and_save_summary_report_excel():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        # ✅ Dashboard
        await page.goto(
            "https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx",
            wait_until="domcontentloaded"
        )
        await page.wait_for_timeout(2000)
        print("✅ Dashboard loaded.")

        # ✅ Report Builder
        await page.hover('#tmbButton1')
        await page.wait_for_timeout(1500)

        flyout = page.locator("#__tmbFlyout1")
        await flyout.wait_for(state="attached")

        await flyout.locator("a[href*='ReportsBuilder']").first.click(force=True)
        await page.wait_for_load_state("load")
        print("✅ Report Builder page loaded.")

        # ✅ Entity selection
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")

        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"
        await page.fill(search_box, "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 >> nth=0")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")

        print("✅ Entity selection saved.")

        # ✅ Select Excel template
        await page.wait_for_load_state("networkidle")

        await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span >> label")
        await page.click("#RepBldrTemplateImg3")
        print("✅ Summary Report Excel clicked.")

        # ✅ HANDLE POPUP (same as PDF)
        report_page = page

        try:
            async with page.context.expect_page(timeout=15000) as popup_info:
                pass
            report_page = await popup_info.value
            await report_page.wait_for_load_state("domcontentloaded")
            print("✅ Report popup opened (Excel).")

        except Exception:
            print("ℹ️ No popup — checking iframe...")

        # ✅ WAIT FOR CONTENT
        await report_page.wait_for_timeout(5000)

        # ✅ Try iframe (Excel usually loads inside iframe)
        download_button = None

        for f in report_page.frames:
            if "report" in f.url.lower() or "excel" in f.url.lower():
                print(f"✅ Found report iframe: {f.url}")

                await f.wait_for_selector(
                    "xpath=//a[contains(text(),'Download')]",
                    state="visible",
                    timeout=60000
                )

                download_button = f.locator(
                    "xpath=//a[contains(text(),'Download')]"
                ).last
                break

        # ✅ Fallback (rare case)
        if not download_button:
            print("⚠️ Using fallback locator on report page")

            await report_page.wait_for_selector(
                "xpath=//a[contains(text(),'Download')]",
                state="visible",
                timeout=60000
            )

            download_button = report_page.locator(
                "xpath=//a[contains(text(),'Download')]"
            ).last

        print("✅ Download button found.")

        # ✅ Screenshot for debugging
        await report_page.screenshot(path="debug_excel.png", full_page=True)

        # ✅ Download file
        async with report_page.expect_download(timeout=120000) as download_info:
            await download_button.click()

        download = await download_info.value

        # ✅ Save
        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

        save_path = os.path.join(save_folder, "Summary_Report_Excel.xlsx")
        await download.save_as(save_path)

        print(f"✅ Excel report downloaded: {save_path}")

        return save_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        print("🔒 Closing browser...")
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()


if __name__ == "__main__":
    asyncio.run(generate_and_save_summary_report_excel())
