import pytest
import os
import sys

# Ensure Python can find your project modules
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from a_28062026_summary_word import generate_summary_word
from b_28062026_summary_pdf import generate_summary_pdf
from c_28062026_summary_excel import generate_summary_excel
from d_28062026_detailed_Report_pdf import generate_detailed_pdf
from e_28062026_detailedReport_excel import generate_detailed_excel
from f_28062026_detailedReport_word import generate_detailed_word
from g_28062026_companyInfo_excel import generate_companyInfo_excel
from h_28062026_companyInfo_Word import generate_companyInfo_word
from i_28062026_copmpnayInfo_pdf import generate_companyInfo_pdf
from j_28062026_landscape import generate_CIQ_landscape
from k_28062026_tearsheet import generate_tearsheet
from l_28062026_QuickReport import generate_quickReport
@pytest.mark.asyncio
async def test_generate_summary_report_word_download():

    save_path = await generate_summary_word()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Word report downloaded successfully: {save_path}")
@pytest.mark.asyncio
async def test_generate_summary_report_pdf_download():

    save_path = await generate_summary_pdf()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ pdf report downloaded successfully: {save_path}")
@pytest.mark.asyncio    
async def test_generate_summary_report_excel_download():

    save_path = await generate_summary_excel()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Excel report downloaded successfully: {save_path}")

@pytest.mark.asyncio    
async def test_generate_detailed_report_pdf_download():

    save_path = await generate_detailed_pdf()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Detailed pdf report downloaded successfully: {save_path}")
@pytest.mark.asyncio
async def test_generate_detailed_report_excel_download():

    save_path = await generate_detailed_excel()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Detailed Excel report downloaded successfully: {save_path}")
@pytest.mark.asyncio
async def test_generate_detailed_report_word_download():

    save_path = await generate_detailed_word()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Detailed Word report downloaded successfully: {save_path}")

@pytest.mark.asyncio
async def test_generate_companyInfo_report_excel_download():
    
    save_path = await generate_companyInfo_excel()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Company Info Excel report downloaded successfully: {save_path}") 
    
@pytest.mark.asyncio
async def test_generate_companyInfo_report_word_download():
    
    save_path = await generate_companyInfo_word()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Company Info Word report downloaded successfully: {save_path}")

@pytest.mark.asyncio
async def test_generate_companyInfo_report_pdf_download():
    
    save_path = await generate_companyInfo_pdf()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Company Info PDF report downloaded successfully: {save_path}")    
@pytest.mark.asyncio
async def test_generate_CIQ_landscape_report_download():
    
    save_path = await generate_CIQ_landscape()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ CIQ Landscape report downloaded successfully: {save_path}")
@pytest.mark.asyncio
async def test_generate_tearsheet_report_download():
    
    save_path = await generate_tearsheet()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Tearsheet report downloaded successfully: {save_path}")
@pytest.mark.asyncio
async def test_generate_quickreport_download():
    
    save_path = await generate_quickReport()

    assert save_path is not None
    assert os.path.exists(save_path)

    print(f"✅ Quick Report downloaded successfully: {save_path}")