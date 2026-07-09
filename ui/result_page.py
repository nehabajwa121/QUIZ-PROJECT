"""
ui/result_page.py

Displays the outcome of a completed quiz attempt: score, grade,
correct/wrong counts, and navigation options.
"""

import tkinter as tk
from tkinter import ttk

from utils.helpers import grade_from_percentage, get_random_quote


class ResultPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.result_data = {}
        self._build_ui()

    def _build_ui(self):
        theme = self.controller.theme
        for widget in self.winfo_children():
            widget.destroy()

        card = tk.Frame(
            self,
            bg=theme["card_bg"],
            padx=50,
            pady=35,
            highlightbackground=theme["border"],
            highlightthickness=1,
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        self.card = card
        self._render_content()

    def _render_content(self):
        theme = self.controller.theme
        card = self.card
        for widget in card.winfo_children():
            widget.destroy()

        data = self.result_data
        grade = data.get("grade", "-")
        grade_color = (
            theme["success"] if grade in ("A+", "A", "B") else theme["danger"]
        )

        tk.Label(
            card,
            text="🎉 Quiz Completed!",
            font=("Segoe UI", 22, "bold"),
            bg=theme["card_bg"],
            fg=theme["accent"],
        ).pack(pady=(0, 15))

        tk.Label(
            card,
            text=f"{data.get('player', '')} — {data.get('category', '')}",
            font=("Segoe UI", 13),
            bg=theme["card_bg"],
            fg=theme["muted"],
        ).pack(pady=(0, 20))

        stats_frame = tk.Frame(card, bg=theme["card_bg"])
        stats_frame.pack(pady=(0, 20))

        stats = [
            ("Final Score", data.get("score", 0)),
            ("Correct", data.get("correct", 0)),
            ("Wrong", data.get("wrong", 0)),
            ("Percentage", f"{data.get('percentage', 0)}%"),
        ]
        for i, (label, value) in enumerate(stats):
            box = tk.Frame(stats_frame, bg=theme["bg"], padx=18, pady=12)
            box.grid(row=0, column=i, padx=8)
            tk.Label(
                box, text=str(value), font=("Segoe UI", 16, "bold"),
                bg=theme["bg"], fg=theme["fg"],
            ).pack()
            tk.Label(
                box, text=label, font=("Segoe UI", 9),
                bg=theme["bg"], fg=theme["muted"],
            ).pack()

        tk.Label(
            card,
            text=f"Grade: {grade}",
            font=("Segoe UI", 20, "bold"),
            bg=theme["card_bg"],
            fg=grade_color,
        ).pack(pady=(0, 15))

        tk.Label(
            card,
            text=f"💡 \"{get_random_quote()}\"",
            font=("Segoe UI", 10, "italic"),
            bg=theme["card_bg"],
            fg=theme["muted"],
            wraplength=400,
        ).pack(pady=(0, 25))

        btn_frame = tk.Frame(card, bg=theme["card_bg"])
        btn_frame.pack()

        def make_btn(text, cmd, primary=False):
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=theme["accent"] if primary else theme["bg"],
                fg="white" if primary else theme["fg"],
                relief="flat",
                cursor="hand2",
                padx=18,
                pady=10,
                command=cmd,
            )
            btn.pack(side="left", padx=6)
            return btn

        make_btn(
            "🔁 Play Again",
            lambda: self.controller.start_quiz(data.get("category", "")),
            primary=True,
        )
        make_btn("🏠 Home", lambda: self.controller.show_frame("HomePage"))
        make_btn("🚪 Exit", self.controller.quit_app)

    def show_result(self, result_data: dict):
        self.result_data = result_data
        self._render_content()

    def on_show(self):
        pass

    def refresh_theme(self):
        self._build_ui()
