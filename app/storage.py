import json
import os

STORAGE_FILE = "data/submissions.json"

def get_submissions():
    if not os.path.exists(STORAGE_FILE):
        return []
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_submission(sub):
    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
    subs = get_submissions()
    subs.append(sub)
    with open(STORAGE_FILE, "w") as f:
        json.dump(subs, f, indent=4)
