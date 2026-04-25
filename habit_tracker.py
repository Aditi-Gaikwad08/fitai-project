"""
habit_tracker.py — Workout Habit Tracker
==========================================
Stores daily workout logs in a JSON file.
Calculates:
  • Current streak (consecutive workout days)
  • Consistency % (workouts done / total days logged)
"""

import json
import os
from datetime import date, timedelta

DATA_FILE = "habit_data.json"   # stored in the project root


# ──────────────────────────────────────────────
# INTERNAL HELPERS
# ──────────────────────────────────────────────
def _load() -> dict:
    """Load habit data from JSON file, or return empty structure."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"logs": {}}   # {"logs": {"2025-07-01": true, ...}}


def _save(data: dict) -> None:
    """Persist habit data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ──────────────────────────────────────────────
# PUBLIC API
# ──────────────────────────────────────────────
def log_workout(did_workout: bool) -> None:
    """
    Record whether a workout was done today.
    Overwrites today's entry if called multiple times.
    """
    data = _load()
    today = str(date.today())          # e.g. "2025-07-15"
    data["logs"][today] = did_workout
    _save(data)


def get_streak() -> int:
    """
    Calculate the current consecutive-day workout streak.

    Counts backwards from today; stops when a day is missed OR
    has no log entry (unlogged days are treated as rest days).

    Returns:
        int — number of consecutive workout days ending today
    """
    data  = _load()
    logs  = data["logs"]
    today = date.today()
    streak = 0

    current = today
    while True:
        key = str(current)
        if logs.get(key) is True:
            streak += 1
            current -= timedelta(days=1)
        else:
            break   # day missed, not logged, or rest day

    return streak


def get_history() -> list:
    """
    Return the last 14 days of history as a list of dicts,
    newest first.

    Each dict: {"date": "Mon 15 Jul", "status": "✅" | "❌" | "—"}
    """
    data  = _load()
    logs  = data["logs"]
    today = date.today()
    history = []

    for i in range(14):
        day = today - timedelta(days=i)
        key = str(day)
        label = day.strftime("%a %d %b")   # e.g. "Mon 15 Jul"

        if key in logs:
            status = "✅ Workout" if logs[key] else "😴 Rest"
        else:
            status = "—"

        history.append({"date": label, "status": status})

    return history


def get_consistency() -> float:
    """
    Return workout consistency as a percentage.
    = (workout days) / (total logged days) × 100
    """
    data = _load()
    logs = data["logs"]
    if not logs:
        return 0.0
    workout_days = sum(1 for v in logs.values() if v)
    return round(workout_days / len(logs) * 100, 1)
