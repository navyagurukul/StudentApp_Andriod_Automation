"""
base_page.py
FINAL STABLE VERSION STRICT UI VALIDATION
"""

import os
import time
import io
import subprocess
import PIL.Image

from utils.logger import log


class BasePage:

    SS_DIR = "screenshots"

    # ─────────────────────────────────────────────
    # INIT
    # ─────────────────────────────────────────────

    def __init__(self, driver):

        self.driver = driver

        size = driver.get_window_size()

        self.W = size["width"]
        self.H = size["height"]

        log.info(f"Screen size detected: {self.W} x {self.H}")

        os.makedirs(self.SS_DIR, exist_ok=True)

    # ─────────────────────────────────────────────
    # SCREENSHOT
    # ─────────────────────────────────────────────

    def shot(self, name):

        path = f"{self.SS_DIR}/{name}_{int(time.time())}.png"

        self.driver.save_screenshot(path)

        log.info(f"Screenshot: {path}")

        return path

    # ─────────────────────────────────────────────
    # TAP
    # ─────────────────────────────────────────────

    def tap(self, x, y, label=""):

        if isinstance(x, float):
            x = int(self.W * x)

        if isinstance(y, float):
            y = int(self.H * y)

        log.info(f"Tap [{label}] at ({x},{y})")

        subprocess.run(
            ["adb", "shell", "input", "tap", str(x), str(y)],
            capture_output=True
        )

        time.sleep(1)

    # ─────────────────────────────────────────────
    # TYPE
    # ─────────────────────────────────────────────

    def tap_and_type(self, x, y, text, label=""):

        self.tap(x, y, label)

        time.sleep(1)

        self._adb_clear()

        self._adb_type(text)

        log.info(f"Typed [{text}] into [{label}]")

        time.sleep(1)

    # ─────────────────────────────────────────────
    # CLEAR
    # ─────────────────────────────────────────────

    def _adb_clear(self):

        for _ in range(20):

            subprocess.run(
                ["adb", "shell", "input", "keyevent", "67"],
                capture_output=True
            )

            time.sleep(0.03)

    # ─────────────────────────────────────────────
    # TYPE TEXT
    # ─────────────────────────────────────────────

    def _adb_type(self, text):

        safe = (
            str(text)
            .replace("\\", "\\\\")
            .replace(" ", "%s")
            .replace("'", "\\'")
        )

        subprocess.run(
            ["adb", "shell", "input", "text", safe],
            capture_output=True
        )

    # ─────────────────────────────────────────────
    # WAIT
    # ─────────────────────────────────────────────

    def wait(self, secs, reason=""):

        if reason:
            log.info(f"Waiting {secs}s — {reason}")

        time.sleep(secs)

    # ─────────────────────────────────────────────
    # SAFE TAP
    # ─────────────────────────────────────────────

    def try_tap(self, x, y, label=""):

        try:
            self.tap(x, y, label)
            return True

        except Exception as e:

            log.info(f"try_tap failed [{label}] : {e}")

            return False

    # ─────────────────────────────────────────────
    # APP RESTART
    # ─────────────────────────────────────────────

    def restart_app(self):

        pkg = "com.OritSciencesPrivateLimited.EnglishGurukul.studentapp"

        log.info("Restarting app...")

        self.driver.terminate_app(pkg)

        time.sleep(2)

        self.driver.activate_app(pkg)

        time.sleep(8)

        log.info("App restarted")

    # ─────────────────────────────────────────────
    # PIXEL CHECK
    # ─────────────────────────────────────────────

    def pixel_exists(self, x, y):

        try:

            if isinstance(x, float):
                x = int(self.W * x)

            if isinstance(y, float):
                y = int(self.H * y)

            img = self.driver.get_screenshot_as_png()

            image = PIL.Image.open(io.BytesIO(img))

            pixel = image.getpixel((x, y))

            return pixel != (0, 0, 0)

        except Exception as e:

            log.error(f"Pixel check failed: {e}")

            return False

    # ─────────────────────────────────────────────
    # SCREEN DETECTION
    # ─────────────────────────────────────────────

    def get_current_screen(self):

        try:

            # LOGIN
            if (
                self.pixel_exists(1142, 465)
                and self.pixel_exists(2166, 442)
                and self.pixel_exists(1203, 694)
            ):
                return "login_screen"

            # SELECT PROFILE
            if (
                self.pixel_exists(1120, 891)
                and self.pixel_exists(1430, 586)
            ):
                return "Select_Profile_screen"

            # AVATAR
            if (
                self.pixel_exists(1158, 670)
                and self.pixel_exists(1252, 497)
            ):
                return "avatar_screen"

            # LANGUAGE
            if self.pixel_exists(1177, 905):
                return "language_screen"

            # BEGIN SCENE
            if self.pixel_exists(1992, 938):
                return "begin_scene"

            # HOME
            if (
                self.pixel_exists(323, 108)
                and self.pixel_exists(2105, 108)
            ):
                return "home_screen"

            # LICENSE
            if self.pixel_exists(1203, 694):
                return "license_screen"

            return "unknown"

        except Exception as e:

            log.error(f"Screen detect error: {e}")

            return "unknown"

    # ─────────────────────────────────────────────
    # EXISTS
    # ─────────────────────────────────────────────

    def exists(self, screen_name):

        return self.get_current_screen() == screen_name

    # ─────────────────────────────────────────────
    # STRICT SCREEN CHECKER
    # ─────────────────────────────────────────────

    def is_screen_visible(self, screen_name, timeout=15):

        log.info(f"Looking for screen: {screen_name}")

        start = time.time()

        while time.time() - start < timeout:

            current = self.get_current_screen()

            log.info(f"Current screen detected: {current}")

            if current == screen_name:

                log.info(f"Screen detected: {screen_name}")

                return True

            time.sleep(1)

        log.error(f"Screen NOT found: {screen_name}")

        return False