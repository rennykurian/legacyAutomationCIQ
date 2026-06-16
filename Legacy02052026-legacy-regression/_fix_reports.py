import os

base = r'C:\Automation\legacy_automation\Legacy02052026-legacy-regression'

TEMPLATE = '''\
import asyncio
import os
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup


async def {func_name}():
    playwright = None
    browser = None
    page = None

    try:
        os.environ["PLAYWRIGHT_HEADLESS"] = "0"  # run headed so output is visible
        playwright, browser, page = await login()
        await handle_cookie_popup(page)

        # Navigate to Report Builder
        await page.hover("div.tmbButtonBarContainerLeft div")
        await page.wait_for_timeout(1000)
        await page.get_by_role("link", name="Report Builder").click()
        await page.wait_for_load_state("load")
        print("\u2705 Report Builder page loaded.")

        # Open Entity Selector
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog__esLink")
        print("\u2705 Entity selection modal opened.")

        # Search for entity
        search_box = "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es_searchbox"
        await page.wait_for_selector(search_box, timeout=10000)
        await page.fill(search_box, "Bank of America Corporation")
        await page.wait_for_timeout(3000)

        # Select the first result
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("Enter")
        await page.click(
            "#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__es-ava-g-10001 > ul > li:nth-child(1) > table > tbody > tr > td.tree-data > div")

        # Save entity selection
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal_ctl12__saveBtn")
        await page.click("#_rptOpts__rptOptsDS__optsDs__optsTog_float_esModal__esSaveCancel__saveBtn")
        print("\u2705 Entity selection saved.")

        # Select template and trigger download
        await page.wait_for_load_state("load")
        await page.wait_for_timeout(2000)

        await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label")
        print("\u2705 Clicked on Capital IQ Templates.")

        await page.click("{template_img_id}")
        print("\u2705 Clicked on {report_label} option.")
        await page.wait_for_timeout(5000)
        await page.wait_for_selector("body > div.wrapper", state="visible", timeout=20000)

        download_button = page.locator("body > div.wrapper").get_by_text("Download")
        async with page.expect_download(timeout=60000) as download_info:
            await download_button.click()
        download = await download_info.value

        save_folder = "downloads"
        os.makedirs(save_folder, exist_ok=True)
        save_path = os.path.join(save_folder, "{save_filename}")
        await download.save_as(save_path)
        print(f"\u2705 Report downloaded and saved to {{save_path}}")
        return save_path

    except Exception as e:
        print(f"\u274c Error: {{e}}")
        return None

    finally:
        print("\U0001F512 Closing browser...")
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
    asyncio.run({func_name}())
'''

files = [
    ('Detailed Report (Excel).py',  'generate_and_save_detailed_report_excel', '#RepBldrTemplateImg6', 'Detailed_Report_Excel.xlsx', 'Detailed Report Excel'),
    ('Detailed Report (PDF).py',    'generate_and_save_detailed_report_pdf',   '#RepBldrTemplateImg4', 'Detailed_Report.pdf',        'Detailed Report PDF'),
    ('Detailed Report (Word).py',   'generate_and_save_detailed_report_word',  '#RepBldrTemplateImg5', 'Detailed_Report.docx',       'Detailed Report Word'),
    ('Summary Report (Excel).py',   'generate_and_save_summary_report_excel',  '#RepBldrTemplateImg3', 'Summary_Report_Excel.xlsx',  'Summary Report Excel'),
    ('Summary Report (PDF).py',     'generate_and_save_summary_report_pdf',    '#RepBldrTemplateImg2', 'Summary_Report.pdf',         'Summary Report PDF'),
    ('Summary Report (Word).py',    'generate_and_save_summary_report_word',   '#RepBldrTemplateImg1', 'Summary_Report_Word.docx',   'Summary Report Word'),
    ('Tearsheet Report (Word).py',  'generate_tearsheet_report_word',          '#RepBldrTemplateImg7', 'Tearsheet_Report_Word.docx', 'Tearsheet Report Word'),
]

for filename, func, img_id, save_file, label in files:
    path = os.path.join(base, filename)
    content = TEMPLATE.format(
        func_name=func,
        template_img_id=img_id,
        save_filename=save_file,
        report_label=label,
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Written: {filename}')

print('Done. All 7 report files fixed.')
