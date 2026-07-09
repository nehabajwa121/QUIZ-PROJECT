"""
ui/home_page.py

The main menu screen with navigation buttons to all major features.
"""

import tkinter as tk
from tkinter import ttk


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        theme = self.controller.theme
        self.configure(style="Home.TFrame")

        top_bar = tk.Frame(self, bg=theme["bg"])
        top_bar.pack(fill="x", padx=20, pady=(15, 0))

        self.greeting_label = tk.Label(
            top_bar,
            text=f"👋 Welcome, {self.controller.player_name or 'Guest'}!",
            font=("Segoe UI", 14, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
        )
        self.greeting_label.pack(side="left")

        theme_btn = tk.Button(
            top_bar,
            text="🌙 Dark Mode" if not self.controller.dark_mode else "☀ Light Mode",
            font=("Segoe UI", 9),
            bg=theme["card_bg"],
            fg=theme["fg"],
            relief="flat",
            cursor="hand2",
            command=self.controller.toggle_theme,
        )
        theme_btn.pack(side="right")

        fullscreen_btn = tk.Button(
            top_bar,
            text="⛶ Fullscreen",
            font=("Segoe UI", 9),
            bg=theme["card_bg"],
            fg=theme["fg"],
            relief="flat",
            cursor="hand2",
            command=self.controller.toggle_fullscreen,
        )
        fullscreen_btn.pack(side="right", padx=(0, 10))

        center = tk.Frame(self, bg=theme["bg"])
        center.place(relx=0.5, rely=0.52, anchor="center")

        title = tk.Label(
            center,
            text="🎓 Quiz Master",
            font=("Segoe UI", 30, "bold"),
            bg=theme["bg"],
            fg=theme["accent"],
        )
        title.pack(pady=(0, 30))

        buttons = [
            ("▶  Start Quiz", "QuizSetup"),
            ("🏆  Leaderboard", "Leaderboard"),
            ("📜  Score History", "History"),
            ("➕  Add Questions", "QuestionEditor"),
            ("🚪  Exit", None),
        ]

        for text, target in buttons:
            btn = tk.Button(
                center,
                text=text,
                font=("Segoe UI", 13, "bold"),
                bg=theme["card_bg"],
                fg=theme["fg"],
                activebackground=theme["accent"],
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                width=26,
                pady=12,
                command=(
                    self.controller.quit_app
                    if target is None
                    else (lambda t=target: self.controller.show_frame(t))
                ),
            )
            btn.pack(pady=6)
            self._add_hover(btn, theme)

    def _add_hover(self, button, theme):
        button.bind("<Enter>", lambda e: button.config(bg=theme["accent"], fg="white"))
        button.bind(
            "<Leave>", lambda e: button.config(bg=theme["card_bg"], fg=theme["fg"])
        )

    def on_show(self):
        self.greeting_label.config(
            text=f"👋 Welcome, {self.controller.player_name or 'Guest'}!"
        )

    def refresh_theme(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
