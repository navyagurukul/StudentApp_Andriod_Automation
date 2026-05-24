"""
conftest.py — Appium session for English Gurukul student app.
Works with installed APK on real Android device.

Before running:
    Terminal 1:
        appium --port 4723

    Terminal 2:
        adb devices
        pytest tests/test_login_flow.py -v -s
"""

import pytest
import time

from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options

from utils.logger import log


APP_PACKAGE = "com.OritSciencesPrivateLimited.EnglishGurukul.studentapp"
APP_ACTIVITY = "io.branch.unity.BranchUnityActivity"

APPIUM_URL = "http://127.0.0.1:4723"

DEVICE_ID = "7245d3d80508"


def build_options(no_reset=True):

    opt = UiAutomator2Options()

    # =====================================================
    # Platform
    # =====================================================
    opt.platform_name = "Android"

    # =====================================================
    # Real Device
    # =====================================================
    opt.device_name = "Android_Device"
    opt.udid = DEVICE_ID

    # =====================================================
    # Automation
    # =====================================================
    opt.automation_name = "UiAutomator2"

    # =====================================================
    # App
    # =====================================================
    opt.app_package = APP_PACKAGE
    opt.app_activity = APP_ACTIVITY

    # =====================================================
    # Session
    # =====================================================
    opt.no_reset = no_reset
    opt.full_reset = False

    opt.auto_grant_permissions = True
    opt.new_command_timeout = 300

    return opt


@pytest.fixture(scope="session")
def driver():

    log.info("Connecting to Appium...")

    drv = webdriver.Remote(
        command_executor=APPIUM_URL,
        options=build_options()
    )

    time.sleep(5)

    sz = drv.get_window_size()

    log.info(f"App launched — screen {sz['width']}x{sz['height']}")

    yield drv

    drv.quit()

    log.info("Session closed")


def pytest_runtest_logreport(report):

    if report.when == "call":

        log.info(
            f"{'PASS' if report.passed else 'FAIL'} — {report.nodeid}"
        )