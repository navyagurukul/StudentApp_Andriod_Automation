"""School Code (Licence Code) screen — reached from Login after submitting a
mobile number. Selectors confirmed live via tools/discover.py.
"""
from __future__ import annotations

from screens.base_screen import BaseScreen


class S:
    TITLE_TEXT = "Enter School Code"
    # The editable field is the shared "Type mobile" TMP_InputField (reused prefab);
    # "LicenceCode" is only the wrapper/label and is not settable.
    CODE_FIELD = "Type mobile"
    CONFIRM_TEXT = "Confirm"
    BACK_TEXT = "Back"


class SchoolCodeScreen(BaseScreen):
    def is_loaded(self, timeout: int = 15) -> bool:
        return self.has_text(S.TITLE_TEXT, timeout=timeout)

    def wait_loaded(self, timeout: int = 15):
        self.find_by_text(S.TITLE_TEXT, timeout=timeout)
        return self

    def enter_code(self, code: str):
        self.type_into(S.CODE_FIELD, code)
        return self

    def submit_code(self, code: str):
        """Enter a valid licence code and Confirm -> returns the registration form."""
        self.enter_code(code)
        self.tap_text(S.CONFIRM_TEXT)
        from screens.registration_screen import RegistrationScreen
        return RegistrationScreen(self.alt).wait_loaded()

    def go_back(self):
        self.tap_text(S.BACK_TEXT)
        from screens.login_screen import LoginScreen
        login = LoginScreen(self.alt)
        login.is_loaded()
        return login
