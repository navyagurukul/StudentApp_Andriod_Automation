"""Test data for the Student-app AltTester suite."""
from __future__ import annotations

import os

# Test student mobile (unregistered -> advances to the School Code screen).
TEST_MOBILE = os.getenv("TEST_MOBILE", "9000000001")

# Student school/licence code (analog of the teacher app's SANK48).
SCHOOL_LICENSE_CODE = os.getenv("SCHOOL_LICENSE_CODE", "MPSB25")

# The school that SCHOOL_LICENSE_CODE resolves to (pre-filled on the registration form).
SCHOOL_NAME = os.getenv("SCHOOL_NAME", "Modern Public School")
