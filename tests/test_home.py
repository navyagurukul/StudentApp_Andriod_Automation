"""Home hub (Student app) — verifies the content hub loads with its areas."""
import pytest

from screens.home_screen import HomeScreen, S


@pytest.mark.smoke
@pytest.mark.home
def test_home_hub_loads(alt):
    home = HomeScreen(alt).ensure_home()
    for area in (S.STORIES, S.WORD_FUN, S.TESTS, S.FUN_LEARN):
        assert home.has_text(area), f"home area '{area}' not visible"
