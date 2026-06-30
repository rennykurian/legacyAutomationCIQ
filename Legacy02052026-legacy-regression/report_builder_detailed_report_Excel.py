#26062026
import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

async def generate_and_save_detailed_report_excel():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        await page.goto(
            "https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx",
            wait_until="networkidle"
        )
        print("✅ Dashboard loaded.")

        await page.wait_for_selector("#tmbButton1", timeout=30000)
        await page.hover("#tmbButton1")
        print("✅ Hovered over My Capital IQ")

        await page.wait_for_timeout(3000)

        flyout = page.locator("#__tmbFlyout1")
        await flyout.wait_for(state="visible", timeout=30000)

        report_builder = flyout.locator("a[href*='ReportsBuilder']")

        count = await report_builder.count()
        print(f"Found {count} ReportBuilder link(s)")
        for i in range(count):
            try:
                print(
                    i,
                    await report_builder.nth(i).inner_text(),
                    await report_builder.nth(i).get_attribute("href")
                )
            except Exception:
                pass

        await report_builder.first.click(force=True)
        await page.wait_for_timeout(3000)

        print("Current URL:", page.url)
        await page.screenshot(path="debug_after_report_builder_click.png", full_page=True)

        await page.wait_for_selector(
            "#_rptOpts__rptOptsDS__optsDs__optsTog__esLink",
            timeout=60000
        )
        print("✅ Report Builder loaded.")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")
        print("✅ Entity selection modal opened.")
        await page.screenshot(path="debug_entity_modal.png", full_page=True)

        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"
        await page.wait_for_selector(search_box, timeout=30000)
        await page.fill(search_box, "Tejas Networks Limited")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")

        print("✅ Entity selection saved.")

        await page.wait_for_load_state("networkidle")

        await page.wait_for_timeout(2000)
        await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label")

        async with page.context.expect_page(timeout=30000) as popup_info:
            await page.click("#RepBldrTemplateImg6")
            print("generate report clicked")

        """ report_page = await popup_info.value
        await report_page.wait_for_load_state("domcontentloaded")

        download_locator = report_page.locator("text=Download")

        timeout_ms = 600000
        poll = 5000
        elapsed = 0

        while elapsed < timeout_ms:
            if await download_locator.count() > 0:
                break
            await report_page.wait_for_timeout(poll)
            elapsed += poll

        async with report_page.expect_download(timeout=180000) as d:
            await download_locator.first.click()"""
        report_page = page
        try:
            async with page.context.expect_page(timeout=18000) as popup:
                pass
            report_page = await popup.value
            await report_page.wait_for_load_state("domcontentloaded")
        except Exception:
            await page.wait_for_selector("div.wrapper", timeout=60000)

        dl_btn = report_page.get_by_role("link", name="Download").or_(
            report_page.get_by_role("button", name="Download")
        ).first

        await dl_btn.wait_for(state="visible", timeout=70000)

        async with report_page.expect_download(timeout=120000) as d:
            await dl_btn.click()    

        download = await d.value

        os.makedirs("downloads", exist_ok=True)
        save_path=os.path.join("downloads", download.suggested_filename)
        #path = "downloads/Detailed_Report_Excel.xlsx"
        await download.save_as(save_path)
        print(f"✅ saved: {save_path}")

        #print("✅ Saved:", path)
        return save_path
    
    except Exception as e:
        print("❌ Error:", e)
        try:
            print("Current URL:", page.url)
            await page.screenshot(path="FAILED_TEST.png", full_page=True)
            print("📷 Screenshot saved.")
        except Exception:
            pass
        return None

    finally:
        print("🔒 Closing browser...")
        if browser:
            try:
                await browser.close()
            except Exception:
                pass
        if playwright:
            try:
                await playwright.stop()
            except Exception:
                pass

    """except Exception as e:
        print("❌ Error:", e)
        return None

    finally:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()"""


if __name__ == "__main__":
    asyncio.run(generate_and_save_detailed_report_excel())
"""import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_and_save_detailed_report_excel():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"  # run headed so output is visible
        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        # Open dashboard
        await page.goto("https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx", wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)
        print("✅ Dashboard loaded.")

        # Hover My Capital IQ (#tmbButton1) and click Report Builder
        await page.wait_for_selector('#tmbButton1', timeout=15000)
        await page.hover('#tmbButton1')
        print("✅ Hovered over My Capital IQ")
        await page.wait_for_timeout(1500)
        flyout = page.locator("#__tmbFlyout1")
        await flyout.wait_for(state="attached", timeout=15000)
        report_builder = flyout.locator("a[href*='ReportsBuilder']")
        await report_builder.first.click(force=True)
        await page.wait_for_load_state("load")
        print("✅ Report Builder page loaded.")

        # Open Entity Selector
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")
        print("✅ Entity selection modal opened.")

        # Search for entity
        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"
        await page.wait_for_selector(search_box, timeout=10000)
        await page.fill(search_box, "Tejas Networks Limited")
        await page.wait_for_timeout(3000)

        # Select the first result
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")
        await page.click(
            "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div")

        # Save entity selection
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")
        print("✅ Entity selection saved.")

        # Select template and trigger download
        await page.wait_for_load_state("load")
        await page.wait_for_timeout(2000)

        await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label")
        print("✅ Clicked on Capital IQ Templates.")

        await page.click("#RepBldrTemplateImg6")
        print("✅ Clicked on Detailed Report (Excel) option.")

        report_page = page
        try:
            async with page.context.expect_page(timeout=12000) as popup_info:
                pass
            report_page = await popup_info.value
            await report_page.wait_for_load_state("domcontentloaded")
            print("✅ Report popup opened.")
        except Exception:
            print("ℹ️ No popup — waiting for download wrapper on same page.")
            await page.wait_for_selector("div.wrapper", state="visible", timeout=120000)
    
        dl_btn = report_page.get_by_role("link", name="Download").or_(
            report_page.get_by_role("button", name="Download")
        ).first
        await dl_btn.wait_for(state="visible", timeout=120000)
        print("✅ Download button ready.")
        async with report_page.expect_download(timeout=120000) as download_info:
            await dl_btn.click()
        download = await download_info.value

        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, "Detailed_Report_Excel.xlsx")
        await download.save_as(save_path)
        print(f"✅ Report downloaded and saved to {save_path}")
        return save_path

    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    finally:
        print("🔒 Closing browser...")
        if browser:
            try:
                await browser.close()
            except Exception:
                pass
        if playwright:
            try:
                await playwright.stop()
            except Exception:
                pass


if __name__ == "__main__":
    asyncio.run(generate_and_save_detailed_report_excel())
"""