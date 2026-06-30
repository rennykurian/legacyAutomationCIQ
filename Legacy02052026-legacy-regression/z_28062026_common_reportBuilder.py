import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup

"""
async def selectCompany():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "0"  # run headed so output is visible

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
        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"

        await page.wait_for_selector(search_box, timeout=30000)
        await page.fill(search_box, "Tejas Networks Limited")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

        await page.wait_for_timeout(1000)

        tree_node = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div"
        first_save = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn"
        final_save = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn"

        # Check if the tree node still exists (Scenario 1)
        if await page.locator(tree_node).count() > 0:
            print("Scenario 1: Entity not auto-selected.")

            await page.click(tree_node)
            await page.click(first_save)

        else:
            print("Scenario 2: Entity auto-selected after Enter.")

        # Both scenarios end here
        await page.click(final_save)

        print("✅ Entity selection saved.")
        
        # Wait for template section
        await page.wait_for_load_state("load")
        await page.wait_for_timeout(2000)
        return playwright, browser, page
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return playwright, browser, page
            # Wait for UI update
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        # -----------------------------
        # Generate Report
        # -----------------------------
        generate_btn = page.locator(
            "#_rptOpts__rptOptsDS__optsDs__optsTog__generateReportBtn"
        )

        await generate_btn.wait_for(state="visible", timeout=30000)
        await generate_btn.click()

        print("✅ Generate Report clicked")
        report_page = page
        try:
            async with page.context.expect_page(timeout=24000) as popup_info:
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
        async with report_page.expect_download(timeout=240000) as download_info:
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
                
"""
async def selectCompany():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "1"

        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(2000)

        await page.goto(
            "https://www.capitaliq.com/CIQDotNet/my/dashboard.aspx",
            wait_until="domcontentloaded"
        )

        await page.wait_for_timeout(2000)
        print("✅ Dashboard loaded.")

        await page.wait_for_selector("#tmbButton1", timeout=15000)
        await page.hover("#tmbButton1")
        print("✅ Hovered over My Capital IQ")

        await page.wait_for_timeout(1500)

        flyout = page.locator("#__tmbFlyout1")
        await flyout.wait_for(state="attached", timeout=15000)

        await flyout.locator("a[href*='ReportsBuilder']").first.click(force=True)

        await page.wait_for_load_state("load")
        print("✅ Report Builder page loaded.")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")
        print("✅ Entity selection modal opened.")

        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"

        await page.fill(search_box, "Tejas Networks Limited")
        await page.wait_for_timeout(3000)

        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")

        await page.wait_for_timeout(1000)

        tree_node = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div"

        if await page.locator(tree_node).count() > 0:
            print("Scenario 1")
            await page.click(tree_node)
            await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        else:
            print("Scenario 2")

        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")

        print("✅ Entity selection saved.")

        return playwright, browser, page

    except:
        if browser:
            await browser.close()
        if playwright:
            await playwright.stop()
        raise
async def selectCompanyInfo():

    playwright, browser, page = await selectCompany()
    await handle_cookie_popup(page)

    company_checkbox = page.locator(
        'input[name="_categoriesDS$Toggle$_sortList$ctl01$sect$_selectedCb"]'
    )

    if not await company_checkbox.is_checked():
        await company_checkbox.check()

    print("✅ Company Information selected")

    return playwright, browser, page
async def selectCompanyInfoFormat(page, format_type):

    if format_type == "excel":
        await page.locator(
            "img[src*='ico_doctype_excel.gif']"
        ).first.click()

    elif format_type == "pdf":
        await page.locator(
            "img[src*='ico_doctype_pdf.gif']"
        ).first.click()

    elif format_type == "word":
        await page.locator(
            "img[src*='ico_doctype_word.gif']"
        ).first.click()

    print(f"✅ {format_type} selected")
    
    

async def selectTemplate(page, template_selector):

    await page.wait_for_load_state("load")
    await page.wait_for_timeout(2000)

    await page.click(
        "#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label"
    )

    await page.click(template_selector)

    print(f"✅ Template selected: {template_selector}")

    dl_btn = report_page.get_by_role(
        "link",
        name="Download"
    ).or_(
        report_page.get_by_role(
            "button",
            name="Download"
        )
    ).first

    await dl_btn.wait_for(
        state="visible",
        timeout=60000
    )

    print("✅ Download button ready.")

    async with report_page.expect_download(
        timeout=240000
    ) as download_info:

        await dl_btn.click()

    download = await download_info.value

    save_folder = "downloads"
    os.makedirs(save_folder, exist_ok=True)

    file_name = download.suggested_filename

    save_path = os.path.join(
        save_folder,
        file_name
    )

    await download.save_as(save_path)

    print(f"✅ Report downloaded: {save_path}")

    return save_path
