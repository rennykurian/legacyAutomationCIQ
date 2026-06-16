# Download Formats Mapping by Source

## Supported Formats by Download Source

### 1. Dropdown Menu (`dropdown` source)
**Selector pattern:** `#rc_*`
**Triggered by:** Binder dropdown menu

| Format | Selector | Implemented | Status |
|--------|----------|-------------|--------|
| PDF | `#rc_genPDF` | ✅ Yes | [binder_generate_pdf_all_document.py](binder_generate_pdf_all_document.py) |
| Excel | `#rc_genXLS` | ✅ Yes | [binder_generate_excel_all_document.py](binder_generate_excel_all_document.py) |
| Word | `#rc_genWord` | ✅ Yes | [binder_generate_as_word_document.py](binder_generate_as_word_document.py) |
| RTF | `#rc_genRTF` | ✅ Yes | [binder_generate_rtf_all_document.py](binder_generate_rtf_all_document.py) |
| ZIP | `#rc_dlZip` | ✅ Yes | [binder_generate_as_zip.py](binder_generate_as_zip.py) |

---

### 2. Options Button (`options` source)
**Selector pattern:** `#layout_optionsButton_*`
**Triggered by:** Checkbox selection + Options button click

| Format | Selector | Implemented | Status |
|--------|----------|-------------|--------|
| PDF | `#layout_optionsButton_generatePDFLink_txt_0` | ✅ Yes | [binder_generate_pdf_from_options.py](binder_generate_pdf_from_options.py) |
| Excel | `#layout_optionsButton_generateExcelLink_txt_0` | ✅ Yes | [binder_generate_excel_from_options.py](binder_generate_excel_from_options.py) |
| Word | `#layout_optionsButton_generateWordLink_txt_0` | ✅ Yes | [binder_generate_word_options_alt.py](binder_generate_word_options_alt.py) |
| RTF | `#layout_optionsButton_generateRTFLink_txt_0` | ✅ Yes | [binder_generate_word_from_options.py](binder_generate_word_from_options.py) |
| ZIP | `#layout_optionsButton_generateZipLink_txt_0` | ✅ Yes | [binder_generate_zip_from_options.py](binder_generate_zip_from_options.py) |

---

### 3. Report Icons (`report_icon` source)
**Selector pattern:** `#GenerateBinderLink* > img`
**Triggered by:** Icon buttons beside dropdown menu

| Format | Selector | Implemented | Status |
|--------|----------|-------------|--------|
| PDF | `#GenerateBinderLink1 > img` | ✅ Yes | [binder_generates_as_pdf.py](binder_generates_as_pdf.py) |
| Word | `#GenerateBinderLink2 > img` | ✅ Yes | (uses manage_download) |
| Excel | `#GenerateBinderLink3 > img` | ✅ Yes | [binder_generate_as_excel.py](binder_generate_as_excel.py) |
| ZIP | `#GenerateBinderLink4 > img` | ✅ Yes | (uses manage_download) |

---

### 4. Single Report (`single_report` source)
**Selector pattern:** Report-specific icon
**Triggered by:** Icon in front of individual report name

| Format | Selector | Implemented | Status |
|--------|----------|-------------|--------|
| All formats | TBD | ⏳ Pending | **NEEDS INVESTIGATION** |

---

## Missing Implementations

### ✅ Options Button Variants - ALL COMPLETE
1. **Excel from Options** ✅ - `#layout_optionsButton_generateExcelLink_txt_0`
   - [binder_generate_excel_from_options.py](binder_generate_excel_from_options.py)
   - Uses: `source="options"`, `file_name="Report_Excel.xlsx"`

2. **Word from Options** ✅ - `#layout_optionsButton_generateWordLink_txt_0`
   - [binder_generate_word_options_alt.py](binder_generate_word_options_alt.py)
   - Uses: `source="options"`, `file_name="Report_Word.docx"`

3. **ZIP from Options** ✅ - `#layout_optionsButton_generateZipLink_txt_0`
   - [binder_generate_zip_from_options.py](binder_generate_zip_from_options.py)
   - Uses: `source="options"`, `file_name="Report_ZIP.zip"`

### Future - Single Report Support (⏳ Under Investigation)
**Selector pattern:** Document table rows with individual icons
**Base selector:** `#layout_documents > table.cTblListBody.docTable.ui-sortable > tbody > tr`

**Investigation findings:**
- Individual document rows exist in table: `#layout_documents > table.cTblListBody.docTable`
- Each row has document name and potential download icon
- Pattern: `#layout_documents tbody tr[data-doc-id="..."] > td.downloadCol > img`
- Need to: 
  1. Identify actual download icon selector per row
  2. Get document name from row for auto-naming
  3. Implement loop for single/multiple selected documents
  4. Test with actual UI to verify selector pattern

**Expected implementation:**
```python
# Get document name from row
doc_name = await page.query_selector(f"tr[data-doc-id='{doc_id}'] .docName")
# Download with auto-naming: docName_[single_report].ext
```

---

## File Naming Convention

All downloads use the shared `manage_download()` helper which auto-includes source:

```
{custom_name}_[{source}].{ext}
```

**Examples:**
- `Ganesha_[dropdown].pdf` - From dropdown menu
- `Ganesha_[options].xlsx` - From options button
- `Ganesha_[report_icon].zip` - From report icon
- `Ganesha_[single_report].pdf` - From individual report

---

## Implementation Template for Missing Scripts

```python
import asyncio
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_from_options

async def generate_as_{format}_binder_options():
    playwright = None
    browser = None
    page = None

    try:
        playwright, browser, page = await login()
        print("✅ Login successful.")

        await handle_cookie_popup(page)
        await page.wait_for_timeout(5000)

        # Navigate to binder
        if not await navigate_to_binder(page):
            print("❌ Failed to navigate to binder.")
            return None

        # Setup download options (checkbox + options button)
        if not await setup_download_from_options(page):
            print("❌ Failed to setup download options.")
            return None

        print("📥 Starting {FORMAT} download...")

        # Download using shared helper
        save_path = await manage_download(
            page=page,
            button_selector="#{SELECTOR}",
            download_path="downloads",
            file_name="Report_{FORMAT}.{EXT}",
            source="options"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            return save_path

        print("❌ Download failed.")
        return None

    except Exception as e:
        print(f"❌ Error occurred: {e}")
        return None

    finally:
        print("🔒 Closing browser...")
        try:
            if page:
                await page.close()
        except:
            pass
        try:
            if browser:
                await browser.close()
        except:
            pass
        try:
            if playwright:
                await playwright.stop()
        except:
            pass
        await asyncio.sleep(1)

if __name__ == "__main__":
    result = asyncio.run(generate_as_{format}_binder_options())
    if result:
        print(f"✅ Result: {result}")
```

---

## Testing Coverage

Run all tests to verify implementations:
```powershell
pytest tests/test_download_binder.py -v
```

Current status: 10/10 tests passing ✅
