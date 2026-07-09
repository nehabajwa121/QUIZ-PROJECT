"""
models/score_manager.py

Tracks score, correct/wrong counts, and percentage for a single quiz
attempt currently in progress.
"""

POINTS_PER_CORRECT = 10


class ScoreManager:
    """Encapsulates all scoring state for one quiz session."""

    def __init__(self, total_questions: int):
        self._total_questions = max(total_questions, 1)
        self._score = 0
        self._correct = 0
        self._wrong = 0
        self._answered = 0

    def record_correct(self) -> None:
        self._score += POINTS_PER_CORRECT
        self._correct += 1
        self._answered += 1

    def record_wrong(self) -> None:
        self._wrong += 1
        self._answered += 1

    def record_skipped(self) -> None:
        # Skipped/timed-out questions count as answered but score 0
        self._answered += 1

    @property
    def score(self) -> int:
        return self._score

    @property
    def correct(self) -> int:
        return self._correct

    @property
    def wrong(self) -> int:
        return self._wrong

    @property
    def answered(self) -> int:
        return self._answered

    @property
    def percentage(self) -> float:
        max_score = self._total_questions * POINTS_PER_CORRECT
        if max_score == 0:
            return 0.0
        return round((self._score / max_score) * 100, 2)
