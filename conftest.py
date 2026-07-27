"""pytest fixtures: one AltDriver connection per session + screenshot-on-failure.

If no AltServer is reachable (the license-gated broker isn't running), the `alt`
fixture SKIPS rather than fails every test — so an infra outage reads as
"skipped: AltServer unavailable", not a wall of red. Real assertion failures still
fail normally.
"""
from __future__ import annotations

import pytest

from config import settings
from utils.alt_connect import open_driver, close_driver

settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def alt():
    try:
        driver = open_driver()
    except ConnectionError as exc:
        pytest.skip(f"AltServer unavailable — {exc}")
        return
    try:
        yield driver
    finally:
        close_driver(driver)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Capture a screenshot when a test fails, saved under reports/screenshots/."""
    outcome = yield
    report = outcome.get_result()
    # Report on failures in setup (fixtures) or the call itself — a blank/
    # unresponsive screen often surfaces as a fixture command timeout.
    if report.when not in ("setup", "call") or not report.failed:
        return
    driver = item.funcargs.get("alt")
    safe = item.nodeid.replace("/", "_").replace("::", "__").replace(".py", "")
    path = settings.SCREENSHOTS_DIR / f"{safe}.png"
    try:
        if driver is not None:
            driver.get_png_screenshot(str(path))
            print(f"\n[screenshot] {path}")
    except Exception as exc:  # pragma: no cover - best effort
        print(f"\n[screenshot failed] {exc}")

    # Capture blank-screen evidence (adb screenshot + logcat + scene) for every
    # failure so app issues (e.g. blank screens) are reported with context.
    try:
        from utils import blank_screen
        blank_screen.report(safe, driver, reason=f"{report.when} failure: {item.nodeid}")
    except Exception as exc:  # pragma: no cover
        print(f"\n[diagnostics failed] {exc}")
