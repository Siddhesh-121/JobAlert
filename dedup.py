"""
DEDUP MODULE
━━━━━━━━━━━
Tracks jobs already sent so you never get the same alert twice.
State is stored in data/seen_jobs.json and committed back by the
GitHub Actions workflow so it persists across runs.
"""

import json
import hashlib
import os

SEEN_FILE = os.path.join(os.path.dirname(__file__), "data", "seen_jobs.json")


def _job_id(job: dict) -> str:
    """Stable fingerprint: title + company (URL changes, these don't)."""
    raw = f"{job['title'].lower().strip()}|{job['company'].lower().strip()}"
    return hashlib.md5(raw.encode()).hexdigest()


def load_seen() -> set:
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()


def save_seen(seen: set) -> None:
    os.makedirs(os.path.dirname(SEEN_FILE), exist_ok=True)
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(seen), f, indent=2)


def filter_new(jobs: list[dict], seen: set) -> tuple[list[dict], set]:
    """Return only jobs not in seen, and the updated seen set."""
    new_jobs = []
    for job in jobs:
        jid = _job_id(job)
        if jid not in seen:
            new_jobs.append(job)
            seen.add(jid)
    return new_jobs, seen
