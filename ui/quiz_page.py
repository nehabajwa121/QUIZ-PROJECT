"""
ui/quiz_page.py

Contains two frames:
  QuizSetupPage - lets the player pick a category before starting.
  QuizPage      - the live quiz screen with timer, options, and scoring.
"""

import tkinter as tk
from tkinter import ttk

from models.timer import Timer
from models.score_manager import ScoreManager

QUESTION_TIME_SECONDS = 20
AUTO_ADVANCE_DELAY_MS = 1200


class QuizSetupPage(ttk.Frame):
    """Category selection screen shown before a quiz begins."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        theme = self.controller.theme

        back_btn = tk.Button(
            self,
            text="←  Home",
            font=("Segoe UI", 10),
            bg=theme["bg"],
            fg=theme["muted"],
            relief="flat",
            cursor="hand2",
            command=lambda: self.controller.show_frame("HomePage"),
        )
        back_btn.pack(anchor="nw", padx=15, pady=15)

        center = tk.Frame(self, bg=theme["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        title = tk.Label(
            center,
            text="Choose a Category",
            font=("Segoe UI", 22, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
        )
        title.pack(pady=(0, 25))

        icons = {
            "Python": "🐍",
            "General Knowledge": "🌍",
            "Science": "🔬",
            "Mathematics": "➗",
        }

        grid = tk.Frame(center, bg=theme["bg"])
        grid.pack()

        categories = self.controller.question_manager.categories
        for i, category in enumerate(categories):
            count = self.controller.question_manager.question_count(category)
            btn = tk.Button(
                grid,
                text=f"{icons.get(category, '📘')}\n{category}\n({count} questions)",
                font=("Segoe UI", 12, "bold"),
                bg=theme["card_bg"],
                fg=theme["fg"],
                activebackground=theme["accent"],
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=18,
                height=5,
                command=lambda c=category: self._start(c),
            )
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)
            btn.bind(
                "<Enter>", lambda e, b=btn: b.config(bg=theme["accent"], fg="white")
            )
            btn.bind(
                "<Leave>",
                lambda e, b=btn: b.config(bg=theme["card_bg"], fg=theme["fg"]),
            )

    def _start(self, category):
        self.controller.start_quiz(category)

    def on_show(self):
        pass

    def refresh_theme(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()


class QuizPage(ttk.Frame):
    """The live quiz screen: one question at a time, with a countdown timer."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.questions = []
        self.category = ""
        self.current_index = 0
        self.score_manager = None
        self.timer = None
        self.selected_option = None
        self.answer_locked = False
        self.option_buttons = []
        self._build_static_ui()

    # ------------------------------------------------------------------ #
    # UI construction
    # ------------------------------------------------------------------ #
    def _build_static_ui(self):
        theme = self.controller.theme
        for widget in self.winfo_children():
            widget.destroy()

        header = tk.Frame(self, bg=theme["bg"])
        header.pack(fill="x", padx=20, pady=(15, 5))

        self.category_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=theme["bg"],
            fg=theme["accent"],
        )
        self.category_label.pack(side="left")

        self.question_num_label = tk.Label(
            header,
            text="",
            font=("Segoe UI", 12),
            bg=theme["bg"],
            fg=theme["fg"],
        )
        self.question_num_label.pack(side="left", padx=20)

        self.score_label = tk.Label(
            header,
            text="Score: 0",
            font=("Segoe UI", 12, "bold"),
            bg=theme["bg"],
            fg=theme["success"],
        )
        self.score_label.pack(side="right")

        self.pause_btn = tk.Button(
            header,
            text="⏸ Pause",
            font=("Segoe UI", 9),
            bg=theme["card_bg"],
            fg=theme["fg"],
            relief="flat",
            cursor="hand2",
            command=self._toggle_pause,
        )
        self.pause_btn.pack(side="right", padx=15)

        # Progress bar
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=20, pady=(5, 15))

        # Timer display
        self.timer_label = tk.Label(
            self,
            text="⏱ 20s",
            font=("Segoe UI", 16, "bold"),
            bg=theme["bg"],
            fg=theme["danger"],
        )
        self.timer_label.pack(pady=(0, 10))

        # Question card
        self.question_card = tk.Frame(
            self,
            bg=theme["card_bg"],
            padx=30,
            pady=25,
            highlightbackground=theme["border"],
            highlightthickness=1,
        )
        self.question_card.pack(fill="x", padx=40)

        self.question_label = tk.Label(
            self.question_card,
            text="",
            font=("Segoe UI", 15, "bold"),
            bg=theme["card_bg"],
            fg=theme["fg"],
            wraplength=700,
            justify="left",
        )
        self.question_label.pack(anchor="w")

        # Options
        self.options_frame = tk.Frame(self, bg=theme["bg"])
        self.options_frame.pack(fill="both", expand=True, padx=40, pady=20)

        self.pause_overlay = None

        nav_frame = tk.Frame(self, bg=theme["bg"])
        nav_frame.pack(pady=(0, 15))

        self.next_btn = tk.Button(
            nav_frame,
            text="Next  →",
            font=("Segoe UI", 12, "bold"),
            bg=theme["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=25,
            pady=8,
            state="disabled",
            command=self._go_next,
        )
        self.next_btn.pack()

    # ------------------------------------------------------------------ #
    # Quiz lifecycle
    # ------------------------------------------------------------------ #
    def start(self, category: str):
        self._build_static_ui()
        self.category = category
        self.questions = self.controller.question_manager.load_questions(
            category, shuffle=True
        )
        self.current_index = 0
        self.score_manager = ScoreManager(total_questions=len(self.questions))
        self.progress.config(maximum=max(len(self.questions), 1), value=0)
        self.category_label.config(text=f"📘 {category}")
        if not self.questions:
            self.question_label.config(
                text="No questions available for this category yet."
            )
            return
        self._load_question()

    def _load_question(self):
        self.answer_locked = False
        self.selected_option = None
        self.next_btn.config(state="disabled")

        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.option_buttons = []

        question = self.questions[self.current_index]
        self.question_num_label.config(
            text=f"Question {self.current_index + 1} of {len(self.questions)}"
        )
        self.question_label.config(text=question["question"])
        self.progress.config(value=self.current_index)
        self.score_label.config(text=f"Score: {self.score_manager.score}")

        theme = self.controller.theme
        for option in question["options"]:
            btn = tk.Button(
                self.options_frame,
                text=option,
                font=("Segoe UI", 12),
                bg=theme["card_bg"],
                fg=theme["fg"],
                activebackground=theme["accent"],
                relief="flat",
                cursor="hand2",
                wraplength=600,
                justify="left",
                anchor="w",
                padx=20,
                pady=14,
                command=lambda o=option: self._submit_answer(o),
            )
            btn.pack(fill="x", pady=6)
            self.option_buttons.append(btn)
            btn.bind(
                "<Enter>",
                lambda e, b=btn: b.config(bg=theme["accent"], fg="white")
                if not self.answer_locked
                else None,
            )
            btn.bind(
                "<Leave>",
                lambda e, b=btn: b.config(bg=theme["card_bg"], fg=theme["fg"])
                if not self.answer_locked
                else None,
            )

        self.timer = Timer(
            self,
            QUESTION_TIME_SECONDS,
            on_tick=self._update_timer,
            on_timeout=self._handle_timeout,
        )
        self.timer.start()

    def _update_timer(self, remaining: int):
        self.timer_label.config(text=f"⏱ {remaining}s")
        theme = self.controller.theme
        if remaining <= 5:
            self.timer_label.config(fg=theme["danger"])
        else:
            self.timer_label.config(fg=theme["fg"])

    def _handle_timeout(self):
        if self.answer_locked:
            return
        self.answer_locked = True
        self.score_manager.record_skipped()
        self._reveal_correct_answer(None)
        self.next_btn.config(state="normal")
        self.after(AUTO_ADVANCE_DELAY_MS, self._go_next)

    def _submit_answer(self, chosen: str):
        if self.answer_locked:
            return
        self.answer_locked = True
        self.selected_option = chosen
        if self.timer:
            self.timer.stop()

        question = self.questions[self.current_index]
        correct_answer = question["answer"]

        if chosen == correct_answer:
            self.score_manager.record_correct()
            self.controller.play_sound("correct")
        else:
            self.score_manager.record_wrong()
            self.controller.play_sound("wrong")

        self._reveal_correct_answer(chosen)
        self.score_label.config(text=f"Score: {self.score_manager.score}")
        self.next_btn.config(state="normal")
        self.after(AUTO_ADVANCE_DELAY_MS, self._go_next)

    def _reveal_correct_answer(self, chosen):
        theme = self.controller.theme
        question = self.questions[self.current_index]
        correct_answer = question["answer"]

        for btn in self.option_buttons:
            option_text = btn.cget("text")
            btn.config(state="disabled")
            if option_text == correct_answer:
                btn.config(bg=theme["success"], fg="white")
            elif option_text == chosen:
                btn.config(bg=theme["danger"], fg="white")
            else:
                btn.config(bg=theme["card_bg"], fg=theme["muted"])

    def _go_next(self):
        if self.timer:
            self.timer.stop()
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self.progress.config(value=len(self.questions))
            self.controller.finish_quiz(self.category, self.score_manager)
        else:
            self._load_question()

    def _toggle_pause(self):
        if not self.timer:
            return
        if self.timer.is_paused:
            self.timer.resume()
            self.pause_btn.config(text="⏸ Pause")
            if self.pause_overlay:
                self.pause_overlay.destroy()
                self.pause_overlay = None
        else:
            self.timer.pause()
            self.pause_btn.config(text="▶ Resume")
            theme = self.controller.theme
            self.pause_overlay = tk.Label(
                self.question_card,
                text="⏸ Paused",
                font=("Segoe UI", 12, "italic"),
                bg=theme["card_bg"],
                fg=theme["muted"],
            )
            self.pause_overlay.pack(pady=(10, 0))

    def on_show(self):
        pass

    def refresh_theme(self):
        # Rebuild static chrome; if a quiz is in progress, reload current question
        had_quiz = bool(self.questions)
        current_idx = self.current_index
        self._build_static_ui()
        if had_quiz and current_idx < len(self.questions):
            self.category_label.config(text=f"📘 {self.category}")
            self.progress.config(maximum=max(len(self.questions), 1))
            self.current_index = current_idx
            self._load_question()
