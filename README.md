# refresh

A script that refreshes [hobbylandeshop.com/cup2026](https://www.hobbylandeshop.com/cup2026)
every **0.5 s** and stops as soon as a date-selection widget appears on the page.

## Requirements

- Python 3.9+
- [Playwright](https://playwright.dev/python/)

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

```bash
python refresh.py
```

The script opens a visible Chromium browser window, keeps reloading the page every 0.5 s, and
prints a message as soon as it detects a date-selection element. The browser stays open
afterwards so you can interact with the page. Press **Ctrl+C** to exit.
