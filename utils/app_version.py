"""Resolve the Student app version for the daily report header (e.g. V4.0.0.2).

Resolution order (first hit wins):
  1. a live AltDriver reading UnityEngine.Application.version (truest — what the
     running build reports), when a driver is passed;
  2. APP_VERSION env / .env override;
  3. the installed build via `adb shell dumpsys package <pkg>` -> versionName;
  4. the APK via `aapt dump badging`, if APK_PATH is set;
  5. "unknown".
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess

from config import settings


def _run(cmd) -> str:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return (out.stdout or "") + (out.stderr or "")
    except Exception:
        return ""


def from_live(alt) -> str | None:
    """Read Application.version from the running Unity app via AltDriver."""
    if alt is None:
        return None
    try:
        v = alt.get_static_property(
            "UnityEngine.Application", "version", "UnityEngine.CoreModule"
        )
        return str(v).strip() or None
    except Exception:
        return None


def _from_env():
    v = os.getenv("APP_VERSION", "").strip()
    return v or None


def _from_device():
    adb = shutil.which("adb")
    if not adb:
        return None
    cmd = [adb]
    if settings.UDID:
        cmd += ["-s", settings.UDID]
    out = _run(cmd + ["shell", "dumpsys", "package", settings.APP_PACKAGE])
    m = re.search(r"versionName=([0-9][0-9A-Za-z.\-+]*)", out)
    return m.group(1) if m else None


def _from_apk():
    apk = os.getenv("APK_PATH", "").strip()
    if not apk or not os.path.isfile(apk):
        return None
    tool = shutil.which("aapt") or shutil.which("aapt2")
    if not tool:
        return None
    m = re.search(r"versionName='([^']+)'", _run([tool, "dump", "badging", apk]))
    return m.group(1) if m else None


def resolve(alt=None) -> str | None:
    for source in (lambda: from_live(alt), _from_env, _from_device, _from_apk):
        try:
            v = source()
        except Exception:
            v = None
        if v:
            return v
    return None


def label(alt=None) -> str:
    v = resolve(alt)
    return f"V{v}" if v else "unknown"
