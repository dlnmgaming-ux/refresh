"""
Refresh https://www.hobbylandeshop.com/cup2026 every 0.5 s until a date
selection element appears on the page, then stop and notify the user.
"""

import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

TARGET_URL = "https://www.hobbylandeshop.com/cup2026"
INTERVAL = 0.5  # seconds between refreshes

# CSS selectors that indicate a date-selection widget is present
DATE_SELECTORS = [
    "input[type='date']",
    "input[type='datetime-local']",
    "select[name*='date']",
    "select[id*='date']",
    "select[class*='date']",
    "[class*='date-picker']",
    "[class*='datepicker']",
    "[class*='DatePicker']",
    "[class*='calendar']",
    "[class*='Calendar']",
    # Common e-commerce / booking date selectors
    ".date-select",
    "#date-select",
    "[data-testid*='date']",
    "select[name*='delivery']",
    "select[id*='delivery']",
]


def date_selection_visible(page) -> bool:
    """Return True if any date-selection element is present and visible."""
    for selector in DATE_SELECTORS:
        try:
            element = page.query_selector(selector)
            if element and element.is_visible():
                print(f"  → found date selector matching: {selector!r}")
                return True
        except Exception:
            continue
    return False


def main() -> None:
    attempt = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print(f"Opening {TARGET_URL} …")
        try:
            page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=30_000)
        except PlaywrightTimeoutError:
            print("Initial load timed out – continuing anyway.")

        while True:
            attempt += 1
            print(f"[attempt {attempt}] Checking for date selection …", end=" ")

            if date_selection_visible(page):
                print("\n✅  Date selection is now available!")
                print("The browser window will stay open. Press Ctrl+C to exit.")
                # Keep the browser open so the user can interact with it
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
                break

            print("not found, refreshing …")
            time.sleep(INTERVAL)
            try:
                page.reload(wait_until="domcontentloaded", timeout=15_000)
            except PlaywrightTimeoutError:
                print("  (reload timed out, retrying)")

        browser.close()


if __name__ == "__main__":
    main()
