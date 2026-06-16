"""async def manage_download(
    page: Page,
    button_selector: str,
    download_path: str = "downloads",
    custom_name: str = None,
    file_name: str = None
) -> str:

    try:

        # CREATE DOWNLOAD FOLDER
        download_path = os.path.abspath(download_path)

        os.makedirs(download_path, exist_ok=True)

        print(f"📁 Download path: {download_path}")

        # DEBUG EVENTS
        page.on(
            "download",
            lambda d: print(
                f"📥 Download event: {d.suggested_filename}"
            )
        )

        # --------------------------------
        # STEP 1 - GENERATE BINDER
        # --------------------------------
        print("⏳ Generating binder...")

        await page.click(button_selector)

        # IMPORTANT FOR CIQ
        # wait for backend processing
        await page.wait_for_timeout(30000)

        # --------------------------------
        # STEP 2 - ACTUAL DOWNLOAD
        # --------------------------------
        print("⏳ Waiting for actual download...")

        async with page.expect_download(
            timeout=120000
        ) as download_info:

            # second click triggers download
            await page.click(button_selector)

        download = await download_info.value

        print("✅ Download event captured.")

        # --------------------------------
        # FILE NAME
        # --------------------------------
        suggested_name = download.suggested_filename

        if file_name:

            filename = file_name

        elif custom_name:

            ext = Path(suggested_name).suffix

            filename = f"{Path(custom_name).stem}{ext}"

        else:

            filename = suggested_name

        save_path = os.path.join(
            download_path,
            filename
        )

        # HANDLE DUPLICATE FILES
        base = os.path.splitext(save_path)[0]

        ext = os.path.splitext(save_path)[1]

        counter = 1

        while os.path.exists(save_path):

            save_path = f"{base}_{counter}{ext}"

            counter += 1

        # SAVE FILE
        await download.save_as(save_path)

        print(f"✅ Download saved: {save_path}")

        return save_path

    except Exception as e:

        print(
            f"❌ Download failed for selector "
            f"{button_selector}: {e}"
        )

        return None

"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright, Browser, Page


async def manage_download(page: Page, button_selector: str, download_path: str = "downloads", 
                         custom_name: str = None, file_name: str = None, source: str = None) -> str:
    """
    Handles file download triggered by clicking a selector.
    Handles both popup and direct download scenarios.
    Auto-detects file type and source, applies correct naming and extension.
    
    Args:
        page: Playwright page object
        button_selector: CSS selector for download button
        download_path: Where to save file (default: "downloads")
        custom_name: Custom filename with auto-extension detection
        file_name: Explicit filename (overrides auto-detection)
        source: Download source for tracking ("dropdown", "options", "report_icon", "single_report")
                Auto-detected if not provided
    
    Returns:
        Path to downloaded file, or None if failed
    """
    # Auto-detect source from selector if not provided
    if not source:
        if "rc_" in button_selector:
            source = "dropdown"
        elif "layout_optionsButton_" in button_selector:
            source = "options"
        elif "GenerateBinderLink" in button_selector:
            source = "report_icon"
        else:
            source = "unknown"
    
    # Ensure directory exists with proper permissions
    try:
        repo_root = Path(__file__).resolve().parent
        download_path = Path(download_path)
        if not download_path.is_absolute():
            download_path = (repo_root / download_path).resolve()

        download_path.mkdir(parents=True, exist_ok=True)
        # Verify write permissions
        test_file = download_path / ".write_test"
        test_file.write_text("test")
        test_file.unlink()
    except Exception as e:
        print(f"❌ Cannot write to {download_path}: {e}")
        # Try alternative path inside repo root
        download_path = (repo_root / "downloads").resolve()
        download_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Using fallback path: {download_path}")

    try:
        # Prepare selector before click
        await page.wait_for_selector(
            button_selector,
            state="attached",
            timeout=30000
        )

        if "rc_" in button_selector:
            # Menu items can remain hidden in the DOM while still being actionable
            try:
                await page.wait_for_selector(
                    button_selector,
                    state="visible",
                    timeout=5000
                )
            except Exception:
                pass
            await page.wait_for_timeout(500)

        force_click = "rc_" in button_selector
        if force_click:
            print(f"ℹ️ Using force click for hidden menu item: {button_selector}")

        page_download_task = asyncio.create_task(
            page.wait_for_event("download", timeout=120000)
        )
        popup_task = asyncio.create_task(
            page.context.wait_for_event("page", timeout=30000)
        )

        try:
            await page.click(button_selector, force=force_click)
        except Exception as click_error:
            print(f"⚠ Click attempt failed: {click_error}")
            if force_click:
                # Try a direct DOM click if Playwright click cannot act on the hidden menu item
                await page.evaluate(
                    "selector => document.querySelector(selector).click()",
                    button_selector
                )
            else:
                raise

        done, pending = await asyncio.wait(
            {page_download_task, popup_task},
            return_when=asyncio.FIRST_COMPLETED
        )

        if page_download_task in done:
            download = page_download_task.result()
            popup_task.cancel()
            print("✅ Download event captured from original page")
        else:
            popup = popup_task.result()
            page_download_task.cancel()
            print("✅ Popup opened, waiting for download inside popup")
            download = await popup.wait_for_event("download", timeout=120000)
            print("✅ Download event captured from popup")

        # Determine filename
        suggested_name = download.suggested_filename

        if file_name:
            filename = file_name
        elif custom_name:
            ext = Path(suggested_name).suffix
            # Include source in filename for tracking
            base_name = Path(custom_name).stem
            filename = f"{base_name}_[{source}]{ext}"
        else:
            filename = suggested_name

        save_path = os.path.join(download_path, filename)
        
        # Handle duplicate files
        base_path = os.path.splitext(save_path)[0]
        ext = os.path.splitext(save_path)[1]
        counter = 1
        while os.path.exists(save_path):
            save_path = f"{base_path}_{counter}{ext}"
            counter += 1

        await download.save_as(save_path)
        print(f"✅ Download saved: {save_path} (source: {source})")
        return save_path

    except Exception as e:
        print(f"❌ Download failed for selector {button_selector}: {e}")
        return None


async def navigate_to_binder(page: Page) -> bool:
    """
    Navigate to Documents & Reports and select binder.
    Common setup for all binder download scripts.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        documentsAndReports = "https://www.capitaliq.com/CIQDotNet/DocManagement/ReportsCenter.aspx"
        await page.goto(
            documentsAndReports,
            timeout=60000,
            wait_until="domcontentloaded"
        )
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.wait_for_selector("#_pageHeader_PageHeaderLabel", timeout=30000)
        print(" ✅ redirected to Documents and Reports successfully")

        await page.wait_for_selector("#folderTreeScroller > div > div:nth-child(2) > div:nth-child(2)")
        binder = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrName"
        await page.click(binder)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder successfully")
        
        return True
    except Exception as e:
        print(f"❌ Navigation failed: {e}")
        return False


