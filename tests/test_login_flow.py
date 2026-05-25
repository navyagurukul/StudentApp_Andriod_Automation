"""
test_login_flow.py
FINAL STABLE VERSION
English Gurukul Student App Automation
"""

from appium.webdriver.webdriver import WebDriver
import sys
import os
import time
import pytest

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from pages.base_page import BasePage
from config.coordinates import get as C
from utils.logger import log, write_result
from utils.data_loader import load_users
from utils.permission_handler import PermissionHandler


# ─────────────────────────────────────────────
# SCREEN DETECTION
# ─────────────────────────────────────────────

def detect_screen(p):

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
# WAIT FOR SCREEN
# ─────────────────────────────────────────────

def wait_for_any_screen(p, expected_list, timeout=40):

    start = time.time()

    while time.time() - start < timeout:

        screen = detect_screen(p)

        log.info(f"[SCREEN] {screen}")

        if screen in expected_list:
            return screen

        time.sleep(1)

    raise AssertionError(
        f"Expected screens not found: {expected_list}"
    )


# ─────────────────────────────────────────────
# STRICT VALIDATION
# ─────────────────────────────────────────────

def require_screen(p, screen_name, timeout=20):

    log.info(f"VALIDATING SCREEN: {screen_name}")

    actual = wait_for_any_screen(
        p,
        [screen_name],
        timeout
    )

    if actual != screen_name:

        p.shot(f"FAILED_{screen_name}")

        raise AssertionError(
            f"Expected {screen_name}, got {actual}"
        )

    return True


# ─────────────────────────────────────────────
# MAIN TEST CLASS
# ─────────────────────────────────────────────

@pytest.mark.usefixtures("driver")
class TestLoginFlow:

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_all_users(self, driver: WebDriver):

        users = load_users()

        log.info(f"Total users: {len(users)}")

        for i, user in enumerate(users):

            mobile = user["mobileNumber"]

            log.info(
                f"\n===== USER {i+1}: {mobile} ====="
            )

            p = BasePage(driver)

            try:

                _run_user(p, user, i + 1)

                write_result(
                    mobile,
                    True,
                    "PASS"
                )

                log.info(f"PASS — {mobile}")

            except Exception as e:

                log.error(
                    f"FAILED — {mobile}: {e}"
                )

                p.shot(
                    f"FAILED_u{i+1}_{mobile}"
                )

                write_result(
                    mobile,
                    False,
                    str(e)
                )

            if i < len(users) - 1:

                p.restart_app()

        log.info("ALL USERS COMPLETED")


# ─────────────────────────────────────────────
# MAIN FLOW
# ─────────────────────────────────────────────