async def generateReport(page):
    
    await page.wait_for_load_state("networkidle")

    generate_btn = page.locator(
        "#_rptOpts__rptOptsDS__optsDs__optsTog__generateReportBtn"
    )

    await generate_btn.wait_for(
        state="visible",
        timeout=30000
    )

    existing_pages = page.context.pages[:]

    print("📝 Existing pages:", len(existing_pages))

    await generate_btn.click()

    print("✅ Generate Report clicked")
    print("⏳ Waiting for report generation...")

    # Wait a few seconds for either a popup or the existing popup to refresh
    await page.wait_for_timeout(5000)

    current_pages = page.context.pages

    # -------------------------------------------------
    # Scenario 1 - A NEW popup opened
    # -------------------------------------------------
    if len(current_pages) > len(existing_pages):

        report_page = current_pages[-1]

        await report_page.wait_for_load_state("domcontentloaded")

        print("✅ New report popup opened.")
        print(f"Returning page: {report_page.url}")
        return report_page
        #return report_page

    # -------------------------------------------------
    # Scenario 2 - Reuse existing popup
    # -------------------------------------------------
    if len(current_pages) > 1:

        report_page = current_pages[-1]

        await report_page.bring_to_front()

        print("✅ Reusing existing report popup.")
        print(f"Returning page: {report_page.url}")
        return report_page
        #return report_page

    # -------------------------------------------------
    # Scenario 3 - Same page (no popup)
    # -------------------------------------------------
    print("ℹ️ Report opened in same page.")
    report_page= page
    print(f"Returning page: {report_page.url}")
    return report_page
    #return page
async def getReportWindow(page):

    print("🔍 Looking for report window...")

    for _ in range(60):        # wait up to 60 seconds

        pages = page.context.pages

        if len(pages) > 1:

            for p in pages[1:]:

                try:
                    await p.wait_for_load_state("domcontentloaded", timeout=1000)
                except:
                    pass

                if p.is_closed():
                    continue

                await p.bring_to_front()

                print(f"✅ Report window found: {p.url}")

                return p

        await page.wait_for_timeout(1000)

    raise Exception("Report window not found.")
async def downloadReport(report_page):

    print("⏳ Waiting for report generation...")

    download_btn = report_page.get_by_role(
        "link",
        name="Download"
    ).or_(
        report_page.get_by_role(
            "button",
            name="Download"
        )
    ).first

    await download_btn.wait_for(
        state="visible",
        timeout=300000       # 5 minutes
    )

    
    print("✅ Download button visible.")

    await report_page.screenshot(path="before_download.png", full_page=True)
    print("Title:", await report_page.title())
    print("URL:", report_page.url)

    print("Download button visible:", await download_btn.is_visible())
    print("Download button enabled:", await download_btn.is_enabled())

    async with report_page.expect_download(timeout=300000) as download_info:
        print("Clicking download button...")
        await download_btn.click()
        print("Click completed.")

    async with report_page.expect_download(
        timeout=300000
    ) as download_info:

        await download_btn.click()

    download = await download_info.value

    os.makedirs("downloads", exist_ok=True)

    save_path = os.path.join(
        "downloads",
        download.suggested_filename
    )

    await download.save_as(save_path)

    print(f"✅ Downloaded: {save_path}")

    return save_path
"""async def downloadReport(report_page, report_name):

    print("⏳ Waiting for report generation...")

    rows = report_page.locator("#generating-reports-list tr")

    await rows.first.wait_for(state="visible", timeout=120000)

    row_count = await rows.count()

    print(f"✅ Found {row_count} report(s).")

    for i in range(row_count):

        row = rows.nth(i)

        text = await row.inner_text()

        print(f"\nRow {i + 1}:")
        print(text)

        # Only use the requested report and only when complete
        if report_name in text and "100%" in text:

            print(f"✅ Matching completed report found: {report_name}")

            download_btn = row.get_by_role(
                "link",
                name="Download"
            )

            async with report_page.expect_download(
                timeout=240000
            ) as download_info:

                await download_btn.click()

            download = await download_info.value

            save_folder = "downloads"
            os.makedirs(save_folder, exist_ok=True)

            file_name = download.suggested_filename

            save_path = os.path.join(
                save_folder,
                file_name
            )

            await download.save_as(save_path)

            print(f"✅ Downloaded: {save_path}")

            return save_path

    raise Exception(
        f"No completed {report_name} found in Report Monitor."
    )"""