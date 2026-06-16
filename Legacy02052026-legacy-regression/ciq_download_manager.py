import asyncio
import os
from pathlib import Path
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def ciq_download_manager(
    page,
    button_selector: str,
    download_path: str = "downloads",
    file_name: str = None,
    wait_for_indicator: bool = True
):
    """
    Universal CIQ download handler:
    - PDF / Excel / ZIP / RTF
    - handles popup + waiting page
    - handles delayed downloads
    """

    os.makedirs(download_path, exist_ok=True)

    try:
        print(f"📥 Clicking: {button_selector}")

        popup = None
        try:
            async with page.context.expect_page(timeout=10000) as p:
                await page.click(button_selector)
            popup = await p.value
            print("🪟 Popup detected")
        except Exception:
            popup = page
            print("ℹ️ No popup, using same page")

        await popup.wait_for_load_state("domcontentloaded")

        if wait_for_indicator:
            for _ in range(30):
                if "BinderWaitingIndicator.aspx" not in popup.url:
                    break
                print("⌛ Waiting for CIQ processing...")
                await asyncio.sleep(2)
                try:
                    await popup.reload(timeout=5000)
                except Exception:
                    pass

        download_page = popup
        async with download_page.expect_download(timeout=180000) as download_info:
            # The download may be triggered automatically after CIQ processing completes.
            await asyncio.sleep(3)

        download = await download_info.value

        suggested = download.suggested_filename
        ext = Path(suggested).suffix

        if file_name:
            filename = Path(file_name).stem + ext
        else:
            filename = suggested

        save_path = os.path.join(download_path, filename)

        base, ext = os.path.splitext(save_path)
        counter = 1
        while os.path.exists(save_path):
            save_path = f"{base}_{counter}{ext}"
            counter += 1

        await download.save_as(save_path)
        print(f"✅ Saved: {save_path}")
        return save_path

    except PlaywrightTimeoutError:
        print("❌ Download timeout (CIQ still processing or wrong selector)")
        return None
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None
