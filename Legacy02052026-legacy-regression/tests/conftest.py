import pytest
import os
import sys
import pandas as pd

# Ensure root folder access
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

FAILED_TESTS = []


# =========================
# MARKERS
# =========================
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
    config.addinivalue_line(
        "markers", "binder: marks binder tests"
    )


# =========================
# CAPTURE FAILURES + SCREENSHOT
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        screenshot_path = None

        # Try to access Playwright page fixture
        page = item.funcargs.get("page", None)

        if page:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{item.name}.png"
            try:
                page.screenshot(path=screenshot_path, full_page=True)
            except Exception as e:
                screenshot_path = None

        FAILED_TESTS.append({
            "test_name": item.name,
            "file": item.location[0],
            "error": str(report.longrepr),
            "screenshot": screenshot_path
        })


# =========================
# GENERATE EXCEL REPORT
# =========================
def pytest_sessionfinish(session, exitstatus):
    if FAILED_TESTS:
        report_file = "test_failure_report.xlsx"

        df = pd.DataFrame(FAILED_TESTS)
        df.to_excel(report_file, index=False)

        print("\n==============================")
        print(f"Excel report generated: {report_file}")
        print("==============================\n")
