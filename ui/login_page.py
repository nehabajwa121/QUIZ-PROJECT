"""
ui/login_page.py

The first screen shown to the user. Collects and validates the player's name.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from utils.helpers import Theme


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        wrapper = tk.Frame(self, bg=self.controller.theme["bg"])
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(
            wrapper,
            bg=self.controller.theme["card_bg"],
            padx=50,
            pady=40,
            highlightbackground=self.controller.theme["border"],
            highlightthickness=1,
        )
        card.pack()

        title = tk.Label(
            card,
            text="🎓 Quiz Master",
            font=("Segoe UI", 28, "bold"),
            bg=self.controller.theme["card_bg"],
            fg=self.controller.theme["accent"],
        )
        title.pack(pady=(0, 5))

        subtitle = tk.Label(
            card,
            text="Test your knowledge across multiple categories",
            font=("Segoe UI", 11),
            bg=self.controller.theme["card_bg"],
            fg=self.controller.theme["muted"],
        )
        subtitle.pack(pady=(0, 25))

        name_label = tk.Label(
            card,
            text="Enter your name to begin",
            font=("Segoe UI", 11, "bold"),
            bg=self.controller.theme["card_bg"],
            fg=self.controller.theme["fg"],
        )
        name_label.pack(anchor="w")

        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            card, textvariable=self.name_var, font=("Segoe UI", 12), width=28
        )
        self.name_entry.pack(pady=(8, 5), ipady=6)
        self.name_entry.bind("<Return>", lambda e: self._submit())

        self.error_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9),
            bg=self.controller.theme["card_bg"],
            fg=self.controller.theme["danger"],
        )
        self.error_label.pack(anchor="w", pady=(0, 10))

        continue_btn = tk.Button(
            card,
            text="Continue  →",
            font=("Segoe UI", 12, "bold"),
            bg=self.controller.theme["accent"],
            fg="white",
            activebackground=self.controller.theme["accent_hover"],
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._submit,
        )
        continue_btn.pack(fill="x", pady=(10, 0))
        self._add_hover(continue_btn)

        self._card = card
        self._wrapper = wrapper

    def _add_hover(self, button):
        normal = self.controller.theme["accent"]
        hover = self.controller.theme["accent_hover"]
        button.bind("<Enter>", lambda e: button.config(bg=hover))
        button.bind("<Leave>", lambda e: button.config(bg=normal))

    def _submit(self):
        name = self.name_var.get().strip()
        if not name:
            self.error_label.config(text="⚠ Name cannot be empty.")
            return
        self.error_label.config(text="")
        self.controller.set_player_name(name)
        self.controller.show_frame("HomePage")

    def on_show(self):
        """Called whenever this frame becomes visible."""
        self.name_entry.focus_set()

    def refresh_theme(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui()
