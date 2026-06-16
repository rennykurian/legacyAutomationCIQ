# Refactoring Guide for Remaining 4 Scripts

## Scripts Still Need Refactoring:
1. `binder_generate_as_word_document.py`
2. `binder_generates_as_pdf.py`
3. `binder_generate_rtf_all_document.py`
4. `binder_generate_word_from_options.py`

---

## Template for "All Documents" Scripts (3 scripts)

For: `binder_generate_as_word_document.py`, `binder_generates_as_pdf.py`, `binder_generate_rtf_all_document.py`

### Replace entire file with:

```python
import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_all_documents


async def generate_as_FORMAT_binder_all_document():
    """Generate binder as SPECIFIC_FORMAT for all documents."""
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        # Use shared navigation function
        if not await navigate_to_binder(page):
            await browser.close()
            return None

        # Use shared setup function
        if not await setup_download_all_documents(page):
            await browser.close()
            return None

        # Use shared download function with script-specific button selector
        save_path = await manage_download(
            page,
            button_selector="UNIQUE_BUTTON_SELECTOR",  # ← CHANGE THIS PER SCRIPT
            download_path=r"D:\Legacy04082025\downloads",
            custom_name="CUSTOM_FILENAME"  # ← CHANGE THIS PER SCRIPT
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
        else:
            print("❌ Download failed.")

        await browser.close()
        return save_path


if __name__ == "__main__":
    result = asyncio.run(generate_as_FORMAT_binder_all_document())
    if result:
        print(f"✅ Result: {result}")
```

### Script-Specific Changes:

#### 1. `binder_generate_as_word_document.py`
- Function name: `generate_as_word_binder_all_document` (KEEP EXISTING)
- Button selector: `"#GenerateBinderLink2 > img"`
- Custom name: `"Ganesha_word"`

#### 2. `binder_generates_as_pdf.py`
- Function name: `generate_as_pdf_binder_all_document` (KEEP EXISTING)
- Button selector: `"#GenerateBinderLink1 > img"`
- Custom name: `"Ganesha_pdf"`

#### 3. `binder_generate_rtf_all_document.py`
- Function name: `generate_as_rtf_binder_all_document` (KEEP EXISTING)
- Button selector: `"#rc_genRTF"`
- File name: `"BinderReportword.rtf"` (use `file_name` param, not `custom_name`)
- Change last call to:
```python
save_path = await manage_download(
    page,
    button_selector="#rc_genRTF",
    download_path=r"D:\Legacy04082025\downloads",
    file_name="BinderReportword.rtf"
)
```

---

## Template for "From Options" Script (1 script)

For: `binder_generate_word_from_options.py`

### Replace entire file with:

```python
import asyncio
from playwright.async_api import async_playwright
from TestLoginLegacy import login
from test_handleCookie import handle_cookie_popup
from binder_common import manage_download, navigate_to_binder, setup_download_from_options


async def generate_as_word_binder_options():
    """Generate binder as Word from selected documents."""
    async with async_playwright():
        playwright, browser, page = await login()
        await handle_cookie_popup(page)
        await page.wait_for_timeout(10000)

        # Use shared navigation function
        if not await navigate_to_binder(page):
            await browser.close()
            return None

        # Use shared setup function for "from options" workflow
        if not await setup_download_from_options(page):
            await browser.close()
            return None

        # Use shared download function
        save_path = await manage_download(
            page,
            button_selector="#layout_optionsButton_generateRTFLink_0",  # WORD = RTF selector
            download_path=r"D:\Legacy04082025\downloads",
            file_name="fromoptionword.rtf"
        )

        if save_path:
            print(f"🎉 Download complete: {save_path}")
            return save_path
        else:
            print("❌ Download failed.")
            return None

        await browser.close()


if __name__ == "__main__":
    result = asyncio.run(generate_as_word_binder_options())
    if result:
        print(f"✅ Result: {result}")
```

---

## Testing After Refactoring Each Script

After refactoring each script:

```bash
# Test the script runs standalone
python binder_generate_SCRIPT_NAME.py

# Test the pytest test passes
pytest tests/test_download_binder.py::test_generate_SPECIFIC_download -v
```

---

## Expected Results Per Script

| Script | Lines Before → After | Time Saved |
|--------|----------------------|------------|
| binder_generate_as_word_document.py | 95 → 42 | ~50 lines |
| binder_generates_as_pdf.py | 95 → 42 | ~50 lines |
| binder_generate_rtf_all_document.py | 90 → 42 | ~48 lines |
| binder_generate_word_from_options.py | 90 → 42 | ~48 lines |
| **TOTAL** | **370 → 168** | **~202 lines** |

---

## Verification Checklist

After refactoring all 4 scripts:

- [ ] All 4 scripts run without errors: `python script.py`
- [ ] All 9 tests pass: `pytest tests/test_download_binder.py -v`
- [ ] No duplicate code between scripts and `binder_common.py`
- [ ] All original functionality preserved
- [ ] Code is more readable and maintainable

---

## Quick Commands to Apply

To apply refactoring to all 4 files (copy/paste as needed):

```bash
# View a refactored example:
cat binder_generate_as_zip.py

# Compare with original pattern in binder_common.py:
head -50 binder_common.py

# Test all scripts still work:
python binder_generate_as_word_document.py
python binder_generates_as_pdf.py
python binder_generate_rtf_all_document.py
python binder_generate_word_from_options.py

# Run all tests:
pytest tests/test_download_binder.py -v
```
