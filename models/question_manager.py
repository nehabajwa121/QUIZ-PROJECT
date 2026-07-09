"""
models/question_manager.py

Handles loading, randomizing, and validating quiz questions
for all categories. Also supports adding new questions.
"""

import os
import random
from typing import List, Dict, Optional

from utils.helpers import load_json, save_json


class QuestionManager:
    """Manages question banks for every quiz category."""

    CATEGORY_FILES = {
        "Python": "python.json",
        "General Knowledge": "gk.json",
        "Science": "science.json",
        "Mathematics": "maths.json",
    }

    def __init__(self, questions_dir: str = "questions"):
        self._questions_dir = questions_dir
        os.makedirs(self._questions_dir, exist_ok=True)

    @property
    def categories(self) -> List[str]:
        return list(self.CATEGORY_FILES.keys())

    def _path_for(self, category: str) -> str:
        filename = self.CATEGORY_FILES.get(category)
        if filename is None:
            # Fallback: derive a safe filename from the category name
            filename = category.lower().replace(" ", "_") + ".json"
            self.CATEGORY_FILES[category] = filename
        return os.path.join(self._questions_dir, filename)

    def load_questions(self, category: str, shuffle: bool = True) -> List[Dict]:
        """Load all questions for a category, optionally shuffled with
        options also shuffled per-question."""
        path = self._path_for(category)
        questions = load_json(path, default=[])

        # Defensive copy so we never mutate the on-disk representation
        questions = [dict(q) for q in questions]

        if shuffle:
            random.shuffle(questions)
            for q in questions:
                options = list(q.get("options", []))
                random.shuffle(options)
                q["options"] = options

        return questions

    def add_question(
        self,
        category: str,
        question_text: str,
        options: List[str],
        correct_answer: str,
    ) -> Optional[str]:
        """
        Add a new question to a category's JSON file.
        Returns an error message string if validation fails, otherwise None.
        """
        question_text = question_text.strip()
        options = [opt.strip() for opt in options]
        correct_answer = correct_answer.strip()

        if not question_text:
            return "Question text cannot be empty."
        if any(not opt for opt in options) or len(options) != 4:
            return "All four options must be filled in."
        if correct_answer not in options:
            return "Correct answer must match one of the four options."

        path = self._path_for(category)
        existing = load_json(path, default=[])

        # Duplicate check - case-insensitive comparison of question text
        for q in existing:
            if q.get("question", "").strip().lower() == question_text.lower():
                return "This question already exists in the selected category."

        existing.append(
            {
                "question": question_text,
                "options": options,
                "answer": correct_answer,
            }
        )
        save_json(path, existing)
        return None

    def question_count(self, category: str) -> int:
        return len(load_json(self._path_for(category), default=[]))
