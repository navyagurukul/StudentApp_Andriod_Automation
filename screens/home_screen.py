"""Home / dashboard (Unity scene 'ParentsScreen') — the hub after login.

Content areas are text buttons: Fun Learn, Stories, Games, Word Fun, Tests.
Back to home from any area is the 'BackBtn' GameObject (a back-arrow icon).

Per QA rule: if the "take a test" assessment popup appears, tap **Later**
(never Take Test) and continue with the intended navigation.
"""
from __future__ import annotations

import time

from alttester import By

from screens.base_screen import BaseScreen


class S:
    STORIES = "Stories"
    WORD_FUN = "Word Fun"
    TESTS = "Tests"
    FUN_LEARN = "Fun Learn"
    GAMES = "Games"
    BACK_BTN = "BackBtn"          # By.NAME — back-arrow icon
    ASSESSMENT_LATER = "Later"    # dismiss the assessment/take-a-test popup


class HomeScreen(BaseScreen):
    def is_loaded(self, timeout: int = 20) -> bool:
        return self.has_text(S.WORD_FUN, timeout=timeout) and self.has_text(S.STORIES, timeout=3)

    def dismiss_assessment_popup(self):
        """If the assessment 'take a test' popup is showing, click Later.
        Defensive: the popup can vanish between the check and the tap."""
        try:
            if self.has_text(S.ASSESSMENT_LATER, timeout=2):
                self.tap_text(S.ASSESSMENT_LATER)
                time.sleep(1)
        except Exception:
            pass
        return self

    def ensure_home(self, tries: int = 8):
        """Get to the home hub from wherever we are (sub-screen, Begin scene,
        or a popup), dismissing the assessment popup along the way. If a blank/
        unresponsive screen is hit, capture evidence and keep trying."""
        from utils import blank_screen

        for _ in range(tries):
            try:
                self.dismiss_assessment_popup()
                if self.has_text(S.WORD_FUN, timeout=2) and self.has_text(S.STORIES, timeout=1):
                    return self
                if blank_screen.looks_blank(self.alt):
                    blank_screen.report("ensure_home", self.alt, "blank while navigating to Home")
                try:
                    self.alt.find_object(By.NAME, S.BACK_BTN).tap()
                except Exception:
                    for t in ("Enter", "Skip", "Continue", "Close"):
                        if self.has_text(t, timeout=1):
                            self.tap_text(t)
                            break
            except Exception:
                # command timeout / transient — likely a stuck screen; note and retry
                blank_screen.report("ensure_home", self.alt, "command timeout during navigation")
            time.sleep(2)
        assert self.is_loaded(), "could not reach the Home hub"
        return self

    def open(self, area: str):
        self.tap_text(area)
        time.sleep(4)
        return self

    def back(self):
        self.alt.find_object(By.NAME, S.BACK_BTN).tap()
        time.sleep(2)
        return self
