import pytest
import asyncio
import os
import sys
import pandas as pd

# ✅ Ensure Python can find root folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Store failures globally
FAILED_TESTS = []


# =========================
# MARKERS REGISTRATION
# =========================
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "binder: marks tests as binder-related tests"
    )


# =========================
# CAPTURE FAILURES
# =========================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        FAILED_TESTS.append({
            "test_name": item.name,
            "file": item.location[0],
            "error": str(report.longrepr)
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
