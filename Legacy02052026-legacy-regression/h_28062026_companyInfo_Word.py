import asyncio

from z_28062026_common_reportBuilder import (
    selectCompanyInfo,
    selectCompanyInfoFormat,
    generateReport,
    downloadReport
)

async def generate_companyInfo_word():

    playwright, browser, page = await selectCompanyInfo()

    await selectCompanyInfoFormat(page, "word")

    report_page = await generateReport(page)

    save_path = await downloadReport(report_page)

    print(f"Saved to: {save_path}")

    await browser.close()
    await playwright.stop()

    return save_path


if __name__ == "__main__":
    asyncio.run(generate_companyInfo_word())