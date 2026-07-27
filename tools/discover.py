"""Selector-discovery tool. Run this FIRST once an AltServer is up and the app is
on the Pixel — it connects, dumps the live scene (names/text/paths) and a
screenshot to reports/, and prints the app version. Use reports/scene_dump.md to
fill in the real selectors in screens/*.py, then flesh out the tests.

    python tools/discover.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import settings          # noqa: E402
from utils import app_version, scene_dump  # noqa: E402
from utils.alt_connect import open_driver, close_driver  # noqa: E402


def main():
    try:
        alt = open_driver()
    except ConnectionError as exc:
        print(f"[discover] {exc}")
        sys.exit(2)

    try:
        print("[discover] connected.")
        print("  app version :", app_version.label(alt))
        print("  scene       :", alt.get_current_scene())
        md = scene_dump.dump(alt, settings.REPORTS_DIR)
        els = alt.get_all_elements()
        print(f"  elements    : {len(els)}")
        print(f"  wrote       : {md}")
        print(f"  screenshot  : {settings.REPORTS_DIR / 'scene.png'}")
        print("\nNext: open reports/scene_dump.md, copy the real names/text into "
              "screens/login_screen.py + home_screen.py, then remove the skips in tests/.")
    finally:
        close_driver(alt)


if __name__ == "__main__":
    main()
