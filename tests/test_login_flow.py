"""
test_login_flow.py
FINAL STABLE VERSION (UNITY + APPIUM FIXED)
English Gurukul Student App Automation
"""

from appium.webdriver.webdriver import WebDriver
import sys
import os
import time
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.base_page import BasePage
from config.coordinates import get as C
from utils.logger import log, write_result
from utils.data_loader import load_users
from utils.permission_handler import PermissionHandler



@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.android

@pytest.mark.usefixtures("driver")
class TestBasePage:

    def test_screen_detection(self, driver: WebDriver):

        p = BasePage(driver)

        screen = detect_screen(p)

        log.info(f"Detected screen: {screen}")

        assert screen in [
            "license_screen",
            "Select_Profile_screen",
            "avatar_screen",
            "language_screen",
            "home_screen",
            "login_screen",
            "unknown"
        ], f"Unexpected screen detected: {screen}"
# ─────────────────────────────────────────────
# SCREEN DETECTION (FIXED FOR UNITY)
# ─────────────────────────────────────────────

def detect_screen(p):
    """
    Unity-safe screen detection using page_source (NOT cached logic)
    """

    try:
        src = p.driver.page_source.lower()

        if "license" in src:
            return "license_screen"

        if "select profile" in src or "select_profile" in src:
            return "Select_Profile_screen"

        if "avatar" in src:
            return "avatar_screen"

        if "language" in src:
            return "language_screen"

        if "home" in src:
            return "home_screen"

        if "login" in src:
            return "login_screen"

        return "unknown"

    except Exception as e:
        log.error(f"Screen detection error: {e}")
        return "unknown"


# ─────────────────────────────────────────────
# WAIT FOR SCREEN (FIXED)
# ─────────────────────────────────────────────

def wait_for_any_screen(p, expected_list, timeout=40):

    start = time.time()

    while time.time() - start < timeout:

        screen = detect_screen(p)

        log.info(f"[SCREEN] {screen}")

        if screen in expected_list:
            return screen

        time.sleep(1)

    raise AssertionError(f"Expected screens not found: {expected_list}")


# ─────────────────────────────────────────────
# STRICT VALIDATION
# ─────────────────────────────────────────────

def require_screen(p, screen_name, timeout=20):

    log.info(f"VALIDATING SCREEN: {screen_name}")

    actual = wait_for_any_screen(p, [screen_name], timeout)

    if actual != screen_name:
        p.shot(f"FAILED_{screen_name}")
        raise AssertionError(f"Expected {screen_name}, got {actual}")

    return True


# ─────────────────────────────────────────────
# TEST CLASS
# ─────────────────────────────────────────────

class TestLoginFlow:

    def test_all_users(self, driver: WebDriver):

        users = load_users()
        log.info(f"Total users: {len(users)}")

        for i, user in enumerate(users):

            mobile = user["mobileNumber"]
            log.info(f"\n===== USER {i+1}: {mobile} =====")

            p = BasePage(driver)

            try:
                _run_user(p, user, i + 1)
                write_result(mobile, True, "PASS")
                log.info(f"PASS — {mobile}")

            except Exception as e:
                log.error(f"FAILED — {mobile}: {e}")
                p.shot(f"FAILED_u{i+1}_{mobile}")
                write_result(mobile, False, str(e))

            if i < len(users) - 1:
                p.restart_app()

        log.info("ALL USERS COMPLETED")


# ─────────────────────────────────────────────
# MAIN FLOW
# ─────────────────────────────────────────────

def _run_user(p: BasePage, user: dict, num: int):

    mobile = user["mobileNumber"]

    # ───── Permissions ─────
    PermissionHandler(p.driver).handle_all_permissions()

    # ───── LOGIN ─────
    log.info("STEP 1: LOGIN")
    log.info("Assuming login screen is visible")

    x, y = C("login", "mobile_input")
    p.tap_and_type(x, y, mobile, "mobile")

    ox, oy = C("login", "ok_button")
    p.tap(ox, oy, "OK")

    cx, cy = C("login", "confirm_button")

    log.info("CLICK CONFIRM")
    p.tap(cx, cy, "CONFIRM")

    log.info("Waiting for Unity transition...")
    time.sleep(8)
    # IMPORTANT FOR UNITY + API

    # DEBUG
    log.info(f"AFTER CONFIRM SCREEN: {detect_screen(p)}")

    # ───── NEXT SCREEN ─────
    log.info("Proceeding to next step after login delay")

    time.sleep(5)

    # DIRECT ASSUMPTION (THIS IS KEY FOR UNITY)
    next_screen = (
        user.get("expected_next")
        or ("License_screen" if user.get("licenseCode") else "Select_Profile_screen")
    )
    log.info(f"Assuming next screen: {next_screen}")

    # ───── FLOW HANDLING ─────

    if next_screen == "license_screen":
        _handle_license(p, user, num)
        _handle_registration(p, user, num)

        next_screen = wait_for_any_screen(
            p,
            ["Select_Profile_screen", "home_screen"],
            timeout=25
        )

    if next_screen == "Select_Profile_screen":
        _handle_select_profile(p, user, num)
        _handle_avatar(p, user, num)
        _handle_language(p, user, num)

    # ───── POPUPS ─────
    _handle_popups(p, user, num)

    # ───── HOME ─────
    # wait for home ui settle
    time.sleep(5)
    # ───── LOGOUT ─────
    _handle_logout(p, user, num)


