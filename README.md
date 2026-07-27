# Student App — QA Automation (AltTester + Python)

UI test automation for the English Gurukul **Student** app (Unity, IL2CPP, arm64),
driven through the **AltTester** SDK with the Python **AltDriver**. Sibling of the
Flutter Teacher-app Appium suite; same Page/Screen-Object + pytest shape.

- **Stack:** AltTester 2.3.1 · AltDriver (Python) · pytest · Screen Object Model
- **App under test:** `com.OritSciencesPrivateLimited.EnglishGurukul.student` (v4.0.0.2)
- **Device:** physical **arm64** phone over USB (Pixel 4a). The IL2CPP build ships
  `arm64-v8a` only, so an x86 emulator can't run it.

---

## How AltTester connects (read this first)

The app's build embeds the AltTester SDK (GPL-3.0, **no in-app license**). It runs
as a **client** that connects *out* to an **AltServer broker** at
`ALT_HOST:ALT_PORT` (127.0.0.1:13000). The broker only *routes* messages between
the app and the driver — the app executes every command itself. So a run needs,
in order:

1. **A broker listening on 13000.** You do **NOT** need AltTester Desktop (its
   server is license-gated, and free accounts can be deactivated). Instead the
   suite ships its own **license-free broker**, `tools/altserver_relay.py`, which
   `utils/alt_connect.py` **auto-starts** whenever it isn't already running. It's
   a tiny WebSocket relay that pairs the app and driver by `appName` — a complete,
   free replacement for the Desktop server. (Requires the `websockets` package,
   which is in `requirements.txt`.)
2. **`adb reverse tcp:13000 tcp:13000`** so an on-device app reaches the host
   relay. `utils/alt_connect.py` sets this up automatically. *(Not needed when the
   app runs in the Unity Editor on the same machine — see below.)*
3. The app running (on the phone, auto-launched — or in the Unity Editor).

> **No license, no account, no AltTester Desktop.** If the relay ever fails to
> start it logs to `reports/altserver_relay.log`; the most common cause is a
> missing `websockets` package (`pip install -r requirements.txt`).

### Running against the app in the Unity Editor (no device)

For local dev you can drive the app straight from **Play mode** in the Editor:

1. In the Unity project, select the **AltTester runner** object (the `AltTester
   Prefab` / `AltTesterEditor` in the startup scene) and set it to
   **"Connect to AltTester Server"** with **Host `127.0.0.1`**, **Port `13000`**,
   and the app name matching `ALT_APP_NAME` (default `__default__`).
2. Start the relay so the app has something to connect to when you press Play:
   ```powershell
   .\.venv\Scripts\python.exe tools\altserver_relay.py --host 127.0.0.1 --port 13000
   ```
   (Or just run `pytest` / `python tools/discover.py` — those auto-start it.)
3. Press **Play**. The AltTester overlay should connect to `127.0.0.1:13000`.
4. In another terminal run `python tools/discover.py` or `pytest`. Set
   `REVERSE_FORWARD=false` and `LAUNCH_APP=false` in `.env` for Editor runs (no
   device to `adb reverse` or launch).

## Setup

```powershell
# from qa_studentapp_automation/
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env      # then edit if needed
```

## First run — discover the scene

Once an AltServer is up and the phone is connected, learn the real UI object
names before writing UI tests:

```powershell
python tools/discover.py
```

This connects, writes **`reports/scene_dump.md`** (every element's name / text /
path) + **`reports/scene.png`**, and prints the app version. Use the dump to fill
the placeholder selectors in `screens/login_screen.py` and `screens/home_screen.py`,
then delete the `pytest.mark.skip` lines in `tests/test_login.py` / `test_home.py`.

## Run

```powershell
pytest                       # everything
pytest -m connectivity       # just the AltServer/app reachability smoke
pytest -m "login or home"    # once selectors are filled
```

- HTML report: `reports/report.html`  ·  Failure screenshots: `reports/screenshots/`
- `test_connectivity.py` needs **no selectors** — it passes the moment the broker
  is up and the app is instrumented, and writes the scene dump + version as a
  side effect.

## Layout

```
qa_studentapp_automation/
├── config/settings.py     # env-driven: host/port/app-name, package/activity, device
├── screens/               # Screen Objects (base_screen, login_screen, home_screen)
├── tests/                 # connectivity (real) + login/home (skeletons, skipped)
├── utils/
│   ├── alt_connect.py     # adb reverse + launch + AltDriver connect
│   ├── app_version.py     # version for the report (live app -> adb -> apk)
│   └── scene_dump.py      # dump scene/elements/screenshot
├── tools/discover.py      # run first: dump the live scene to learn selectors
├── conftest.py            # session `alt` fixture (skips if AltServer down) + screenshots
├── run_daily.py           # per-area Slack report + app version
├── pytest.ini · requirements.txt · .env.example
└── AUTOMATION_PLAN.md
```

## Daily run + Slack report

`run_daily.py` runs the suite and posts a per-area summary (**Connectivity, Login,
Home**) to Slack, headed with the app version. If the broker is down, areas report
as *skipped* and the status is `BLOCKED (AltServer/broker down)` rather than failed.

```powershell
.\.venv\Scripts\python.exe run_daily.py           # -> Slack (set SLACK_WEBHOOK_URL in .env)
```

Schedule daily via Windows Task Scheduler (see `run_daily.ps1`), same as the
teacher-app suite.

## Markers

`smoke`, `regression`, `connectivity`, `login`, `home`, `lessons`, `tests_flow`,
`profile`. See `AUTOMATION_PLAN.md` for the phased buildout.