def _run_user(p: BasePage, user: dict, num: int):

    mobile = user["mobileNumber"]

    # ─────────────────────────────
    # PERMISSIONS
    # ─────────────────────────────

    PermissionHandler(
        p.driver
    ).handle_all_permissions()

    # ─────────────────────────────
    # LOGIN
    # ─────────────────────────────

    log.info("STEP 1: LOGIN")

    x, y = C("login", "mobile_input")

    p.tap_and_type(
        x,
        y,
        mobile,
        "mobile"
    )

    ox, oy = C("login", "ok_button")

    p.tap(ox, oy, "OK")

    cx, cy = C("login", "confirm_button")

    log.info("CLICK CONFIRM")

    p.tap(cx, cy, "CONFIRM")

    log.info(
        "Waiting for Unity transition..."
    )

    time.sleep(10)

    # ─────────────────────────────
    # DYNAMIC SCREEN DETECTION
    # UNITY SAFE
    # ─────────────────────────────

    log.info("Detecting next screen...")

    # LICENSE SCREEN
    

    time.sleep(5)

    if p.is_screen_visible("license_screen", timeout=5):
        next_screen = "license_screen"
    elif p.is_screen_visible("Select_Profile_screen", timeout=5):
        next_screen = "Select_Profile_screen"

    # SELECT PROFILE SCREEN

    elif p.pixel_exists(1120, 891):
        
        next_screen = "Select_Profile_screen"

    # AVATAR SCREEN

    elif p.pixel_exists(1158, 670):

        next_screen = "avatar_screen"

    # LANGUAGE SCREEN

    elif p.pixel_exists(1177, 905):

        next_screen = "language_screen"

    # OTHERWISE HOME

    else:

        next_screen = "home_screen"

    log.info(
        f"Detected next screen: {next_screen}"
    )

    # ─────────────────────────────
    # LICENSE FLOW
    # ─────────────────────────────

    if next_screen == "license_screen":

        log.info("LICENSE SCREEN")

        x, y = C("login", "mobile_input")

        p.tap_and_type(
            x,
            y,
            user.get("licenseCode", ""),
            "license"
        )

        cx, cy = C("login", "confirm_button")

        p.tap(cx, cy, "CONFIRM")

        time.sleep(5)

        # ───── REGISTRATION ─────

        log.info("REGISTRATION")

        p.tap_and_type(
            0.50,
            0.38,
            user.get("studentName", ""),
            "name"
        )

        gender = user.get(
            "studentGender",
            "Male"
        )

        p.tap(
            0.35 if gender == "Male" else 0.65,
            0.48,
            gender
        )

        p.tap_and_type(
            0.50,
            0.68,
            user.get(
                "studentParentName",
                ""
            ),
            "parent"
        )

        p.tap_and_type(
            0.50,
            0.76,
            str(
                user.get(
                    "studentAlternateMobileNumber",
                    ""
                )
            ),
            "alt mobile"
        )

        p.tap(0.50, 0.91, "submit")

        time.sleep(10)

        next_screen = "Select_Profile_screen"

    # ─────────────────────────────
    # SELECT PROFILE
    # ─────────────────────────────

    if next_screen == "Select_Profile_screen":

        log.info("SELECT PROFILE")

        idx = user.get(
            "profileIndex",
            1
        )

        try:

            px, py = C(
                "select_profile",
                f"profile_{idx}"
            )

        except:

            px, py = C(
                "select_profile",
                "profile_1"
            )

        p.tap(px, py, "profile")

        nx, ny = C(
            "select_profile",
            "next_button"
        )

        p.tap(nx, ny, "NEXT")

        time.sleep(5)

        next_screen = "avatar_screen"

    # ─────────────────────────────
    # AVATAR
    # ─────────────────────────────

    if next_screen == "avatar_screen":

        log.info("AVATAR")

        sx, sy = C(
            "select_avatar",
            "save_button"
        )

        p.tap(sx, sy, "SAVE")

        time.sleep(5)

        next_screen = "language_screen"

    # ─────────────────────────────
    # LANGUAGE
    # ─────────────────────────────

    if next_screen == "language_screen":

        log.info("LANGUAGE")

        dx, dy = C(
            "language_dialog",
            "dropdown"
        )

        p.tap(dx, dy, "dropdown")

        idx = user.get(
            "studentLanguageIndex",
            0
        )

        try:

            ox, oy = C(
                "language_dialog",
                f"option_{idx}"
            )

        except:

            ox, oy = C(
                "language_dialog",
                "option_0"
            )

        p.tap(ox, oy, "language")

        sx, sy = C(
            "language_dialog",
            "save_button"
        )

        p.tap(sx, sy, "SAVE")

        time.sleep(5)

    # ─────────────────────────────
    # POPUPS
    # ─────────────────────────────

    log.info("HANDLING POPUPS")

    try:

        x, y = C(
            "begin_scene",
            "skip_button"
        )

        log.info("Clicking SKIP")

        p.tap(x, y, "SKIP")

        time.sleep(5)

    except Exception as e:

        log.info(
            f"Skip not found: {e}"
        )

    try:

        x, y = C(
            "streak_popup",
            "close_btn"
        )

        log.info(
            "Closing STREAK popup"
        )

        p.tap(
            x,
            y,
            "CLOSE STREAK"
        )

        time.sleep(4)

    except Exception as e:

        log.info(
            f"Streak popup not found: {e}"
        )

    try:

        x, y = C(
            "welcome_back",
            "continue_btn"
        )

        log.info(
            "Clicking CONTINUE"
        )

        p.tap(
            x,
            y,
            "CONTINUE"
        )

        time.sleep(4)

    except Exception as e:

        log.info(
            f"Welcome popup not found: {e}"
        )

    try:

        x, y = C(
            "test_popup",
            "later_btn"
        )

        log.info("Clicking LATER")

        p.tap(x, y, "LATER")

        time.sleep(4)

    except Exception as e:

        log.info(
            f"Test popup not found: {e}"
        )

    log.info("POPUP FLOW COMPLETE")

    # ─────────────────────────────
    # HOME WAIT
    # ─────────────────────────────

    time.sleep(5)

    # ─────────────────────────────
    # LOGOUT
    # ─────────────────────────────

    log.info("LOGOUT")

    hx, hy = C(
        "home_screen",
        "parents_icon"
    )

    p.tap(hx, hy, "parents")

    time.sleep(3)

    lx, ly = C(
        "parents_corner",
        "logout_button"
    )

    p.tap(lx, ly, "logout")

    time.sleep(5)

    write_result(
        user["mobileNumber"],
        True,
        "Logout done"
    )

    log.info("LOGOUT SUCCESS")