async def setup_download_all_documents(page: Page) -> bool:
    """
    Setup for 'download all documents' workflow (binder dropdown).
    Used by: ZIP, Word, PDF, RTF, Excel scripts
    """
    try:
        binder_dropdown = "#layout_folder_frb-90308440 > table > tbody > tr > td.fldrMenu"
        await page.click(binder_dropdown)
        await page.wait_for_timeout(5000)
        print("✅ clicked on binder_dropdown successfully")
        return True
    except Exception as e:
        print(f"❌ Setup download all documents failed: {e}")
        return False


async def setup_download_from_options(page: Page) -> bool:
    """
    Setup for 'download from options' workflow (checkbox + options button).
    Used by: Word from options, PDF from options scripts
    """
    try:
        checkbox = "#layout_documents > table.cTblListBody.docTable.ui-sortable > thead > tr > th.cbcol > input[type=checkbox]"
        await page.wait_for_selector(checkbox)
        await page.click(checkbox)
        print("✅ checkbox selected")
        await page.wait_for_timeout(5000)
        
        options_button = "#layout_optionsButton_MenuButton"
        await page.click(options_button)
        await page.wait_for_timeout(5000)
        print("✅ clicked on options button successfully")
        
        return True
    except Exception as e:
        print(f"❌ Setup download from options failed: {e}")
        return False       

#checking for binder_generate_excel_from_options.py for differences in navigate_to_binder and setup functions
