"""Content-area screen objects (reached from the Home hub): Stories, WordFun,
Tests (Quiz), Fun Learn, and the video player. Selectors confirmed live via
AltDriver exploration.
"""
from __future__ import annotations

import time

from alttester import By

from screens.base_screen import BaseScreen


class StoriesScreen(BaseScreen):
    def is_loaded(self, timeout: int = 15) -> bool:
        # Title 'Stories' on the stories screen.
        return self.has_name("Title", timeout=timeout) and self.has_text("Stories", timeout=3)


class WordFunScreen(BaseScreen):
    def is_loaded(self, timeout: int = 15) -> bool:
        # Title 'WordFun' + chapters (e.g. Phonics).
        return self.has_text("WordFun", timeout=timeout) or self.has_text("Phonics", timeout=3)


class QuizScreen(BaseScreen):
    """Tests == the Quiz/assessment area (Completed / Pending tabs)."""

    def is_loaded(self, timeout: int = 15) -> bool:
        return self.has_text("Pending", timeout=timeout) and self.has_text("Completed", timeout=3)


class FunLearnScreen(BaseScreen):
    """Fun Learn holds the video lessons (units of lessons)."""

    def is_loaded(self, timeout: int = 15) -> bool:
        return self.has_text("Off to school", timeout=timeout) or self.has_text("Unit", timeout=3)

    def open_lesson(self, name: str = "Off to school"):
        self.tap_text(name)
        time.sleep(7)  # video buffers/starts
        return VideoPlayer(self.alt)


class VideoPlayer(BaseScreen):
    SLIDER = "Slider"          # By.NAME — the timeline slider (UnityEngine.UI.Slider + SliderDrag)
    CURRENT_TIME = "currentTime"

    def is_playing(self, timeout: int = 25) -> bool:
        # The video screen is open when the VideoPlayer object exists; the
        # timeline/controls stay hidden until the video is tapped.
        return self.has_name("Video Player", timeout=timeout) or \
            self.has_name("Video Screen(Clone)", timeout=3)

    def seek_to_end(self):
        """Per QA rule: don't watch the whole video — click the video so the
        timeline hovers, then drag the timeline slider to the end. Records the
        slider value reached in `self.last_value` (≈1.0 means the end)."""
        w, h = self.alt.get_application_screensize()
        self.alt.tap([w / 2, h / 2])          # reveal the controls / timeline
        time.sleep(1)
        slider = self.alt.find_object(By.NAME, self.SLIDER)
        pos = slider.get_screen_position()
        # drag the handle from its current spot to the far right end of the track
        self.alt.swipe([pos[0], pos[1]], [w - 200, pos[1]], duration=1.5)
        time.sleep(1)
        try:
            self.last_value = float(
                slider.get_component_property("UnityEngine.UI.Slider", "value", "UnityEngine.UI")
            )
        except Exception:
            self.last_value = 1.0  # slider already gone -> video completed at the end
        return self

    def play(self):
        """Tap the play/pause button."""
        try:
            self.alt.find_object(By.NAME, "play and puase").tap()
        except Exception:
            pass
        time.sleep(2)
        return self

    def continue_to_quiz(self, timeout: int = 30) -> bool:
        """Per QA flow: after seeking to the end, click Play; if the Next/Retry
        popup appears, click Next so the quiz continues. Returns True if Next was
        taken (a quiz followed), False if the video just completed (no quiz)."""
        self.play()
        end = time.time() + timeout
        while time.time() < end:
            if self.has_text("Next", timeout=2):
                self.tap_text("Next")
                return True
            if not self.has_name("Video Player", timeout=1):
                return False  # video closed with no quiz
            time.sleep(2)
        return False

    def has_ended(self, timeout: int = 8) -> bool:
        """After seeking to the end the player closes -> the Slider is gone."""
        end = time.time() + timeout
        while time.time() < end:
            if not self.has_name(self.SLIDER, timeout=1):
                return True
            time.sleep(1)
        return False
