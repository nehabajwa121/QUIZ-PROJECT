"""
utils/helpers.py

Shared utility functions used across the Quiz Application:
- Safe JSON reading/writing with automatic file creation
- Theme (light/dark) color palettes
- Motivational quotes
- CSV export helper
"""

import json
import os
import random
import csv
from typing import Any, List


def ensure_file(path: str, default_content: Any) -> None:
    """Create a file with default content if it doesn't already exist."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default_content, f, indent=4)


def load_json(path: str, default: Any = None) -> Any:
    """
    Safely load JSON data from a file.
    Creates the file with a default value if missing.
    Returns the default value if the JSON is invalid.
    """
    if default is None:
        default = []
    ensure_file(path, default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Corrupted or unreadable file - reset to default gracefully
        save_json(path, default)
        return default


def save_json(path: str, data: Any) -> bool:
    """Safely write JSON data to a file. Returns True on success."""
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except OSError:
        return False


def export_to_csv(path: str, rows: List[dict], fieldnames: List[str]) -> bool:
    """Export a list of dict rows to a CSV file."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return True
    except OSError:
        return False


MOTIVATIONAL_QUOTES = [
    "Believe you can and you're halfway there.",
    "Success is the sum of small efforts repeated daily.",
    "The expert in anything was once a beginner.",
    "Don't watch the clock; do what it does. Keep going.",
    "Mistakes are proof that you are trying.",
    "Knowledge is power. Keep learning!",
    "Every accomplishment starts with the decision to try.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "The only way to learn is to keep going, one question at a time.",
]


def get_random_quote() -> str:
    return random.choice(MOTIVATIONAL_QUOTES)


class Theme:
    """Holds color palettes for light and dark modes."""

    LIGHT = {
        "bg": "#f5f7fa",
        "fg": "#1c1c1c",
        "card_bg": "#ffffff",
        "accent": "#4361ee",
        "accent_hover": "#3a56d4",
        "success": "#2ecc71",
        "danger": "#e74c3c",
        "muted": "#6c757d",
        "border": "#dee2e6",
        "entry_bg": "#ffffff",
    }

    DARK = {
        "bg": "#1a1d23",
        "fg": "#f1f1f1",
        "card_bg": "#252932",
        "accent": "#5c7cfa",
        "accent_hover": "#4c6ef5",
        "success": "#40c057",
        "danger": "#fa5252",
        "muted": "#adb5bd",
        "border": "#3a3f4b",
        "entry_bg": "#2d3139",
    }

    @staticmethod
    def get(dark_mode: bool) -> dict:
        return Theme.DARK if dark_mode else Theme.LIGHT


def grade_from_percentage(percentage: float) -> str:
    """Convert a percentage score to a letter grade."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    else:
        return "Fail"
