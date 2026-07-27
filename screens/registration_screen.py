"""Self Registration Form — reached from the School Code screen after a valid
licence code. Selectors confirmed live via tools/discover.py.

We only assert this form opens correctly (e.g. school pre-filled from the code);
the tests never tap the final Confirm, which would register a real student.
"""
from __future__ import annotations

from screens.base_screen import BaseScreen


class S:
    TITLE_TEXT = "Self Registration Form"
    NAME_PLACEHOLDER = "Child Name"
    CONFIRM_TEXT = "Confirm"
    BACK_TEXT = "Back"


class RegistrationScreen(BaseScreen):
    def is_loaded(self, timeout: int = 15) -> bool:
        return self.has_text(S.TITLE_TEXT, timeout=timeout)

    def wait_loaded(self, timeout: int = 15):
        self.find_by_text(S.TITLE_TEXT, timeout=timeout)
        return self

    def shows_school(self, name: str, timeout: int = 8) -> bool:
        """The School field is pre-filled from the licence code."""
        return self.has_text(name, timeout=timeout)
