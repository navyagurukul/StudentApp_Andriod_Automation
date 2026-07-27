"""Content-area tests (Student app), driven via AltDriver over the relay.

Covers the home content hub: Stories, Word Fun, Tests (Quiz), and Fun Learn
videos. For videos we do NOT watch the whole clip — we open a lesson, click the
video so the timeline hovers, and drag the timeline to the end (which fast-
forwards the clip to completion). If the assessment "take a test" popup appears,
we click Later.

Prereq: a logged-in student at the Home hub. The `home` fixture navigates there.
"""
import time

import pytest

from screens.home_screen import HomeScreen, S
from screens.content_screens import (
    StoriesScreen,
    WordFunScreen,
    QuizScreen,
    FunLearnScreen,
)


@pytest.fixture
def home(alt):
    return HomeScreen(alt).ensure_home()


@pytest.mark.content
@pytest.mark.stories
def test_open_stories(alt, home):
    home.open(S.STORIES)
    assert StoriesScreen(alt).is_loaded(), "Stories screen did not load"
    home.back()


@pytest.mark.content
@pytest.mark.wordfun
def test_open_wordfun(alt, home):
    home.open(S.WORD_FUN)
    assert WordFunScreen(alt).is_loaded(), "Word Fun screen did not load"
    home.back()


@pytest.mark.content
@pytest.mark.quiz
def test_open_quiz_tests(alt, home):
    home.open(S.TESTS)
    home.dismiss_assessment_popup()
    assert QuizScreen(alt).is_loaded(), "Tests/Quiz screen did not load"
    home.back()


@pytest.mark.content
@pytest.mark.video
def test_video_seeks_and_continues(alt, home):
    home.open(S.FUN_LEARN)
    fun = FunLearnScreen(alt)
    assert fun.is_loaded(), "Fun Learn did not load"

    player = fun.open_lesson("Off to school")
    assert player.is_playing(), "video did not start"

    # Don't watch the whole clip: click the video so the timeline hovers, drag it
    # to the end, then click Play. If a Next/Retry popup appears, click Next and
    # the quiz continues; otherwise the video completes.
    player.seek_to_end()
    assert player.last_value >= 0.9, (
        f"timeline was not dragged to the end (slider value={player.last_value})"
    )

    # Click Play; if a Next/Retry popup appears (quiz-lessons), click Next so the
    # quiz continues. Plain lessons just complete — both are fine.
    went_to_quiz = player.continue_to_quiz()
    print(f"[video] followed by quiz: {went_to_quiz}")

    HomeScreen(alt).ensure_home()
