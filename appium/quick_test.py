"""
quick_test.py — Run this FIRST to confirm Appium connects.
    python quick_test.py
"""
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
import time

opt = UiAutomator2Options()
opt.platform_name          = "Android"
opt.device_name            = "Android Device"
opt.app_package            = "com.OritSciencesPrivateLimited.EnglishGurukul.studentapp"
opt.app_activity           = "io.branch.unity.BranchUnityActivity"
opt.no_reset               = True
opt.auto_grant_permissions = True

try:
    print("Connecting to Appium...")
    driver = webdriver.Remote("http://127.0.0.1:4723", options=opt)
    time.sleep(4)
    sz = driver.get_window_size()
    print(f"Connected! Screen: {sz['width']} x {sz['height']}")
    driver.save_screenshot("quick_test_screenshot.png")
    print("Screenshot saved: quick_test_screenshot.png")
    driver.quit()
    print("DONE — Appium is working correctly.")
except Exception as e:
    print(f"FAILED: {e}")
    print()
    print("Checklist:")
    print("  1. Is Appium running?  appium --port 4723")
    print("  2. Is device connected?  adb devices")
    print("  3. Is port forwarded?  adb forward tcp:4723 tcp:4723")
    print("  4. Is app installed?  adb shell pm list packages | findstr gurukul")
