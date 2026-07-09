"""
ui/history_page.py

Displays score history with search, delete, clear-all, and CSV export.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class HistoryPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_entries = []
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
            text="📜 Score History",
            font=("Segoe UI", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"],
        ).pack(side="left", padx=20)

        tk.Button(
            header,
            text="⬇ Export CSV",
            font=("Segoe UI", 9),
            bg=theme["accent"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._export_csv,
        ).pack(side="right")

        tk.Button(
            header,
            text="🗑 Clear All",
            font=("Segoe UI", 9),
            bg=theme["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._clear_all,
        ).pack(side="right", padx=10)

        search_frame = tk.Frame(self, bg=theme["bg"])
        search_frame.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(
            search_frame,
            text="🔍 Search by player:",
            font=("Segoe UI", 10),
            bg=theme["bg"],
            fg=theme["fg"],
        ).pack(side="left")

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side="left", padx=10)
        search_entry.bind("<KeyRelease>", lambda e: self._refresh_data())

        columns = ("date", "player", "category", "score", "percentage")
        style = ttk.Style()
        style.configure(
            "History.Treeview",
            background=theme["card_bg"],
            fieldbackground=theme["card_bg"],
            foreground=theme["fg"],
            rowheight=28,
        )
        self.tree = ttk.Treeview(
            self, columns=columns, show="headings", style="History.Treeview", height=10
        )
        headings = {
            "date": "Date",
            "player": "Player",
            "category": "Category",
            "score": "Score",
            "percentage": "Percentage",
        }
        widths = {"date": 150, "player": 150, "category": 160, "score": 80, "percentage": 100}
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")
        self.tree.pack(fill="both", expand=True, padx=30)

        action_frame = tk.Frame(self, bg=theme["bg"])
        action_frame.pack(pady=15)
        tk.Button(
            action_frame,
            text="Delete Selected",
            font=("Segoe UI", 10),
            bg=theme["danger"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self._delete_selected,
        ).pack()

    def _refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        query = self.search_var.get()
        self.current_entries = self.controller.history_manager.search_by_player(query)
        for entry in self.current_entries:
            self.tree.insert(
                "",
                "end",
                values=(
                    entry.get("date", ""),
                    entry.get("player", ""),
                    entry.get("category", ""),
                    entry.get("score", 0),
                    f"{entry.get('percentage', 0)}%",
                ),
            )

    def _delete_selected(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Select a Row", "Please select a history entry to delete.")
            return
        item = selection[0]
        values = self.tree.item(item, "values")
        # Find the matching entry's real index in the full history (not filtered view)
        all_entries = self.controller.history_manager.all_entries()
        for idx, entry in enumerate(all_entries):
            if (
                entry.get("date") == values[0]
                and entry.get("player") == values[1]
                and entry.get("category") == values[2]
                and str(entry.get("score")) == str(values[3])
            ):
                self.controller.history_manager.delete_entry(idx)
                break
        self._refresh_data()

    def _clear_all(self):
        if messagebox.askyesno("Clear History", "This will delete ALL score history. Continue?"):
            self.controller.history_manager.clear_all()
            self._refresh_data()

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Score History",
        )
        if path:
            success = self.controller.history_manager.export_csv(path)
            if success:
                messagebox.showinfo("Export Complete", f"History exported to:\n{path}")
            else:
                messagebox.showerror("Export Failed", "Could not export history to CSV.")

    def on_show(self):
        self.search_var.set("")
        self._refresh_data()

    def refresh_theme(self):
        self._build_ui()
        self._refresh_data()
