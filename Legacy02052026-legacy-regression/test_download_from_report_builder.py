import pytest
import os
import sys

# ✅ Ensure Python can find your module (root folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from report_builder_ciq_report_Landscape import generate_and_save_CiqReport_landscape
#from report_builder_detailed_report_PDF import generate_and_save_detailed_report_pdf
#from report_builder_detailed_report_Excel import generate_and_save_detailed_report_excel
#from report_builder_detailed_report_Word  import generate_and_save_detailed_report_word
from report_builder_excel_companyInformation import generate_save_excel_report
from report_builder_pdf_companyInformation import generate_save_pdf_report
from report_builder_word_companyInformation import generate_save_word_report
from report_builder_summary_report_Excel import generate_and_save_summary_report_excel
from report_builder_summary_report_Word import generate_and_save_summary_report_word
from report_builder_summary_report_PDF import generate_and_save_summary_report_pdf

"""@pytest.mark.asyncio
async def test_generate_detailed_report_pdf_download():  
    result = await generate_and_save_detailed_report_pdf()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"

@pytest.mark.asyncio
async def test_generate_detailed_report_word_download():  
    result = await generate_and_save_detailed_report_word()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 
"""
@pytest.mark.asyncio
async def test_generate_summary_report_excel_download():  
    result = await generate_and_save_summary_report_excel()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio    
async def test_generate_summary_report_word_download():  
    result = await generate_and_save_summary_report_word()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}" 

@pytest.mark.asyncio
async def test_generate_summary_report_pdf_download():  
    result = await generate_and_save_summary_report_pdf()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"

@pytest.mark.asyncio
async def test_generate_excel_report_download():  
    result = await generate_save_excel_report()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_pdf_report_download():  
    result = await generate_save_pdf_report()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio    
async def test_generate_word_report_download():  
    result = await generate_save_word_report()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
@pytest.mark.asyncio
async def test_generate_CiqReport_landscape_download():  
    result = await generate_and_save_CiqReport_landscape()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
"""@pytest.mark.asyncio
async def test_generate_detailed_report_excel_download():  
    result = await generate_and_save_detailed_report_excel()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
"""