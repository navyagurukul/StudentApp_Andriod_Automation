"""Post a pytest JUnit result summary to Slack.

Used by the Appium daily workflow, which needs no AltTester build on the device.
The AltTester suite has its own richer per-area reporter in run_daily.py.

    python tools/slack_junit_report.py --junit appium/reports/junit.xml \
        --title "Student App (Android) - Appium"

Config (environment):
    SLACK_WEBHOOK_URL   Slack Incoming Webhook. Without it the report is printed.
    GITHUB_RUN_ID       linked in the header when running under Actions
    GITHUB_REPOSITORY   likewise
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ICON = {"pass": ":white_check_mark:", "fail": ":x:", "skip": ":fast_forward:"}


def classify(case) -> tuple[str, str]:
    """-> (status, detail)"""
    if case.find("failure") is not None:
        return "fail", (case.find("failure").get("message") or "").strip()
    if case.find("error") is not None:
        return "fail", (case.find("error").get("message") or "").strip()
    if case.find("skipped") is not None:
        return "skip", (case.find("skipped").get("message") or "").strip()
    return "pass", ""


def build(junit: Path, title: str) -> tuple[str, bool]:
    if not junit.is_file():
        return f":warning: *{title}*\nNo results file at `{junit}` - the run died before pytest wrote one.", False

    root = ET.parse(junit).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    cases = list(suite.iter("testcase"))

    counts = {"pass": 0, "fail": 0, "skip": 0}
    failures, skips = [], []
    for c in cases:
        status, detail = classify(c)
        counts[status] += 1
        name = f"{(c.get('classname') or '').split('.')[-1]}::{c.get('name')}"
        if status == "fail":
            failures.append((name, detail.splitlines()[0][:180] if detail else ""))
        elif status == "skip":
            skips.append((name, detail.splitlines()[0][:120] if detail else ""))

    ok = counts["fail"] == 0 and counts["pass"] > 0
    head = ICON["pass"] if ok else (ICON["fail"] if counts["fail"] else ":warning:")

    lines = [f"{head} *{title}*"]
    run_id, repo = os.getenv("GITHUB_RUN_ID"), os.getenv("GITHUB_REPOSITORY")
    if run_id and repo:
        lines.append(f"<https://github.com/{repo}/actions/runs/{run_id}|Run details> · {suite.get('time', '?')}s")
    lines.append(
        f"*{counts['pass']} passed · {counts['fail']} failed · {counts['skip']} skipped* "
        f"(of {len(cases)})"
    )

    if counts["pass"] == 0 and counts["skip"]:
        lines.append("_Nothing actually ran - every test was skipped._")
    for name, msg in failures[:6]:
        lines.append(f"  {ICON['fail']} `{name}`" + (f" - {msg}" if msg else ""))
    if len(failures) > 6:
        lines.append(f"  _...and {len(failures) - 6} more failures_")
    for name, msg in skips[:3]:
        lines.append(f"  {ICON['skip']} `{name}`" + (f" - {msg}" if msg else ""))
    if len(skips) > 3:
        lines.append(f"  _...and {len(skips) - 3} more skipped_")

    return "\n".join(lines), ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--junit", required=True, type=Path)
    ap.add_argument("--title", default="Student App QA")
    args = ap.parse_args()

    text, ok = build(args.junit, args.title)
    print(text)

    hook = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    if not hook:
        print("\n[slack] SLACK_WEBHOOK_URL not set - printed above instead of posting.")
        return 0
    req = urllib.request.Request(
        hook, data=json.dumps({"text": text}).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        print(f"\n[slack] {r.status} {r.read().decode()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
