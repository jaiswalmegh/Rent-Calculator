
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1020"
PANEL = "#121A2D"
BORDER = "#263653"
TEXT = "#F4F7FF"
MUTED = "#9AAAC5"
CYAN = "#41D9FF"
PURPLE = "#9B8CFF"
GREEN = "#4DE0B0"
ORANGE = "#FFBE6B"


class RentCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NESTWISE | Shared Rent Calculator")
        self.geometry("1100x800")
        self.minsize(900, 650)
        self.configure(fg_color=BG)

        self.members = []
        self.expenses = []
        self.summary = []

        self.build_ui()

        self.add_member("Roommate 1")
        self.add_member("Roommate 2")

        for name, category in [
            ("Monthly Rent", "Rent"),
            ("Electricity", "Utilities"),
            ("Water", "Utilities"),
            ("Internet", "Utilities"),
            ("Shared Groceries", "Shared"),
        ]:
            self.add_expense(name, category)

        self.calculate()

    def label(self, parent, text, size=12,
              color=TEXT, bold=False):
        return ctk.CTkLabel(
            parent,
            text=text,
            text_color=color,
            font=ctk.CTkFont(
                "Segoe UI", size,
                "bold" if bold else "normal"
            )
        )

    def card(self, parent, accent=BORDER):
        return ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=16,
            border_width=1,
            border_color=accent
        )

    def build_ui(self):
        self.main = ctk.CTkScrollableFrame(
            self,
            fg_color=BG,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=CYAN
        )
        self.main.pack(fill="both", expand=True)

        # HEADER
        header = ctk.CTkFrame(
            self.main, fg_color="transparent"
        )
        header.pack(fill="x", padx=28, pady=(24, 20))

        left = ctk.CTkFrame(
            header, fg_color="transparent"
        )
        left.pack(side="left", fill="x", expand=True)

        self.label(
            left, "✦  N E S T W I S E",
            12, CYAN, True
        ).pack(anchor="w")

        self.label(
            left, "Shared Rent Calculator",
            28, TEXT, True
        ).pack(anchor="w", pady=(6, 2))

        self.label(
            left,
            "Split the bills. Keep the house harmony.",
            13, MUTED
        ).pack(anchor="w")

        self.month_var = tk.StringVar(
            value=datetime.now().strftime("%B %Y")
        )
        ctk.CTkEntry(
            header,
            textvariable=self.month_var,
            width=155,
            height=38,
            corner_radius=10,
            border_color=BORDER,
            fg_color=PANEL,
            text_color=TEXT
        ).pack(side="right", pady=12)

        # MEMBERS
        self.members_card = self.card(self.main)
        self.members_card.pack(
            fill="x", padx=28, pady=(0, 16)
        )

        top = ctk.CTkFrame(
            self.members_card, fg_color="transparent"
        )
        top.pack(fill="x", padx=18, pady=(18, 10))

        self.label(
            top, "01  /  HOUSEHOLD MEMBERS",
            11, CYAN, True
        ).pack(side="left")

        ctk.CTkButton(
            top, text="+ Add member",
            width=125, height=32,
            fg_color="#20344D",
            hover_color="#2B496A",
            command=lambda: self.add_member()
        ).pack(side="right")

        self.members_container = ctk.CTkFrame(
            self.members_card, fg_color="transparent"
        )
        self.members_container.pack(
            fill="x", padx=18, pady=(0, 18)
        )

        # EXPENSES
        self.expenses_card = self.card(self.main)
        self.expenses_card.pack(
            fill="x", padx=28, pady=(0, 16)
        )

        top = ctk.CTkFrame(
            self.expenses_card, fg_color="transparent"
        )
        top.pack(fill="x", padx=18, pady=(18, 10))

        self.label(
            top, "02  /  MONTHLY EXPENSES",
            11, CYAN, True
        ).pack(side="left")

        ctk.CTkButton(
            top, text="+ Add expense",
            width=125, height=32,
            fg_color="#20344D",
            hover_color="#2B496A",
            command=lambda: self.add_expense()
        ).pack(side="right")

        self.expenses_container = ctk.CTkFrame(
            self.expenses_card, fg_color="transparent"
        )
        self.expenses_container.pack(
            fill="x", padx=18, pady=(0, 18)
        )

        # SPLIT METHOD
        rule_card = self.card(self.main)
        rule_card.pack(
            fill="x", padx=28, pady=(0, 16)
        )

        rule_top = ctk.CTkFrame(
            rule_card, fg_color="transparent"
        )
        rule_top.pack(fill="x", padx=18, pady=(16, 8))

        self.label(
            rule_top, "03  /  SPLIT METHOD",
            11, PURPLE, True
        ).pack(side="left")

        self.split_var = tk.StringVar(
            value="Equal split"
        )

        ctk.CTkOptionMenu(
            rule_top,
            values=["Equal split", "Custom percentages"],
            variable=self.split_var,
            fg_color="#263653",
            button_color="#354B70",
            button_hover_color="#45618E",
            command=lambda _value: self.on_split_change()
        ).pack(side="right")

        self.split_hint = self.label(
            rule_card,
            "Expenses are divided equally among all members.",
            12, MUTED
        )
        self.split_hint.pack(
            anchor="w", padx=18, pady=(0, 16)
        )

        # CALCULATE
        ctk.CTkButton(
            self.main,
            text="CALCULATE HOUSEHOLD SHARE   ↗",
            command=self.calculate,
            height=46,
            corner_radius=12,
            fg_color=CYAN,
            hover_color="#22BFE8",
            text_color="#07111F",
            font=ctk.CTkFont("Segoe UI", 13, "bold")
        ).pack(fill="x", padx=28, pady=(0, 16))

        # RESULTS
        self.summary_card = self.card(self.main)
        self.summary_card.pack(
            fill="x", padx=28, pady=(0, 16)
        )

        top = ctk.CTkFrame(
            self.summary_card, fg_color="transparent"
        )
        top.pack(fill="x", padx=18, pady=(18, 10))

        self.label(
            top, "04  /  PAYMENT BREAKDOWN",
            11, GREEN, True
        ).pack(side="left")

        ctk.CTkButton(
            top, text="Export CSV ↓",
            width=110, height=32,
            fg_color="#164638",
            hover_color="#21624F",
            command=self.export_csv
        ).pack(side="right")

        self.total_label = self.label(
            self.summary_card,
            "Total household expenses: ₹0.00",
            20, TEXT, True
        )
        self.total_label.pack(
            anchor="w", padx=18, pady=(4, 14)
        )

        self.summary_container = ctk.CTkFrame(
            self.summary_card, fg_color="transparent"
        )
        self.summary_container.pack(
            fill="x", padx=18, pady=(0, 18)
        )

        self.label(
            self.main,
            "NESTWISE  •  SMART HOUSEHOLD BUDGETING",
            10, "#52617C", True
        ).pack(pady=(0, 20))

    # MEMBER MANAGEMENT
    def add_member(self, name=""):
        self.members.append({
            "name": tk.StringVar(value=name),
            "percent": tk.StringVar(value="")
        })
        self.refresh_members()
        self.calculate()

    def remove_member(self, member):
        if len(self.members) <= 1:
            messagebox.showwarning(
                "Member required",
                "At least one member must remain."
            )
            return

        self.members.remove(member)
        self.refresh_members()
        self.calculate()

    def refresh_members(self):
        for widget in self.members_container.winfo_children():
            widget.destroy()

        for index, member in enumerate(self.members):
            row = ctk.CTkFrame(
                self.members_container,
                fg_color="#0F1728",
                corner_radius=10
            )
            row.pack(fill="x", pady=4)

            self.label(
                row, f"{index + 1:02d}",
                11, MUTED, True
            ).pack(side="left", padx=(12, 8), pady=9)

            ctk.CTkEntry(
                row,
                textvariable=member["name"],
                placeholder_text="Member name",
                height=35,
                border_color=BORDER,
                fg_color=PANEL
            ).pack(
                side="left", fill="x", expand=True,
                padx=5, pady=7
            )

            if self.split_var.get() == "Custom percentages":
                ctk.CTkEntry(
                    row,
                    textvariable=member["percent"],
                    placeholder_text="Share %",
                    width=100,
                    height=35,
                    border_color=BORDER,
                    fg_color=PANEL
                ).pack(side="left", padx=5, pady=7)

            ctk.CTkButton(
                row, text="×", width=34, height=32,
                fg_color="#482637",
                hover_color="#70334B",
                command=lambda m=member: self.remove_member(m)
            ).pack(side="right", padx=8, pady=7)

    # EXPENSE MANAGEMENT
    def add_expense(self, name="", category="Shared"):
        self.expenses.append({
            "name": tk.StringVar(value=name),
            "category": tk.StringVar(value=category),
            "amount": tk.StringVar(value="0.00")
        })
        self.refresh_expenses()
        self.calculate()

    def remove_expense(self, expense):
        self.expenses.remove(expense)
        self.refresh_expenses()
        self.calculate()

    def refresh_expenses(self):
        for widget in self.expenses_container.winfo_children():
            widget.destroy()

        for expense in self.expenses:
            row = ctk.CTkFrame(
                self.expenses_container,
                fg_color="#0F1728",
                corner_radius=10
            )
            row.pack(fill="x", pady=4)

            ctk.CTkEntry(
                row,
                textvariable=expense["name"],
                placeholder_text="Expense name",
                height=35,
                border_color=BORDER,
                fg_color=PANEL
            ).pack(
                side="left", fill="x", expand=True,
                padx=(8, 5), pady=7
            )

            ctk.CTkOptionMenu(
                row,
                variable=expense["category"],
                values=["Rent", "Utilities", "Shared", "Other"],
                width=120,
                height=35,
                fg_color="#263653",
                button_color="#354B70"
            ).pack(side="left", padx=5, pady=7)

            ctk.CTkEntry(
                row,
                textvariable=expense["amount"],
                placeholder_text="Amount ₹",
                width=130,
                height=35,
                border_color=BORDER,
                fg_color=PANEL
            ).pack(side="left", padx=5, pady=7)

            ctk.CTkButton(
                row, text="×", width=34, height=32,
                fg_color="#482637",
                hover_color="#70334B",
                command=lambda e=expense: self.remove_expense(e)
            ).pack(side="right", padx=8, pady=7)

    def on_split_change(self):
        custom = self.split_var.get() == "Custom percentages"

        self.split_hint.configure(
            text=(
                "Enter each member's percentage. Shares must total 100%."
                if custom else
                "Expenses are divided equally among all members."
            )
        )

        self.refresh_members()
        self.calculate()

    # VALIDATION AND CALCULATION
    def get_data(self):
        if not self.members:
            raise ValueError("Add at least one member.")

        names = [
            member["name"].get().strip()
            for member in self.members
        ]

        if any(not name for name in names):
            raise ValueError("Every member needs a name.")

        if len({name.casefold() for name in names}) != len(names):
            raise ValueError("Member names must be unique.")

        expenses = []

        for expense in self.expenses:
            name = expense["name"].get().strip()

            if not name:
                raise ValueError("Every expense needs a name.")

            try:
                amount = float(
                    expense["amount"].get().strip() or "0"
                )
            except ValueError:
                raise ValueError(f"Invalid amount for {name}.")

            if amount < 0:
                raise ValueError("Amounts cannot be negative.")

            expenses.append((
                name,
                expense["category"].get(),
                amount
            ))

        if self.split_var.get() == "Equal split":
            shares = [1 / len(names)] * len(names)
        else:
            percentages = []

            for member in self.members:
                try:
                    value = float(member["percent"].get().strip())
                except ValueError:
                    raise ValueError(
                        f"Enter a percentage for "
                        f"{member['name'].get()}."
                    )

                if not 0 <= value <= 100:
                    raise ValueError(
                        "Percentages must be between 0 and 100."
                    )

                percentages.append(value)

            if abs(sum(percentages) - 100) > 0.01:
                raise ValueError(
                    f"Shares total {sum(percentages):.2f}%. "
                    "They must total 100%."
                )

            shares = [p / 100 for p in percentages]

        return names, expenses, shares

    def calculate(self):
        try:
            names, expenses, shares = self.get_data()
        except ValueError as error:
            self.total_label.configure(
                text="Please check your names, amounts and shares."
            )
            self.render_summary([])
            self.last_error = str(error)
            return

        total = sum(amount for _, _, amount in expenses)
        self.summary = []

        for name, share in zip(names, shares):
            breakdown = [
                (expense_name, category, amount * share)
                for expense_name, category, amount in expenses
            ]

            self.summary.append({
                "name": name,
                "percentage": share * 100,
                "total": sum(item[2] for item in breakdown),
                "breakdown": breakdown
            })

        self.total_label.configure(
            text=f"Total household expenses: ₹{total:,.2f}"
        )

        self.render_summary(self.summary)

    def render_summary(self, summary):
        for widget in self.summary_container.winfo_children():
            widget.destroy()

        if not summary:
            self.label(
                self.summary_container,
                "Enter valid details to view payment breakdown.",
                12, MUTED
            ).pack(anchor="w", pady=8)
            return

        for member in summary:
            card = ctk.CTkFrame(
                self.summary_container,
                fg_color="#0F1728",
                corner_radius=12
            )
            card.pack(fill="x", pady=5)

            top = ctk.CTkFrame(
                card, fg_color="transparent"
            )
            top.pack(fill="x", padx=14, pady=(12, 6))

            self.label(
                top, member["name"], 15, TEXT, True
            ).pack(side="left")

            self.label(
                top,
                f'{member["percentage"]:.2f}%  •  '
                f'₹{member["total"]:,.2f}',
                14, GREEN, True
            ).pack(side="right")

            for name, category, amount in member["breakdown"]:
                line = ctk.CTkFrame(
                    card, fg_color="transparent"
                )
                line.pack(fill="x", padx=14, pady=2)

                self.label(
                    line, f"{name} · {category}",
                    11, MUTED
                ).pack(side="left")

                self.label(
                    line, f"₹{amount:,.2f}",
                    11, TEXT
                ).pack(side="right")

            ctk.CTkFrame(
                card, height=8, fg_color="transparent"
            ).pack()

    # CSV EXPORT
    def export_csv(self):
        if not self.summary:
            messagebox.showwarning(
                "Nothing to export",
                "Calculate a valid breakdown first."
            )
            return

        filename = filedialog.asksaveasfilename(
            title="Export payment summary",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="nestwise_rent_summary.csv"
        )

        if not filename:
            return

        try:
            with open(
                filename, "w",
                newline="", encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)

                writer.writerow(["NESTWISE - Rent Summary"])
                writer.writerow(["Month", self.month_var.get().strip()])
                writer.writerow([])
                writer.writerow([
                    "Member", "Share %",
                    "Expense", "Category", "Amount (INR)"
                ])

                for member in self.summary:
                    for name, category, amount in member["breakdown"]:
                        writer.writerow([
                            member["name"],
                            f'{member["percentage"]:.2f}%',
                            name, category, f"{amount:.2f}"
                        ])

                    writer.writerow([
                        member["name"],
                        f'{member["percentage"]:.2f}%',
                        "TOTAL", "", f'{member["total"]:.2f}'
                    ])
                    writer.writerow([])

                writer.writerow([
                    "HOUSEHOLD TOTAL", "", "", "",
                    f"{sum(m['total'] for m in self.summary):.2f}"
                ])

            messagebox.showinfo(
                "Export successful",
                f"Summary saved to:\n{filename}"
            )

        except OSError as error:
            messagebox.showerror(
                "Export failed", str(error)
            )


if __name__ == "__main__":
    app = RentCalculator()
    app.mainloop()
