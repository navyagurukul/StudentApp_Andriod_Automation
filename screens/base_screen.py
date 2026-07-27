"""Base screen object over AltDriver.

Unity UI text usually surfaces as an object whose NAME is a stable widget id and
whose TEXT is the visible label. These helpers prefer matching by visible TEXT
(what a tester sees) with a NAME fallback, and centralise the waits so screen
objects stay declarative — mirroring the teacher-app Page Object style.

Selector note: the exact names/text below the base class are placeholders until
the live scene is inspected (run tools/discover.py -> reports/scene_dump.md).
"""
from __future__ import annotations

from alttester import AltDriver, By
from alttester.exceptions import WaitTimeOutException


class BaseScreen:
    def __init__(self, alt: AltDriver):
        self.alt = alt

    # -- lookups ---------------------------------------------------------------

    def find_by_text(self, text: str, timeout: int = 15):
        return self.alt.wait_for_object_which_contains(
            By.TEXT, text, timeout=timeout
        )

    def find_by_name(self, name: str, timeout: int = 15):
        return self.alt.wait_for_object(By.NAME, name, timeout=timeout)

    def has_text(self, text: str, timeout: int = 5) -> bool:
        try:
            self.alt.wait_for_object_which_contains(By.TEXT, text, timeout=timeout)
            return True
        except WaitTimeOutException:
            return False

    def has_name(self, name: str, timeout: int = 5) -> bool:
        try:
            self.alt.wait_for_object(By.NAME, name, timeout=timeout)
            return True
        except WaitTimeOutException:
            return False

    # -- actions ---------------------------------------------------------------

    def tap_text(self, text: str, timeout: int = 15):
        el = self.find_by_text(text, timeout=timeout)
        el.tap()
        return el

    def tap_name(self, name: str, timeout: int = 15):
        el = self.find_by_name(name, timeout=timeout)
        el.tap()
        return el

    def type_into(self, name: str, value: str, timeout: int = 15):
        el = self.find_by_name(name, timeout=timeout)
        el.set_text(value)
        return el

    # -- scene -----------------------------------------------------------------

    def current_scene(self) -> str:
        return self.alt.get_current_scene()

    def wait_scene(self, scene_name: str, timeout: int = 20):
        self.alt.wait_for_current_scene_to_be(scene_name, timeout=timeout)
        return self
