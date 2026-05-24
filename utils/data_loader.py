"""utils/data_loader.py — load test users from JSON"""
import json, os

def load_users(path: str = None) -> list:
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "config", "test_users.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
