"""async def handle_cookie_popup(page):
    try:
        # Adjust text selector if button text is different
        await page.wait_for_selector("text='Accept All'", timeout=3000)
        accept_btn = page.locator("text='Accept All'")
        if await accept_btn.is_visible():
            await accept_btn.click()
            print("✅ 'Accept All Cookies' clicked.")
        else:
            print("⚠️ Cookie button not visible.")
    except:
        print("ℹ️ No cookie popup appeared.")

from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def handle_cookie_popup(page):
    
    #Safely handles the cookie consent popup.
    

    try:
        accept_button = page.get_by_role(
            "button",
            name= "Accept optional cookies",
            exact=True
        )

        if await accept_button.is_visible(timeout=5000):
            await accept_button.click()
            print("✅ Accepted cookies.")
        else:
            print("ℹ️ Cookie popup not visible.")

    except PlaywrightTimeoutError:
        print("ℹ️ Cookie popup did not appear.")

    except Exception as e:
        print(f"⚠️ Cookie handler error: {e}")
from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def handle_cookie_popup(page):
    
    Handle cookie banner if it appears.
    Tries several common buttons before continuing.
    

    try:
        await page.wait_for_timeout(2000)

        button_names = [
            "Accept All",
            "Accept Optional Cookies",
            "Reject Optional Cookies",
            "Reject All",
            "Allow All",
            "Accept",
            "Accept Cookies",
            "Agree",
            "I Agree",
            "OK",
            "Got it"
        ]

        for name in button_names:
            button = page.get_by_role("button", name=name, exact=True)

            try:
                if await button.count() > 0:
                    if await button.first.is_visible():
                        print(f"🍪 Clicking '{name}'")
                        await button.first.click()
                        await page.wait_for_timeout(1000)
                        return
            except Exception:
                pass

        print("ℹ️ Cookie banner found, but no supported button was available.")

    except PlaywrightTimeoutError:
        print("ℹ️ No cookie banner appeared.")

    except Exception as e:
        print(f"⚠️ Cookie handler warning: {e}")"""


from playwright.async_api import TimeoutError as PlaywrightTimeoutError


async def handle_cookie_popup(page):
    """
    Handle cookie banner before any other interaction.
    Prefers Accept Optional Cookies if available,
    otherwise Reject Optional Cookies,
    otherwise Accept All / Reject All.
    """

    try:
        await page.wait_for_timeout(1000)

        button_selectors = [
            "#onetrust-accept-btn-handler",   # Accept Optional Cookies
            "#onetrust-reject-all-handler",   # Reject Optional Cookies
        ]

        button_names = [
            "Accept Optional Cookies",
            "Reject Optional Cookies",
            "Accept All",
            "Reject All",
            "Accept",
            "Reject",
            "Allow All",
            "Accept Cookies",
            "Agree",
            "I Agree",
            "OK",
            "Got it",
        ]

        # ---------- Try ID first ----------
        for selector in button_selectors:
            button = page.locator(selector)

            if await button.count() > 0:
                if await button.first.is_visible():
                    text = (await button.first.inner_text()).strip()

                    print(f"🍪 Clicking '{text}'")

                    await button.first.click()

                    await page.wait_for_load_state("networkidle")

                    return

        # ---------- Try accessible names ----------
        for name in button_names:

            button = page.get_by_role(
                "button",
                name=name,
                exact=True
            )

            if await button.count() > 0:

                if await button.first.is_visible():

                    print(f"🍪 Clicking '{name}'")

                    await button.first.click()

                    await page.wait_for_load_state("networkidle")

                    return

        print("ℹ️ Cookie popup not found.")

    except PlaywrightTimeoutError:
        print("ℹ️ Cookie popup did not appear.")

    except Exception as e:
        print(f"⚠️ Cookie handler error: {e}")