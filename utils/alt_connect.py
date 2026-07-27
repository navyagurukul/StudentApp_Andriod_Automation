"""Open/close the AltDriver connection to the running Student app.

Handles the USB plumbing the AltTester broker model needs:
  1. `adb reverse tcp:<port>` so the on-device app can reach the host's AltServer.
  2. (optionally) launch the app.
  3. connect AltDriver to the AltServer at ALT_HOST:ALT_PORT.

If the connection is refused/closed, that almost always means **no AltServer is
running** (it's started by AltTester Desktop, which is license-gated) — the error
message says so, so a failing run points at the real cause.
"""
from __future__ import annotations

import atexit
import shutil
import socket
import subprocess
import sys
import time

from alttester import AltDriver

from config import settings

_relay_proc = None


def _port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        return s.connect_ex((host, port)) == 0


def _relay_log_path():
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return settings.REPORTS_DIR / "altserver_relay.log"


def ensure_relay() -> None:
    """Start the free AltServer relay if nothing is already listening on the
    AltTester port. The relay is the license-free broker both the app and the
    driver connect to; auto-starting it means `pytest` just works.

    If the relay can't start (most commonly the `websockets` dependency is
    missing), say so loudly — a silent failure here just makes every test skip
    with a misleading "AltServer unavailable"."""
    global _relay_proc
    host = "127.0.0.1"
    if _port_open(host, settings.ALT_PORT):
        return  # already running (this session or externally)

    try:
        import websockets  # noqa: F401 — the relay needs it; fail early with a clear message
    except ImportError:
        print(
            "[alt_connect] cannot start the free AltServer relay: the 'websockets' "
            "package is not installed. Run `pip install -r requirements.txt` "
            "(or `pip install websockets`) and try again."
        )
        return

    script = settings.ROOT / "tools" / "altserver_relay.py"
    log_path = _relay_log_path()
    # Send relay output to a log file (not DEVNULL) so a crash is diagnosable.
    log_file = open(log_path, "w", encoding="utf-8")
    _relay_proc = subprocess.Popen(
        [sys.executable, "-u", str(script), "--host", host, "--port", str(settings.ALT_PORT)],
        stdout=log_file, stderr=subprocess.STDOUT,
    )
    atexit.register(_stop_relay)
    for _ in range(20):  # wait up to ~10s for it to bind
        if _port_open(host, settings.ALT_PORT):
            print(f"[alt_connect] started AltServer relay on :{settings.ALT_PORT} (log: {log_path})")
            return
        if _relay_proc.poll() is not None:  # it exited early — surface why
            break
        time.sleep(0.5)

    tail = ""
    try:
        tail = log_path.read_text(encoding="utf-8").strip()[-500:]
    except Exception:
        pass
    print(
        f"[alt_connect] warning: AltServer relay did not come up on :{settings.ALT_PORT}. "
        f"See {log_path}." + (f"\n--- relay log tail ---\n{tail}" if tail else "")
    )


def _stop_relay() -> None:
    global _relay_proc
    if _relay_proc is not None:
        try:
            _relay_proc.terminate()
        except Exception:
            pass
        _relay_proc = None


def _adb(*args) -> subprocess.CompletedProcess:
    adb = shutil.which("adb") or "adb"
    base = [adb]
    if settings.UDID:
        base += ["-s", settings.UDID]
    return subprocess.run(base + list(args), capture_output=True, text=True, timeout=30)


def setup_reverse() -> None:
    """`adb reverse tcp:PORT tcp:PORT` — lets the device app reach the host AltServer."""
    try:
        _adb("reverse", f"tcp:{settings.ALT_PORT}", f"tcp:{settings.ALT_PORT}")
    except Exception as exc:  # pragma: no cover - best effort
        print(f"[alt_connect] adb reverse failed (continuing): {exc}")


def launch_app() -> None:
    try:
        _adb("shell", "monkey", "-p", settings.APP_PACKAGE,
             "-c", "android.intent.category.LAUNCHER", "1")
    except Exception as exc:  # pragma: no cover - best effort
        print(f"[alt_connect] launch failed (continuing): {exc}")


def open_driver(app_name: str | None = None) -> AltDriver:
    """Connect and return an AltDriver. Raises a clear error if no AltServer is up."""
    ensure_relay()
    if settings.REVERSE_FORWARD:
        setup_reverse()
    if settings.LAUNCH_APP:
        launch_app()
    try:
        return AltDriver(
            host=settings.ALT_HOST,
            port=settings.ALT_PORT,
            app_name=app_name or settings.ALT_APP_NAME,
            timeout=settings.CONNECT_TIMEOUT,
            enable_logging=False,
        )
    except Exception as exc:
        raise ConnectionError(
            f"Could not connect to AltServer at {settings.ALT_HOST}:{settings.ALT_PORT} "
            f"(app '{app_name or settings.ALT_APP_NAME}'). The free relay "
            f"(tools/altserver_relay.py) should auto-start — check "
            f"reports/altserver_relay.log. You do NOT need AltTester Desktop. "
            f"Make sure: (1) `pip install -r requirements.txt` ran (needs 'websockets'), "
            f"(2) the app is running and its AltTester runner is set to connect to "
            f"{settings.ALT_HOST}:{settings.ALT_PORT} with appName '{settings.ALT_APP_NAME}', "
            f"and (3) on a USB device, `adb reverse tcp:{settings.ALT_PORT} tcp:{settings.ALT_PORT}` is set. "
            f"Original error: {exc}"
        ) from exc


def close_driver(alt: AltDriver | None) -> None:
    if alt is None:
        return
    try:
        alt.stop()
    except Exception:
        pass
