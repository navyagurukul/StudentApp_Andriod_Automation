"""
screen_detector.py
==================
Takes a screenshot and saves it so you can SEE what's on screen.
Also provides a manual + automatic detection flow.

Since Unity has no element tree, we detect screens by:
  1. Taking a screenshot after each action
  2. Waiting known amounts of time for each screen
  3. Using the user data to know which path to take

HOW TO USE AFTER FIRST RUN:
  Open logs/screenshots/ folder
  Look at the screenshots to find exact button positions
  Update config/screen_coords.py with pixel positions
"""

import os
import time
import subprocess
from utils.logger import log


class ScreenDetector:

    def __init__(self, driver, W: int, H: int):
        self.driver = driver
        self.W = W
        self.H = H

    def capture_and_save(self, label: str) -> str:
        """Take screenshot and save. Returns file path."""
        os.makedirs("logs/screenshots", exist_ok=True)
        path = f"logs/screenshots/{label}_{int(time.time())}.png"
        self.driver.save_screenshot(path)
        log.info(f"📸 Saved: {path}")
        return path

    def pull_screenshot_via_adb(self, label: str) -> str:
        """Alternative: capture via ADB directly."""
        remote = f"/sdcard/{label}.png"
        local  = f"logs/screenshots/{label}_{int(time.time())}.png"
        subprocess.run(["adb", "shell", "screencap", "-p", remote], capture_output=True)
        subprocess.run(["adb", "pull", remote, local], capture_output=True)
        subprocess.run(["adb", "shell", "rm", remote], capture_output=True)
        log.info(f"📸 ADB screenshot: {local}")
        return local

    def wait_and_capture(self, wait_seconds: float, label: str) -> str:
        """Wait then capture — use after clicking buttons."""
        log.info(f"Waiting {wait_seconds}s then capturing '{label}'...")
        time.sleep(wait_seconds)
        return self.capture_and_save(label)

    def detect_after_login(self, wait: float = 15) -> str:
        """
        PURE DEBUG TOOL — NOT LOGIC DECISION
        Only captures screen after login.
        """

        log.info(f"Waiting {wait}s for screen after login...")
        time.sleep(wait)

        path = self.capture_and_save("after_login_detect")

        log.info(f"📸 Saved login state screenshot: {path}")

        return "unknown"