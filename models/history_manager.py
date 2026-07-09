"""
models/history_manager.py

Manages persistent score-history data stored in data/history.json.
Supports search by player name, deleting single entries, and clearing all.
"""

from datetime import datetime
from typing import List, Dict

from utils.helpers import load_json, save_json, export_to_csv


class HistoryManager:
    def __init__(self, path: str = "data/history.json"):
        self._path = path

    def add_entry(
        self, player: str, category: str, score: int, percentage: float
    ) -> None:
        entries = load_json(self._path, default=[])
        entries.append(
            {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "player": player,
                "category": category,
                "score": score,
                "percentage": percentage,
            }
        )
        save_json(self._path, entries)

    def all_entries(self) -> List[Dict]:
        return load_json(self._path, default=[])

    def search_by_player(self, name: str) -> List[Dict]:
        name = name.strip().lower()
        if not name:
            return self.all_entries()
        return [
            e for e in self.all_entries() if name in e.get("player", "").lower()
        ]

    def delete_entry(self, index: int) -> bool:
        entries = self.all_entries()
        if 0 <= index < len(entries):
            entries.pop(index)
            save_json(self._path, entries)
            return True
        return False

    def clear_all(self) -> None:
        save_json(self._path, [])

    def export_csv(self, path: str) -> bool:
        entries = self.all_entries()
        fieldnames = ["date", "player", "category", "score", "percentage"]
        return export_to_csv(path, entries, fieldnames)