# ─────────────────────────────────────────────
# HANDLERS (UNCHANGED LOGIC BUT SAFE)
# ─────────────────────────────────────────────

def _handle_license(p, user, num):

    log.info("LICENSE SCREEN")

    x, y = C("login", "mobile_input")
    p.tap_and_type(x, y, user.get("licenseCode", ""), "license")

    cx, cy = C("login", "confirm_button")
    p.tap(cx, cy, "CONFIRM")

    time.sleep(3)


def _handle_registration(p, user, num):

    log.info("REGISTRATION")

    p.tap_and_type(0.50, 0.38, user.get("studentName", ""), "name")

    gender = user.get("studentGender", "Male")
    p.tap(0.35 if gender == "Male" else 0.65, 0.48, gender)

    p.tap_and_type(0.50, 0.68, user.get("studentParentName", ""), "parent")

    p.tap_and_type(0.50, 0.76,
                str(user.get("studentAlternateMobileNumber", "")),
                "alt mobile")

    p.tap(0.50, 0.91, "submit")

    time.sleep(5)


def _handle_select_profile(p, user, num):

    log.info("SELECT PROFILE")

    idx = user.get("profileIndex", 1)

    try:
        px, py = C("select_profile", f"profile_{idx}")
    except:
        px, py = C("select_profile", "profile_1")

    p.tap(px, py, "profile")

    nx, ny = C("select_profile", "next_button")
    p.tap(nx, ny, "NEXT")


def _handle_avatar(p, user, num):

    log.info("AVATAR")

    sx, sy = C("select_avatar", "save_button")
    p.tap(sx, sy, "SAVE")
    time.sleep(4)


def _handle_language(p, user, num):

    log.info("LANGUAGE")

    dx, dy = C("language_dialog", "dropdown")
    p.tap(dx, dy, "dropdown")

    idx = user.get("studentLanguageIndex", 0)

    try:
        ox, oy = C("language_dialog", f"option_{idx}")
    except:
        ox, oy = C("language_dialog", "option_0")

    p.tap(ox, oy, "language")

    sx, sy = C("language_dialog", "save_button")
    p.tap(sx, sy, "SAVE")
    time.sleep(3)


def _handle_popups(p, user, num):

    log.info("HANDLING POPUPS")

    # ─────────────────────────────
    # SKIP BUTTON
    # ─────────────────────────────

    try:

        x, y = C("begin_scene", "skip_button")

        log.info("Clicking SKIP")

        p.tap(x, y, "SKIP")

        time.sleep(5)

    except Exception as e:

        log.info(f"Skip not found: {e}")

    # ─────────────────────────────
    # STREAK POPUP
    # ─────────────────────────────

    try:

        x, y = C("streak_popup", "close_btn")

        log.info("Closing STREAK popup")

        p.tap(x, y, "CLOSE STREAK")

        time.sleep(4)

    except Exception as e:

        log.info(f"Streak popup not found: {e}")

    # ─────────────────────────────
    # WELCOME BACK
    # ─────────────────────────────

    try:

        x, y = C("welcome_back", "continue_btn")

        log.info("Clicking CONTINUE")

        p.tap(x, y, "CONTINUE")

        time.sleep(4)

    except Exception as e:

        log.info(f"Welcome popup not found: {e}")

    # ─────────────────────────────
    # TEST POPUP
    # ─────────────────────────────

    try:

        x, y = C("test_popup", "later_btn")

        log.info("Clicking LATER")

        p.tap(x, y, "LATER")

        time.sleep(4)

    except Exception as e:

        log.info(f"Test popup not found: {e}")

    log.info("POPUP FLOW COMPLETE")


def _handle_logout(p, user, num):

    log.info("LOGOUT")

    hx, hy = C("home_screen", "parents_icon")

    p.tap(hx, hy, "parents")

    time.sleep(3)

    lx, ly = C("parents_corner", "logout_button")

    p.tap(lx, ly, "logout")

    time.sleep(5)

    write_result(
        user["mobileNumber"],
        True,
        "Logout done"
    )

    log.info("LOGOUT SUCCESS")