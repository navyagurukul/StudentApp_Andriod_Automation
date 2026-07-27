"""Run the Student App QA pass and post a per-area summary to Slack. Built for a
daily scheduled run — the AltTester counterpart of the teacher-app daily report.

The report is grouped by area — **Connectivity, Login, Home** (grow as the suite
does) — each with its own PASS/FAIL, headed with the app version. Tests that can't
run because the AltServer/broker is down show as **skipped** (not failed), so a
license/broker outage reads clearly instead of as a wall of red.

Usage (with the venv python):
    python run_daily.py                 # full suite -> Slack
    python run_daily.py -m connectivity # a subset
    python run_daily.py tests/test_x.py # explicit scope

Config (.env or environment):
    SLACK_WEBHOOK_URL   Slack Incoming Webhook URL (required to post)
    APP_VERSION         override the version shown in the header (else auto)
"""
from __future__ import annotations

import datetime
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PY = sys.executable
REPORTS = ROOT / "reports"
JUNIT = REPORTS / "junit.xml"

AREAS = ["Connectivity", "Login", "Home", "Stories", "Word Fun", "Quiz", "Videos"]


def classify(classname: str, name: str) -> str:
    c = (classname or "").replace(".", "/").lower()
    n = (name or "").lower()
    if "test_connectivity" in c:
        return "Connectivity"
    if "test_login" in c:
        return "Login"
    if "test_home" in c:
        return "Home"
    if "test_content" in c:
        # check video before quiz — every test name contains "test_"
        if "video" in n:
            return "Videos"
        if "stories" in n:
            return "Stories"
        if "wordfun" in n or "word_fun" in n:
            return "Word Fun"
        if "quiz" in n:
            return "Quiz"
    return "Connectivity"


def run_pytest(args):
    REPORTS.mkdir(parents=True, exist_ok=True)
    if JUNIT.exists():
        JUNIT.unlink()
    cmd = [PY, "-m", "pytest", *args, f"--junitxml={JUNIT}", "-p", "no:cacheprovider"]
    subprocess.run(cmd, cwd=str(ROOT))


def parse_junit(path):
    if not path.exists():
        return []
    root = ET.parse(path).getroot()
    suites = root.findall("testsuite") or [root]
    out = []
    for s in suites:
        for tc in s.findall("testcase"):
            failed = tc.find("failure") is not None or tc.find("error") is not None
            skipped = tc.find("skipped") is not None
            out.append({
                "area": classify(tc.get("classname"), tc.get("name")),
                "name": tc.get("name"),
                "failed": failed,
                "skipped": skipped,
                "ok": not failed and not skipped,
                "time": float(tc.get("time", 0) or 0),
            })
    return out


def area_line(area, records):
    recs = [r for r in records if r["area"] == area]
    if not recs:
        return f"• {area:<13} ⤼ not run"
    total = len(recs)
    passed = sum(1 for r in recs if r["ok"])
    failed = [r["name"] for r in recs if r["failed"]]
    skipped = sum(1 for r in recs if r["skipped"])
    if failed:
        line = f"• {area:<13} ❌ {passed}/{total}  — " + ", ".join(failed[:3])
        if len(failed) > 3:
            line += f" +{len(failed) - 3} more"
    elif passed == 0 and skipped:
        line = f"• {area:<13} ⤼ skipped ({skipped})"
    else:
        line = f"• {area:<13} ✅ {passed}/{total}"
    return line


def app_version_label():
    # Prefer the live value the connectivity test captured this run.
    captured = REPORTS / "app_version.txt"
    if captured.exists():
        v = captured.read_text(encoding="utf-8").strip()
        if v and v.lower() != "unknown":
            return f"V{v}"
    from utils import app_version
    return app_version.label()


def post_slack(text):
    url = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    if not url:
        print("[run_daily] SLACK_WEBHOOK_URL not set — printing report instead:\n")
        print(text)
        return
    r = requests.post(url, json={"text": text}, timeout=30)
    r.raise_for_status()
    print("[run_daily] posted to Slack.")


def main():
    args = sys.argv[1:] or []
    run_pytest(args)
    records = parse_junit(JUNIT)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    version = app_version_label()

    if not records:
        post_slack(
            f"*Student App QA — Daily* ({now})   ⚠️ could not run tests\n"
            f"App version: {version}"
        )
        sys.exit(1)

    total = len(records)
    passed = sum(1 for r in records if r["ok"])
    failed = sum(1 for r in records if r["failed"])
    skipped = sum(1 for r in records if r["skipped"])
    runtime = sum(r["time"] for r in records)

    if failed:
        status = "❌ FAIL"
    elif passed == 0 and skipped:
        status = "⤼ BLOCKED (AltServer/broker down)"
    else:
        status = "✅ PASS"

    lines = [
        f"*Student App QA — Daily* ({now})   {status}",
        f"App version: *{version}*",
        f"Passed {passed}/{total}  •  Failed {failed}  •  Skipped {skipped}  •  {runtime:.0f}s",
        "",
    ]
    lines += [area_line(a, records) for a in AREAS]
    post_slack("\n".join(lines))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
