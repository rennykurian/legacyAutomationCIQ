import asyncio

from z_28062026_common_reportBuilder import (
    selectCompany,
    generateReport,
    getReportWindow,
    downloadReport,
)

async def generate_summary_word():

    playwright, browser, page = await selectCompany()

    await page.click("#_templatesFilmstrip__filmstripDS_ctl02__ciqTempRb_span > label")

    await page.click("#RepBldrTemplateImg1")
    print("✅ Summary word template selected.")

    report_page = await generateReport(page)

    save_path = await downloadReport(report_page)

    print(f"Saved to: {save_path}")

    await browser.close()
    await playwright.stop()
    return save_path


if __name__ == "__main__":
    asyncio.run(generate_summary_word())