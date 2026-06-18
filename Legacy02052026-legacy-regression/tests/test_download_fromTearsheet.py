import pytest
import os
import sys

# ✅ Ensure Python can find your module (root folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tearsheet_ciqWordReport import  generate_save_ciq_report_tearsheet
from tearsheet_QuickReport import generate_save_quick_report_fromTearsheet
from tearsheet_tenK_excel import generate_ten_kExcel_from_tearsheet
from tearsheet_tenK_word import  generate_ten_kWORD_from_tearsheet  
from tearsheet_tenK_pdf import generate_ten_kPDF_from_tearsheet

@pytest.mark.asyncio
async def test_generate_tearsheet_report_word_download():  
    result = await generate_save_ciq_report_tearsheet()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_tearsheet_quick_report_download():  
    result = await generate_save_quick_report_fromTearsheet()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio   
async def test_generate_tearsheet_10K_excel_download():  
    result = await generate_ten_kExcel_from_tearsheet()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 
@pytest.mark.asyncio
async def test_generate_tearsheet_10K_word_download():  
    result = await generate_ten_kWORD_from_tearsheet()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_tearsheet_10K_pdf_download():  
    result = await generate_ten_kPDF_from_tearsheet()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 

