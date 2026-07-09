"""
ui/question_editor.py

Screen for adding new questions to any category, with validation
against empty fields and duplicate questions.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class QuestionEditorPage(ttk.Frame):
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
            text="➕ Add a New Question",
            font=("Segoe UI", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
        ).pack(side="left", padx=20)

        card = tk.Frame(
            self,
            bg=theme["card_bg"],
            padx=40,
            pady=30,
            highlightbackground=theme["border"],
            highlightthickness=1,
        )
        card.pack(padx=40, pady=(0, 20), fill="both", expand=True)

        # Category selector
        tk.Label(
            card, text="Category", font=("Segoe UI", 10, "bold"),
            bg=theme["card_bg"], fg=theme["fg"],
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.category_var = tk.StringVar(
            value=self.controller.question_manager.categories[0]
        )
        category_menu = ttk.Combobox(
            card,
            textvariable=self.category_var,
            values=self.controller.question_manager.categories,
            state="readonly",
            width=30,
        )
        category_menu.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Question text
        tk.Label(
            card, text="Question", font=("Segoe UI", 10, "bold"),
            bg=theme["card_bg"], fg=theme["fg"],
        ).grid(row=2, column=0, sticky="w", pady=(0, 5))
        self.question_var = tk.StringVar()
        ttk.Entry(card, textvariable=self.question_var, width=60).grid(
            row=3, column=0, columnspan=2, sticky="we", pady=(0, 15)
        )

        # Options
        self.option_vars = []
        for i in range(4):
            tk.Label(
                card, text=f"Option {i + 1}", font=("Segoe UI", 10, "bold"),
                bg=theme["card_bg"], fg=theme["fg"],
            ).grid(row=4 + i, column=0, sticky="w", pady=(0, 5))
            var = tk.StringVar()
            ttk.Entry(card, textvariable=var, width=40).grid(
                row=4 + i, column=1, sticky="w", padx=(10, 0), pady=(0, 5)
            )
            self.option_vars.append(var)

        # Correct answer selector
        tk.Label(
            card, text="Correct Answer", font=("Segoe UI", 10, "bold"),
            bg=theme["card_bg"], fg=theme["fg"],
        ).grid(row=8, column=0, sticky="w", pady=(15, 5))
        self.correct_var = tk.StringVar()
        self.correct_menu = ttk.Combobox(
            card, textvariable=self.correct_var, values=[], state="readonly", width=30
        )
        self.correct_menu.grid(row=9, column=0, columnspan=2, sticky="w", pady=(0, 15))

        refresh_btn = tk.Button(
            card,
            text="🔄 Sync Options → Correct Answer List",
            font=("Segoe UI", 9),
            bg=theme["bg"],
            fg=theme["fg"],
            relief="flat",
            cursor="hand2",
            command=self._sync_options,
        )
        refresh_btn.grid(row=10, column=0, columnspan=2, sticky="w", pady=(0, 15))

        self.status_label = tk.Label(
            card, text="", font=("Segoe UI", 9), bg=theme["card_bg"], fg=theme["danger"]
        )
        self.status_label.grid(row=11, column=0, columnspan=2, sticky="w")

        save_btn = tk.Button(
            card,
            text="💾 Save Question",
            font=("Segoe UI", 12, "bold"),
            bg=theme["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self._save,
        )
        save_btn.grid(row=12, column=0, columnspan=2, pady=(15, 0), sticky="w")

    def _sync_options(self):
        options = [v.get().strip() for v in self.option_vars if v.get().strip()]
        self.correct_menu.config(values=options)
        if options:
            self.correct_var.set(options[0])

    def _save(self):
        category = self.category_var.get()
        question_text = self.question_var.get()
        options = [v.get() for v in self.option_vars]
        correct_answer = self.correct_var.get()

        error = self.controller.question_manager.add_question(
            category, question_text, options, correct_answer
        )
        if error:
            self.status_label.config(text=f"⚠ {error}")
            return

        self.status_label.config(text="")
        messagebox.showinfo("Question Saved", "Your question has been added successfully!")
        self.question_var.set("")
        for v in self.option_vars:
            v.set("")
        self.correct_var.set("")
        self.correct_menu.config(values=[])

    def on_show(self):
        pass

    def refresh_theme(self):
        self._build_ui()
