"""utils/logger.py — logging + per-user results"""
import logging, json, os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", encoding="utf-8"),
    ]
)
log = logging.getLogger("student_app")

RESULTS_FILE = "logs/results.jsonl"

def write_result(mobile: str, passed: bool, message: str):
    entry = {"ts": datetime.now().isoformat(), "mobile": mobile, "passed": passed, "msg": message}
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    log.info(f"{'OK' if passed else 'FAIL'} | {mobile} | {message}")
