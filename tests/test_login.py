"""Login flow (Student app) — real tests, driven via AltDriver over the relay.

Covers the login screen, mobile-field input, and the transition to the School
Code screen (and Back). We don't complete registration (that hits the backend).
"""
import pytest

from data.test_data import TEST_MOBILE
from screens.login_screen import LoginScreen, S


@pytest.mark.smoke
@pytest.mark.login
def test_login_screen_loads(alt):
    login = LoginScreen(alt).ensure_loaded()
    assert login.has_name(S.MOBILE_FIELD), "mobile input 'Type mobile' not found"
    assert login.has_text(S.CONFIRM_TEXT), "'Confirm' button not found"


@pytest.mark.smoke
@pytest.mark.login
def test_mobile_field_accepts_input(alt):
    login = LoginScreen(alt).ensure_loaded()
    login.enter_mobile(TEST_MOBILE)
    value = login.mobile_value()
    assert TEST_MOBILE in value, f"mobile field did not hold the typed value (got {value!r})"


@pytest.mark.login
def test_login_advances_to_school_code(alt):
    login = LoginScreen(alt).ensure_loaded()
    school = login.submit_mobile(TEST_MOBILE)
    assert school.is_loaded(), "did not reach the School Code screen after Confirm"


@pytest.mark.login
def test_back_from_school_code_returns_to_login(alt):
    login = LoginScreen(alt).ensure_loaded()
    school = login.submit_mobile(TEST_MOBILE)
    assert school.is_loaded()
    back = school.go_back()
    assert back.is_loaded(), "Back did not return to the login screen"
