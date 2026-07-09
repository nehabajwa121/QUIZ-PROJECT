"""
ui/leaderboard_page.py

Displays the Top 10 leaderboard entries sorted by score, and allows
resetting the leaderboard.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class LeaderboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        theme = self.controller.theme
        for widget in self.winfo_children():
            widget.destroy()

        header = tk.Frame(self, bg=theme["bg"])
        header.pack(fill="x", padx=20, pady=15)

        tk.Button(
            header,
            text="←  Home",
            font=("Segoe UI", 10),
            bg=theme["bg"],
            fg=theme["muted"],
            relief="flat",
            cursor="hand2",
            command=lambda: self.controller.show_frame("HomePage"),
        ).pack(side="left")

        tk.Label(
            header,
            text="🏆 Leaderboard — Top 10",
            font=("Segoe UI", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="🗑 Reset Leaderboard",
            font=("Segoe UI", 9),
            bg=theme["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._reset,
        ).pack(side="right")

        columns = ("rank", "player", "score", "category", "date")
        style = ttk.Style()
        style.configure(
            "Leaderboard.Treeview",
            background=theme["card_bg"],
            fieldbackground=theme["card_bg"],
            foreground=theme["fg"],
            rowheight=28,
        )
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            style="Leaderboard.Treeview",
            height=10,
        )
        headings = {
            "rank": "Rank",
            "player": "Player",
            "score": "Score",
            "category": "Category",
            "date": "Date",
        }
        widths = {"rank": 60, "player": 180, "score": 80, "category": 160, "date": 160}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def _reset(self):
        if messagebox.askyesno(
            "Reset Leaderboard", "This will permanently clear all leaderboard scores. Continue?"
        ):
            self.controller.leaderboard.reset()
            self._refresh_data()

    def _refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        entries = self.controller.leaderboard.top_scores(10)
        for i, entry in enumerate(entries, start=1):
            self.tree.insert(
                "",
                "end",
                values=(
                    i,
                    entry.get("player", ""),
                    entry.get("score", 0),
                    entry.get("category", ""),
                    entry.get("date", ""),
                ),
            )

    def on_show(self):
        self._refresh_data()

    def refresh_theme(self):
        self._build_ui()
        self._refresh_data()
