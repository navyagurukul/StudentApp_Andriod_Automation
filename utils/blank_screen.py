"""Blank-screen detection + reporting.

The Student app sometimes shows a blank/unresponsive screen. Per QA policy we
don't just fail — we capture evidence (screenshot, logcat, scene + element count,
and where it happened) into reports/blank_screens/ so the app team can act on it.
"""
from __future__ import annotations

import datetime
import shutil
import subprocess
from pathlib import Path

from config import settings

OUT = settings.REPORTS_DIR / "blank_screens"


def _ts() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def _adb(*args) -> str:
    adb = shutil.which("adb") or "adb"
    base = [adb]
    if settings.UDID:
        base += ["-s", settings.UDID]
    try:
        out = subprocess.run(base + list(args), capture_output=True, text=True, timeout=30)
        return (out.stdout or "") + (out.stderr or "")
    except Exception as exc:
        return f"(adb failed: {exc})"


def looks_blank(alt, min_elements: int = 4) -> bool:
    """Blank if the driver returns almost no UI elements, or can't respond."""
    try:
        return len(alt.get_all_elements()) < min_elements
    except Exception:
        return True  # unresponsive == effectively blank


def report(where: str, alt=None, reason: str = "") -> Path:
    """Capture evidence of a blank/unresponsive screen and write a report."""
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = _ts()
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in where)[:60]
    png = OUT / f"blank_{safe}_{stamp}.png"
    md = OUT / f"blank_{safe}_{stamp}.md"

    # screenshot (adb is reliable even when the driver is stuck)
    _adb("exec-out", "screencap", "-p")  # warm up
    try:
        raw = subprocess.run(
            ([shutil.which("adb") or "adb"] + (["-s", settings.UDID] if settings.UDID else []) +
             ["exec-out", "screencap", "-p"]),
            capture_output=True, timeout=30,
        ).stdout
        png.write_bytes(raw)
    except Exception:
        png = None  # noqa

    scene = elements = "(driver unavailable)"
    if alt is not None:
        try:
            scene = alt.get_current_scene()
        except Exception as exc:
            scene = f"(get_current_scene failed: {type(exc).__name__})"
        try:
            elements = str(len(alt.get_all_elements()))
        except Exception as exc:
            elements = f"(get_all_elements failed: {type(exc).__name__})"

    logcat = _adb("logcat", "-d", "-t", "400")
    errs = [l for l in logcat.splitlines()
            if any(k in l for k in (" E ", "Exception", "error", "Error", "ANR", "Unity"))][-60:]

    lines = [
        f"# Blank / unresponsive screen — {where}", "",
        f"- When: **{stamp}**",
        f"- Reason: {reason or 'blank screen detected'}",
        f"- Scene: `{scene}`",
        f"- Element count: {elements}",
        f"- Screenshot: `{png.name if png else '(failed)'}`",
        "", "## Recent logcat (errors / Unity, last ~60)", "```",
        *errs, "```",
    ]
    md.write_text("\n".join(lines), encoding="utf-8")
    print(f"[blank-screen] reported at '{where}' -> {md}")
    return md
