"""Login screen object (Student app).

Selectors confirmed from the live scene via tools/discover.py:
  - title "Enter your mobile number"  (MainTitle)
  - mobile input GameObject "Type mobile"
  - "Confirm" button label (Text (TMP))

Submitting a mobile number advances to the School Code screen.
"""
from __future__ import annotations

from screens.base_screen import BaseScreen


class S:
    TITLE_TEXT = "Enter your mobile number"
    MOBILE_FIELD = "Type mobile"     # By.NAME — the mobile TMP_InputField
    CONFIRM_TEXT = "Confirm"


class LoginScreen(BaseScreen):
    def is_loaded(self, timeout: int = 20) -> bool:
        return self.has_text(S.TITLE_TEXT, timeout=timeout)

    def ensure_loaded(self):
        """Get back to the login screen if a downstream screen is showing, so a
        test can start from a known state regardless of what ran before it."""
        if not self.has_text(S.TITLE_TEXT, timeout=3):
            if self.has_text("Enter School Code", timeout=2):
                self.tap_text("Back")
        assert self.is_loaded(), "could not return to the login screen"
        return self

    def enter_mobile(self, number: str):
        self.type_into(S.MOBILE_FIELD, number)
        return self

    def mobile_value(self) -> str:
        return self.find_by_name(S.MOBILE_FIELD).get_text() or ""

    def tap_confirm(self):
        self.tap_text(S.CONFIRM_TEXT)
        return self

    def submit_mobile(self, number: str):
        """Enter the number and Confirm -> returns the School Code screen."""
        self.enter_mobile(number)
        self.tap_confirm()
        from screens.school_code_screen import SchoolCodeScreen
        return SchoolCodeScreen(self.alt).wait_loaded()
