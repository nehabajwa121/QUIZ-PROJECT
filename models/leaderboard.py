"""
models/leaderboard.py

Manages persistent leaderboard data stored in data/leaderboard.json.
"""

from datetime import datetime
from typing import List, Dict

from utils.helpers import load_json, save_json


class Leaderboard:
    def __init__(self, path: str = "data/leaderboard.json"):
        self._path = path

    def add_entry(self, player: str, score: int, category: str) -> None:
        entries = load_json(self._path, default=[])
        entries.append(
            {
                "player": player,
                "score": score,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        save_json(self._path, entries)

    def top_scores(self, limit: int = 10) -> List[Dict]:
        entries = load_json(self._path, default=[])
        return sorted(entries, key=lambda e: e.get("score", 0), reverse=True)[:limit]

    def reset(self) -> None:
        save_json(self._path, [])
