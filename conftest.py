"""
conftest.py — Appium session for English Gurukul student app.
Works with any installed APK — no AltTester needed.

Before running:
    Terminal 1:  appium --port 4723
    Terminal 2:  adb devices
                 adb forward tcp:4723 tcp:4723
                 pytest tests/test_login_flow.py -v -s
"""
import pytest, time
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from utils.logger import log

APP_PACKAGE  = "com.OritSciencesPrivateLimited.EnglishGurukul.studentapp"
APP_ACTIVITY = "io.branch.unity.BranchUnityActivity"
APPIUM_URL   = "http://127.0.0.1:4723"

def build_options(no_reset=True):
    opt = UiAutomator2Options()
    opt.platform_name          = "Android"
    opt.device_name            = "Android Device"
    opt.app_package            = APP_PACKAGE
    opt.app_activity           = APP_ACTIVITY
    opt.no_reset               = no_reset
    opt.auto_grant_permissions = True
    opt.new_command_timeout    = 300
    return opt

@pytest.fixture(scope="session")
def driver():
    log.info("Connecting to Appium...")
    drv = webdriver.Remote(command_executor=APPIUM_URL, options=build_options())
    time.sleep(5)
    sz = drv.get_window_size()
    log.info(f"App launched — screen {sz['width']}x{sz['height']}")
    yield drv
    drv.quit()
    log.info("Session closed")

def pytest_runtest_logreport(report):
    if report.when == "call":
        log.info(f"{'PASS' if report.passed else 'FAIL'} — {report.nodeid}")
