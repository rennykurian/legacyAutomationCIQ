import pytest
import os
import sys

# ✅ Ensure Python can find your module (root folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tearsheet_ciqWordReport import generate_tearsheet_report_word
from tearsheet_QuickReport import generate_tearsheet_quick_report
from tearsheet_tenK_excel import generate_tearsheet_10K_excel
from tearsheet_tenK_word import generate_tearsheet_10K_word  
from tearsheet_tenK_pdf import generate_tearsheet_10K_pdf

@pytest.mark.asyncio
async def test_generate_tearsheet_report_word_download():  
    result = await generate_tearsheet_report_word()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_tearsheet_quick_report_download():  
    result = await generate_tearsheet_quick_report()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio   
async def test_generate_tearsheet_10K_excel_download():  
    result = await generate_tearsheet_10K_excel()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 
@pytest.mark.asyncio
async def test_generate_tearsheet_10K_word_download():  
    result = await generate_tearsheet_10K_word()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_tearsheet_10K_pdf_download():  
    result = await generate_tearsheet_10K_pdf()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 

