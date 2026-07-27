"""
screen_coords.py
================
ALL button/field coordinates for every screen.

DEVICE:
2400 x 1080

UNITY APP
ALL COORDINATES ARE DIRECT PIXELS
NO PERCENTAGES

HOW TO UPDATE:
---------------
1. Take screenshot
2. Open in Paint
3. Hover mouse over button center
4. Replace x,y below
"""

# ─────────────────────────────────────────────────────────────
# DEVICE SCREEN SIZE
# ─────────────────────────────────────────────────────────────

SCREEN_W = 2400
SCREEN_H = 1080

# ─────────────────────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────────────────────

LOGIN = {

    # Mobile number input
        "mobile_input":   (1142, 465),
        "ok_button":      (2166, 442),
        "confirm_button": (1203, 694),
}

LICENSE_SCREEN = {
        "license_input": (1108, 465),
        "confirm_button": (1181, 582),# "Enter license code" white input box
    }

# ─────────────────────────────────────────────────────────────
# SELECT PROFILE SCREEN
# ─────────────────────────────────────────────────────────────

SELECT_PROFILE = {

    "profile_1": (802, 581),

    "profile_2": (1111, 517),

    "profile_3": (1430, 586),

    "next_button": (1120, 891),
}

# ─────────────────────────────────────────────────────────────
# AVATAR SCREEN
# ─────────────────────────────────────────────────────────────

SELECT_AVATAR = {

    "avatar_1": (933, 492),

    "avatar_2": (1083, 488),

    "avatar_3": (1252, 497),

    "avatar_4": (1392, 483),

    "save_button": (1158, 670),
}

# ─────────────────────────────────────────────────────────────
# LANGUAGE DIALOG
# ─────────────────────────────────────────────────────────────

LANGUAGE_DIALOG = {

    "dropdown": (1692, 323),

    "option_0": (1186, 441),

    "option_1": (1177, 539),

    "option_2": (1167, 670),

    "option_3": (1181, 759),

    "save_button": (1177, 905),
}

# ─────────────────────────────────────────────────────────────
# BEGIN SCENE
# ─────────────────────────────────────────────────────────────

BEGIN_SCENE = {

    "enter_button": (1195, 567),

    "skip_button": (1992, 938),
}

# ─────────────────────────────────────────────────────────────
# WELCOME BACK POPUP
# ─────────────────────────────────────────────────────────────

WELCOME_BACK = {

    "continue_btn": (1191, 877),
}

# ─────────────────────────────────────────────────────────────
# STREAK POPUP
# ─────────────────────────────────────────────────────────────

STREAK_POPUP = {

    "close_btn": (2273, 117),
}

# ─────────────────────────────────────────────────────────────
# TEST POPUP
# ─────────────────────────────────────────────────────────────

TEST_POPUP = {

    "later_btn": (1425, 717),

    "take_test_btn": (1027, 713),
}

# ─────────────────────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────────────────────

HOME_SCREEN = {

    "back_arrow": (127, 108),

    "parents_icon": (323, 108),

    "school_icon": (145, 942),

    "stars_icon": (2105, 108),

    "avatar_icon": (473, 108),
}

# ─────────────────────────────────────────────────────────────
# PARENTS CORNER
# ─────────────────────────────────────────────────────────────

PARENTS_CORNER = {

    "logout_button": (2236, 103),

    "back_button": (127, 94),

    "parents_info_tab": (666, 127),

    "child_profile_tab": (998, 127),

    "progress_tab": (1317, 127),

    "timeout_tab": (1683, 127),

    "save_button": (1195, 952),
}

# ─────────────────────────────────────────────────────────────
# HELPER FUNCTION
# ─────────────────────────────────────────────────────────────

def get(screen_dict: dict, key: str):

    if key not in screen_dict:

        raise KeyError(
            f"Coordinate '{key}' not found"
        )

    return screen_dict[key]
