# Student App — Automation Plan (phased)

Built out in phases, mirroring the teacher-app suite. Each phase adds Screen
Objects + tests and is independently runnable via markers.

Legend: ✅ built · 🔶 next (needs live scene) · ⬜ planned

---

## Phase 0 — Infrastructure ✅ (built)

- AltDriver connection factory with auto `adb reverse` + app launch (`utils/alt_connect.py`).
- Session `alt` fixture that **skips** (not fails) when no AltServer is reachable.
- Screenshot-on-failure; HTML + JUnit reports.
- Scene-discovery tool (`tools/discover.py` → `reports/scene_dump.md` + screenshot).
- Per-area daily Slack report with app version (`run_daily.py`).

## Phase 1 — Connectivity ✅ (built)

| Test | Marker | Notes |
|---|---|---|
| Connected + scene loaded | `smoke connectivity` | scene non-empty, elements returned; writes version + scene dump |
| Screenshot + screen size | `smoke connectivity` | sane WxH, PNG captured |

Passes as soon as the broker is up and the app is instrumented — no selectors.

## Phase 2 — Login 🔶 (skeleton; needs live scene)

- Login screen loads; valid login reaches Home.
- Fill `screens/login_screen.py` selectors from `reports/scene_dump.md`; set
  `TEST_MOBILE` / `TEST_PASSWORD` in `.env`; remove the skip in `tests/test_login.py`.

Marker: `login`.

## Phase 3 — Home / Dashboard 🔶 (skeleton; needs live scene)

- Home loads; primary nav entries present (Lessons / Test / Profile).
- Fill `screens/home_screen.py`; remove the skip in `tests/test_home.py`.

Marker: `home`.

## Phase 4 — Lessons / Learning ⬜

- Open the learning area, a lesson/topic loads, media/content renders.

Marker: `lessons`.

## Phase 5 — Tests / Quizzes ⬜

- Start a quiz, questions render, submit → result/score.

Marker: `tests_flow`.

## Phase 6 — Profile / Rewards / Cross-cutting ⬜

- Profile data, stars/rewards, logout, offline/error states.

Marker: `profile`.

---

## Notes / risks to confirm

- **Broker/license:** the AltServer (AltTester Desktop) is license-gated; the app
  build is GPL/keyless. Running needs a valid Lite license *or* a free AltServer.
- **AltServer app name:** the build's registered name (default `__default__`) —
  confirm from the AltTester SDK settings / the first successful connect; set
  `ALT_APP_NAME` if different.
- **Selectors:** Unity names/text must be read from the live scene
  (`tools/discover.py`) — don't guess. Ask the app devs to add stable object
  names where a control is hard to target, same principle as Semantics labels on
  the Flutter side.
- **Device:** arm64 physical phone only (IL2CPP arm64 build).
