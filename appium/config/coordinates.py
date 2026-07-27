"""
coordinates.py
==============
DEVICE:
2400 x 1080

ALL VALUES ARE DIRECT PIXELS
NO PERCENTAGES
"""

COORDS = {

    # ── Login screen ──────────────────────────────────────────────────────
    # Login.png / Confirm.png
    "login": {
        "mobile_input":   (1142, 465),  # "Enter mobile number" white input box
        "ok_button":      (2166, 442),  # green "OK" button
        "confirm_button": (1203, 694),  # green "Confirm" button
    },

    "license_screen": {
        "license_input": (1108, 465),
        "confirm_button": (1181, 582),# "Enter license code" white input box
    },

    # ── Select Profile ────────────────────────────────────────────────────
    # Select_Profile.png — shows 3 profiles: Grade Tre / Blah5 / q4
    "select_profile": {
        "profile_1":   (802, 581),  # leftmost profile
        "profile_2":   (1111, 517),  # middle profile
        "profile_3":   (1430, 586),  # rightmost profile
        "next_button": (1120, 891),  # "NEXT >" orange button
    },

    # ── Select Avatar ─────────────────────────────────────────────────────
    # Avatar.png — "Select your Avatar" with 4 animals + Save
    "select_avatar": {
        "avatar_1":    (933, 492),  # fox
        "avatar_2":    (1083, 488),  # panda
        "avatar_3":    (1252, 497),  # bear
        "avatar_4":    (1392, 483),  # cat
        "save_button": (1158, 670),  # "Save" orange button
    },

    # ── Language Dialog ───────────────────────────────────────────────────
    # mother_tonguelanguage.png — "What is your mother tongue?"
    "language_dialog": {
        "dropdown":    (1692, 323),  # 1st language dropdown (tap to open)
        "save_button": (1177, 905),  # "Save" button at bottom
        # Options visible after tapping dropdown (language_dropdown.png):
        "option_0":    (1186, 441),  # Telugu — index 0
        "option_1":    (1177, 539),  # next language — index 1
        "option_2":    (1167, 670),  # next language — index 2
        "option_3":    (1181, 759),  # next language — index 3
    },

    # ── Enter Button (Begin scene — door with Enter label) ────────────────
    # enter_button.png
    "begin_scene": {
        "enter_button": (1195, 567),  # "Enter" button center of screen
        "skip_button": (1992, 938),      # Skip button bottom-right corner
    },

    # ── Welcome Back popup ────────────────────────────────────────────────
    # welcome_back.png — shows profile / grade / stars / Continue
    "welcome_back": {
        "continue_btn": (1191, 877),  # "Continue" orange button
    },

    # ── Daily Rewards / Streak popup ──────────────────────────────────────
    # streak.png — Day 1/2/3/4/5 stars popup
    "streak_popup": {
        "close_btn": (2273, 117),  # X button top-right corner
    },

    # ── Test popup ────────────────────────────────────────────────────────
    # test_popup.png — "Your teacher has asked you to take a test"
    "test_popup": {
        "later_btn":     (1425, 717),  # "Later" button (right)
        "take_test_btn": (1027, 713),  # "Take Test" button (left)
    },

    # ── Home / ParentsScreen ──────────────────────────────────────────────
    # Home_loading.png — main game screen with top icon bar
    "home_screen": {
        "back_arrow":    (127, 108),  # <- back arrow far left
        "parents_icon":  (323, 108),  # people icon (2nd from left) → opens Parents Corner
        "school_icon":   (145, 942),  # school logo (3rd from left)
        "stars_icon":    (2105, 108),  # star count top-right area
        "avatar_icon":   (473, 108),  # avatar icon far right
    },

    # ── Parents Corner ────────────────────────────────────────────────────
    # logout_button.png — Parents Info screen
    # LOGOUT = orange arrow icon TOP-RIGHT corner
    "parents_corner": {
        "logout_button":     (2236, 103),  # ↪ orange logout icon — TOP RIGHT
        "back_button":       (127, 94),  # <- back arrow — top left
        "parents_info_tab":  (666, 127),  # "Parents Info" tab
        "child_profile_tab": (998, 127),  # "Child Profile" tab
        "progress_tab":      (1317, 127),  # "Progress" tab
        "timeout_tab":       (1683, 127),  # "Timeout" tab
        "save_button":       (1195, 952),  # "Save" button bottom
    },
}


def get(screen: str, element: str):

    if screen not in COORDS:
        raise ValueError(
            f"Screen '{screen}' not found"
        )

    if element not in COORDS[screen]:
        raise ValueError(
            f"Element '{element}' not found"
        )

    return COORDS[screen][element]