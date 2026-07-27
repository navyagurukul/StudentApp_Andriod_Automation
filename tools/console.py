"""Live AltTester console — connect the app via the free relay and inspect/drive
it, no AltTester Desktop or license needed.

It auto-starts the relay (utils/alt_connect.ensure_relay), sets up `adb reverse`,
launches the app, connects AltDriver, and then:
  * prints the connection info (scene, screen size, element count),
  * dumps the full object hierarchy to reports/hierarchy.md,
  * saves a screenshot to reports/inspect.png.

Modes:
    python tools/console.py            # one-shot snapshot (scene + tree + screenshot)
    python tools/console.py --watch    # keep polling the scene every 3s (Ctrl+C to stop)
    python tools/console.py --logs     # stream the app's AltTester logs (adb logcat)

The three live "log" surfaces:
  1. the RELAY log  — run `python tools/altserver_relay.py` in its own terminal to
     watch connections + every driver<->app message,
  2. this console   — scene + object hierarchy + screenshots,
  3. `--logs`       — the app's own AltTester/game logs from logcat.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import settings                       # noqa: E402
from utils.alt_connect import open_driver, close_driver  # noqa: E402


def dump_hierarchy(alt) -> Path:
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = settings.REPORTS_DIR / "hierarchy.md"
    lines = [f"# Object hierarchy — scene `{alt.get_current_scene()}`", "",
             "| Name | Text |", "|---|---|"]
    for e in alt.get_all_elements():
        name = (getattr(e, "name", "") or "").replace("|", "/")
        try:
            text = (e.get_text() or "").replace("|", "/").replace("\n", " ")[:50]
        except Exception:
            text = ""
        lines.append(f"| {name} | {text} |")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def stream_logs():
    """Stream the app's AltTester/Unity logs from logcat."""
    print("[inspect] streaming app logs (Ctrl+C to stop)...")
    adb = ["adb"] + (["-s", settings.UDID] if settings.UDID else [])
    subprocess.run(adb + ["logcat", "-c"])
    p = subprocess.Popen(adb + ["logcat", "-s", "Unity:*", "AltTester:*"],
                         stdout=subprocess.PIPE, text=True)
    try:
        for line in p.stdout:
            if any(k in line for k in ("AltTester", "Unity")):
                print(line.rstrip())
    except KeyboardInterrupt:
        pass
    finally:
        p.terminate()


def main():
    if "--logs" in sys.argv:
        stream_logs()
        return

    alt = open_driver()
    try:
        w, h = alt.get_application_screensize()
        els = alt.get_all_elements()
        print("=== AltTester live console ===")
        print(f"  host/port : {settings.ALT_HOST}:{settings.ALT_PORT}  (ws://…/altws)")
        print(f"  app name  : {settings.ALT_APP_NAME}")
        print(f"  scene     : {alt.get_current_scene()}")
        print(f"  screen    : {w}x{h}")
        print(f"  elements  : {len(els)}")

        tree = dump_hierarchy(alt)
        shot = settings.REPORTS_DIR / "inspect.png"
        alt.get_png_screenshot(str(shot))
        print(f"  hierarchy : {tree}")
        print(f"  screenshot: {shot}")

        if "--watch" in sys.argv:
            print("\n[inspect] watching scene (Ctrl+C to stop)...")
            last = None
            while True:
                sc = alt.get_current_scene()
                n = len(alt.get_all_elements())
                if sc != last:
                    print(f"  scene -> {sc}  ({n} elements)")
                    last = sc
                time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        close_driver(alt)


if __name__ == "__main__":
    main()
