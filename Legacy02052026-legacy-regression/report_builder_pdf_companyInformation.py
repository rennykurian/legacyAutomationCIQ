import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def generate_save_pdf_report():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"  # run headed so output is visible

        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        # Open dashboard
        await page.goto(
            "https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx",
            wait_until="domcontentloaded"
        )
        await page.wait_for_timeout(2000)
        print("✅ Dashboard loaded.")

        # Hover My Capital IQ and click Report Builder
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
        await page.fill(search_box, "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        # Select first result
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

        await page.click(
            "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div"
        )

        # Save entity selection
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")

        print("✅ Entity selection saved.")

        # Wait for template section
        await page.wait_for_load_state("load")
        await page.wait_for_timeout(2000)

        # -----------------------------
        # Company Information checkbox
        # -----------------------------
        company_checkbox = page.locator(
            'input[name="_categoriesDS$Toggle$_sortList$ctl01$sect$_selectedCb"]'
        )

        if not await company_checkbox.is_checked():
            await company_checkbox.check()

        print("✅ Company Information selected")

        # -----------------------------
        # Report type radio button
        # -----------------------------
        await page.locator("img[src*='ico_doctype_pdf.gif']").first.click()
        print("✅ PDF radio (via icon) selected")


        # Wait for UI update
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        # -----------------------------
        # Generate Report
        # -----------------------------
        generate_btn = page.locator(
            "#_rptOpts__rptOptsDS__optsDs__optsTog__generateReportBtn"
        )

        await generate_btn.wait_for(state="visible", timeout=10000)
        await generate_btn.click()

        print("✅ Generate Report clicked")
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
        await dl_btn.wait_for(state="visible", timeout=60000)
        print("✅ Download button ready.")
        async with report_page.expect_download(timeout=120000) as download_info:
            await dl_btn.click()
        download = await download_info.value

        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)

# real filename from browser (includes correct extension)
        file_name = download.suggested_filename

        save_path = os.path.join(save_folder, file_name)

        await download.save_as(save_path)

        print(f"✅ Report downloaded and saved to {save_path}")

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
    asyncio.run(generate_save_pdf_report())