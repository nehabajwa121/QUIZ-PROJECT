"""
main.py

Entry point for the Advanced Python Quiz Application.

QuizApp is the central controller: it owns the Tk root window, manages
navigation between screens (frames), holds shared managers (questions,
score, leaderboard, history), and exposes actions that individual pages
call back into (start_quiz, finish_quiz, toggle_theme, etc.).

Run with:  python main.py
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Make sure local packages (models, ui, utils) are importable regardless
# of the working directory the script is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.question_manager import QuestionManager
from models.leaderboard import Leaderboard
from models.history_manager import HistoryManager
from utils.helpers import Theme, grade_from_percentage

from ui.login_page import LoginPage
from ui.home_page import HomePage
from ui.quiz_page import QuizSetupPage, QuizPage
from ui.result_page import ResultPage
from ui.leaderboard_page import LeaderboardPage
from ui.history_page import HistoryPage
from ui.question_editor import QuestionEditorPage

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_DIR = os.path.join(BASE_DIR, "questions")
DATA_DIR = os.path.join(BASE_DIR, "data")
LEADERBOARD_PATH = os.path.join(DATA_DIR, "leaderboard.json")
HISTORY_PATH = os.path.join(DATA_DIR, "history.json")

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 650


class QuizApp(tk.Tk):
    """Root application window and central controller for all screens."""

    def __init__(self):
        super().__init__()
        self.title("Quiz Master — Advanced Python Quiz Application")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(760, 560)

        # ---------------- Shared state ---------------- #
        self.player_name = ""
        self.dark_mode = False
        self.sound_enabled = True
        self._is_fullscreen = False

        # ---------------- Shared managers ---------------- #
        self.question_manager = QuestionManager(QUESTIONS_DIR)
        self.leaderboard = Leaderboard(LEADERBOARD_PATH)
        self.history_manager = HistoryManager(HISTORY_PATH)

        self.configure(bg=Theme.get(self.dark_mode)["bg"])
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self._exit_fullscreen())

        # ---------------- Frame container ---------------- #
        container = tk.Frame(self, bg=self.theme["bg"])
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self._container = container

        self.frames = {}
        frame_classes = {
            "LoginPage": LoginPage,
            "HomePage": HomePage,
            "QuizSetup": QuizSetupPage,
            "QuizPage": QuizPage,
            "ResultPage": ResultPage,
            "Leaderboard": LeaderboardPage,
            "History": HistoryPage,
            "QuestionEditor": QuestionEditorPage,
        }
        for name, FrameClass in frame_classes.items():
            frame = FrameClass(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    # ------------------------------------------------------------------ #
    # Theme helpers
    # ------------------------------------------------------------------ #
    @property
    def theme(self) -> dict:
        return Theme.get(self.dark_mode)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.configure(bg=self.theme["bg"])
        self._container.configure(bg=self.theme["bg"])
        for frame in self.frames.values():
            if hasattr(frame, "refresh_theme"):
                frame.refresh_theme()
        # Re-show current frame's on_show to refresh dynamic labels/data
        self._invoke_on_show(self._current_frame_name)

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    _current_frame_name = "LoginPage"

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()
        self._current_frame_name = name
        self._invoke_on_show(name)

    def _invoke_on_show(self, name: str):
        frame = self.frames.get(name)
        if frame and hasattr(frame, "on_show"):
            frame.on_show()

    def set_player_name(self, name: str):
        self.player_name = name

    # ------------------------------------------------------------------ #
    # Quiz lifecycle actions (called by pages)
    # ------------------------------------------------------------------ #
    def start_quiz(self, category: str):
        quiz_frame: QuizPage = self.frames["QuizPage"]
        self.show_frame("QuizPage")
        quiz_frame.start(category)

    def finish_quiz(self, category: str, score_manager):
        percentage = score_manager.percentage
        grade = grade_from_percentage(percentage)

        self.leaderboard.add_entry(self.player_name, score_manager.score, category)
        self.history_manager.add_entry(
            self.player_name, category, score_manager.score, percentage
        )

        result_data = {
            "player": self.player_name,
            "category": category,
            "score": score_manager.score,
            "correct": score_manager.correct,
            "wrong": score_manager.wrong,
            "percentage": percentage,
            "grade": grade,
        }
        self.show_frame("ResultPage")
        self.frames["ResultPage"].show_result(result_data)

    # ------------------------------------------------------------------ #
    # Window controls
    # ------------------------------------------------------------------ #
    def toggle_fullscreen(self):
        self._is_fullscreen = not self._is_fullscreen
        self.attributes("-fullscreen", self._is_fullscreen)

    def _exit_fullscreen(self):
        if self._is_fullscreen:
            self._is_fullscreen = False
            self.attributes("-fullscreen", False)

    def quit_app(self):
        self.destroy()

    # ------------------------------------------------------------------ #
    # Sound effects (best-effort; silently disabled on unsupported platforms)
    # ------------------------------------------------------------------ #
    def play_sound(self, kind: str):
        if not self.sound_enabled:
            return
        try:
            if sys.platform.startswith("win"):
                import winsound

                frequency = 880 if kind == "correct" else 220
                winsound.Beep(frequency, 150)
            else:
                # Fallback for macOS/Linux: terminal bell (non-intrusive, best-effort)
                self.bell()
        except Exception:
            pass  # Sound is a nice-to-have; never let it crash the app


def main():
    os.makedirs(QUESTIONS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)
    app = QuizApp()
    app.mainloop()


if __name__ == "__main__":
    main()
