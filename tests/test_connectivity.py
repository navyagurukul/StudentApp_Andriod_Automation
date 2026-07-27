"""Connectivity smoke: prove the AltServer/app link is healthy and capture a
baseline. These pass as soon as a broker is up and the app is instrumented — no
UI selectors required — so they're the first thing to run end-to-end.

As a side effect they write the scene dump + app version into reports/, which is
what you use to build the real screen objects/tests.
"""
import pytest

from config import settings
from utils import app_version, scene_dump


@pytest.mark.smoke
@pytest.mark.connectivity
def test_connected_and_scene_loaded(alt):
    scene = alt.get_current_scene()
    assert scene, "AltDriver connected but no active scene was reported"

    elements = alt.get_all_elements()
    assert elements, "scene is loaded but no UI elements were returned"

    # Capture the live version (Application.version) for the daily report header.
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    version = app_version.resolve(alt) or "unknown"
    (settings.REPORTS_DIR / "app_version.txt").write_text(version, encoding="utf-8")

    # Snapshot the scene so selectors can be built from a real hierarchy.
    scene_dump.dump(alt, settings.REPORTS_DIR)


@pytest.mark.smoke
@pytest.mark.connectivity
def test_screenshot_and_screensize(alt):
    w, h = alt.get_application_screensize()
    assert w > 0 and h > 0, f"implausible screen size {w}x{h}"
    settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    alt.get_png_screenshot(str(settings.SCREENSHOTS_DIR / "connectivity.png"))
