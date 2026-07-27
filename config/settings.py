"""Central configuration for the Student-app AltTester suite, env-driven with safe
defaults. Import from here — nothing else should read os.environ directly.

The app is a Unity build instrumented with the AltTester SDK (2.3.1, GPL). It runs
as a client that connects OUT to an AltServer broker at ALT_HOST:ALT_PORT. Over
USB that means: `adb reverse tcp:13000 tcp:13000` + an AltServer listening on the
host. See README for the license/broker note.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


def _bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes"}


# --- AltTester connection -----------------------------------------------------
# The app connects to the AltServer at this address; the driver connects here too.
ALT_HOST = os.getenv("ALT_HOST", "127.0.0.1")
ALT_PORT = int(os.getenv("ALT_PORT", "13000"))
# AltServer app name the RUNNING app registers with. The installed build uses
# "__default__" (verified live — the editor asset's "EnglishGurukulStudentApp" is
# not what the shipped APK actually registers). Override via ALT_APP_NAME if a
# future build changes it (check the AltTester popup on the device).
ALT_APP_NAME = os.getenv("ALT_APP_NAME", "__default__")
CONNECT_TIMEOUT = int(os.getenv("ALT_CONNECT_TIMEOUT", "30"))

# --- device / app under test --------------------------------------------------
APP_PACKAGE = os.getenv("APP_PACKAGE", "com.OritSciencesPrivateLimited.EnglishGurukul.student")
# Unity apps launch through Branch's activity in this build.
APP_ACTIVITY = os.getenv("APP_ACTIVITY", "io.branch.unity.BranchUnityActivity")
UDID = os.getenv("UDID", "").strip()  # pin a device when several are attached (adb devices)

# Set up `adb reverse` and launch the app automatically when opening the driver.
REVERSE_FORWARD = _bool("REVERSE_FORWARD", True)
LAUNCH_APP = _bool("LAUNCH_APP", True)

REPORTS_DIR = ROOT / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
