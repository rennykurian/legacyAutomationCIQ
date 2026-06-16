import pytest
import os
import sys

# ✅ Ensure Python can find your module (root folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from binder_generate_pdf_all_document import generate_as_pdf_binder_all_document
from binder_generate_excel_all_document import generate_as_excel_binder_all_document
from binder_generate_as_zip import generate_as_zip_binder_all_document
from binder_generate_as_word_document import generate_as_word_binder_all_document
from binder_generates_as_pdf import generate_as_pdf_binder_all_document as generate_as_pdf_alt
from binder_generate_rtf_all_document import generate_as_rtf_binder_all_document
from binder_generate_word_from_options import generate_as_word_binder_options
from binder_generate_pdf_from_options import generate_as_pdf_binder_options
from binder_generate_as_excel import generate_as_excel_binder_document
from binder_generate_zip_from_options import generate_as_zip_binder_options
from binder_generate_excel_from_options import generate_as_excel_binder_options

@pytest.mark.asyncio
async def test_generate_pdf_binder_download():
    """Test PDF binder generation (all documents)"""
    result = await generate_as_pdf_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_excel_binder_download():
    """Test Excel binder generation (all documents)"""
    result = await generate_as_excel_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_zip_binder_download():
    """Test ZIP binder generation (all documents)"""
    result = await generate_as_zip_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_word_binder_download():
    """Test Word binder generation (all documents)"""
    result = await generate_as_word_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_pdf_binder_alt_download():
    """Test PDF binder generation (alternative - all documents)"""
    result = await generate_as_pdf_alt()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_rtf_binder_download():
    """Test RTF binder generation (all documents)"""
    result = await generate_as_rtf_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_word_binder_from_options():
    """Test Word binder generation (from options)"""
    result = await generate_as_word_binder_options()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"


@pytest.mark.asyncio
async def test_generate_pdf_binder_from_options():
    """Test PDF binder generation (from options)"""
    result = await generate_as_pdf_binder_options()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"

@pytest.mark.asyncio
async def test_generate_as_excel():
    """Test Excel binder generation"""
    result = await generate_as_excel_binder_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"

@pytest.mark.asyncio
async def test_generate_zip_binder_all_document():
    """Test ZIP binder generation (all documents)"""
    result = await generate_as_zip_binder_all_document()
    assert result is not None, "Download path is None"
    assert os.path.exists(result), f"File does not exist: {result}"
