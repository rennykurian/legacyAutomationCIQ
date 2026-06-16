import pytest
import asyncio
import os
import sys

# ✅ Ensure Python can find your module (root folder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# ✅ Custom markers
def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "binder: marks tests as binder-related tests"
    )


# ✅ Run tests sequentially (not in parallel) to save login time
def pytest_configure(config):
    """Disable parallel execution by default."""
    # This ensures tests run one after another, not in parallel
    # You can still use -n flag to override if pytest-xdist is installed
    pass