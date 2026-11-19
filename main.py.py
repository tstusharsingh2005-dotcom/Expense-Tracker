from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Health", "Entertainment", "Other"]


@dataclass
class Expense:
    """One expense record. The date is stored as YYYY-MM-DD text."""

    name: str
    amount: float
    category: str
    date: str


class ExpenseTracker:
    """Owns the expense list, monthly budgets, and JSON file operations."""

    def __init__(self, data_file: str | Path = "data.json") -> None:
        self.data_file = Path(data_file)
        self.expenses: list[Expense] = []
        self.budgets: dict[str, float] = {}
        self.load()

    def load(self) -> None:
        """Read saved data; start with empty records if the file is new."""
        if not self.data_file.exists():
            return
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            self.expenses = [Expense(**item) for item in data.get("expenses", [])]
            self.budgets = {str(k): float(v) for k, v in data.get("budgets", {}).items()}
        except (json.JSONDecodeError, TypeError, ValueError, OSError) as error:
            print(f"Could not read {self.data_file}: {error}")
            print("Starting with empty data. Save a change to create a fresh file.")

    def save(self) -> None:
        """Write records in a readable JSON format."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "expenses": [asdict(expense) for expense in self.expenses],
            "budgets": self.budgets,
        }
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_expense(self, name: str, amount: float, category: str, expense_date: str) -> None:
        self.expenses.append(Expense(name.strip(), round(amount, 2), category, expense_date))
        self.save()

    def update_expense(self, index: int, name: str, amount: float, category: str, expense_date: str) -> None:
        self.expenses[index] = Expense(name.strip(), round(amount, 2), category, expense_date)
        self.save()

    def delete_expense(self, index: int) -> Expense:
        removed = self.expenses.pop(index)
        self.save()
        return removed

    def set_budget(self, month: str, amount: float) -> None:
        self.budgets[month] = round(amount, 2)
        self.save()

    def expenses_for_month(self, month: str) -> list[Expense]:
        return [expense for expense in self.expenses if expense.date.startswith(month)]

    def total(self, expenses: list[Expense] | None = None) -> float:
        records = self.expenses if expenses is None else expenses
        return round(sum(expense.amount for expense in records), 2)


def ask_amount(prompt: str, allow_zero: bool = False) -> float:
    while True:
        try:
            amount = float(input(prompt).replace(",", "").strip())
            if amount < 0 or (amount == 0 and not allow_zero):
                print("Enter an amount greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Enter a valid number, for example 250 or 250.50.")


def ask_date(prompt: str, default_today: bool = False) -> str:
    while True:
        raw = input(prompt).strip()
        if not raw and default_today:
            return date.today().isoformat()
        try:
            return date.fromisoformat(raw).isoformat()
        except ValueError:
            print("Use a real date in YYYY-MM-DD format (for example 2026-10-30).")


def ask_category(current: str | None = None) -> str:
    options = ", ".join(CATEGORIES)
    while True:
        prompt = f"Category ({options})"
        if current:
            prompt += f" [{current}]"
        answer = input(prompt + ": ").strip()
        if not answer and current:
            return current
        match = next((item for item in CATEGORIES if item.casefold() == answer.casefold()), None)
        if match:
            return match
        print("Choose one of the listed categories.")


def show_expenses(expenses: list[Expense]) -> None:
    if not expenses:
        print("No expenses found.")
        return
    print("\n #  Date        Name                     Category          Amount")
    print("-" * 70)
    for number, expense in enumerate(expenses, start=1):
        print(f"{number:>2}  {expense.date:<10}  {expense.name[:23]:<23}  {expense.category:<16} ₹{expense.amount:>9.2f}")
    print(f"\nTotal: ₹{sum(item.amount for item in expenses):.2f}")


def choose_record(tracker: ExpenseTracker) -> int | None:
    show_expenses(tracker.expenses)
    if not tracker.expenses:
        return None
    while True:
        answer = input("Enter the record number (or 0 to cancel): ").strip()
        if answer.isdigit() and 0 <= int(answer) <= len(tracker.expenses):
            return None if int(answer) == 0 else int(answer) - 1
        print("Enter a number from the list, or 0 to cancel.")


def add_expense(tracker: ExpenseTracker) -> None:
    name = input("Expense name: ").strip()
    while not name:
        print("Name cannot be empty.")
        name = input("Expense name: ").strip()
    amount = ask_amount("Amount (₹): ")
    category = ask_category()
    expense_date = ask_date("Date [Enter for today, or YYYY-MM-DD]: ", default_today=True)
    tracker.add_expense(name, amount, category, expense_date)
    print("Expense saved.")


def edit_expense(tracker: ExpenseTracker) -> None:
    index = choose_record(tracker)
    if index is None:
        return
    old = tracker.expenses[index]
    name = input(f"Name [{old.name}]: ").strip() or old.name
    amount_text = input(f"Amount (₹) [{old.amount:.2f}]: ").strip()
    amount = old.amount
    if amount_text:
        try:
            amount = float(amount_text.replace(",", ""))
            if amount <= 0:
                raise ValueError
        except ValueError:
            print("Invalid amount; keeping the previous amount.")
            amount = old.amount
    category = ask_category(old.category)
    date_text = input(f"Date [{old.date}]: ").strip()
    expense_date = old.date
    if date_text:
        try:
            expense_date = date.fromisoformat(date_text).isoformat()
        except ValueError:
            print("Invalid date; keeping the previous date.")
    tracker.update_expense(index, name, amount, category, expense_date)
    print("Expense updated.")


def delete_expense(tracker: ExpenseTracker) -> None:
    index = choose_record(tracker)
    if index is None:
        return
    item = tracker.expenses[index]
    if input(f"Delete '{item.name}' (y/N)? ").strip().casefold() == "y":
        tracker.delete_expense(index)
        print("Expense deleted.")
    else:
        print("Delete cancelled.")


def monthly_report(tracker: ExpenseTracker) -> None:
    month = input("Month (YYYY-MM, Enter for current month): ").strip()
    if not month:
        month = date.today().strftime("%Y-%m")
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Enter the month as YYYY-MM.")
        return
    records = tracker.expenses_for_month(month)
    print(f"\nReport for {month}")
    show_expenses(records)
    spent = tracker.total(records)
    budget = tracker.budgets.get(month)
    if budget is not None:
        remaining = budget - spent
        print(f"Budget: ₹{budget:.2f} | Remaining: ₹{remaining:.2f}")
        if remaining < 0:
            print(f"Over budget by ₹{-remaining:.2f}.")


def category_report(tracker: ExpenseTracker) -> None:
    month = input("Month (YYYY-MM, Enter for all dates): ").strip()
    records = tracker.expenses
    if month:
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            print("Enter the month as YYYY-MM.")
            return
        records = tracker.expenses_for_month(month)
    if not records:
        print("No expenses found.")
        return
    totals: dict[str, float] = {}
    for item in records:
        totals[item.category] = totals.get(item.category, 0) + item.amount
    print("\nSpending by category:")
    for category, amount in sorted(totals.items()):
        print(f"{category:<18} ₹{amount:.2f}")
    print(f"{'TOTAL':<18} ₹{sum(totals.values()):.2f}")


def daily_report(tracker: ExpenseTracker) -> None:
    day = ask_date("Day (YYYY-MM-DD, Enter for today): ", default_today=True)
    show_expenses([item for item in tracker.expenses if item.date == day])


def search_expenses(tracker: ExpenseTracker) -> None:
    term = input("Search name or category: ").strip().casefold()
    matches = [item for item in tracker.expenses if term in item.name.casefold() or term in item.category.casefold()]
    show_expenses(matches)


def budget_menu(tracker: ExpenseTracker) -> None:
    month = input("Budget month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Enter the month as YYYY-MM.")
        return
    amount = ask_amount("Monthly budget (₹): ", allow_zero=True)
    tracker.set_budget(month, amount)
    spent = tracker.total(tracker.expenses_for_month(month))
    print(f"Budget saved. Spent: ₹{spent:.2f}; remaining: ₹{amount - spent:.2f}.")


def main() -> None:
    tracker = ExpenseTracker(Path(__file__).with_name("data.json"))
    actions: dict[str, Any] = {
        "1": lambda: add_expense(tracker),
        "2": lambda: show_expenses(tracker.expenses),
        "3": lambda: search_expenses(tracker),
        "4": lambda: edit_expense(tracker),
        "5": lambda: delete_expense(tracker),
        "6": lambda: daily_report(tracker),
        "7": lambda: monthly_report(tracker),
        "8": lambda: category_report(tracker),
        "9": lambda: budget_menu(tracker),
        "10": lambda: print(f"All-time spending: ₹{tracker.total():.2f}"),
    }
    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add expense       6. Daily report")
        print("2. View expenses     7. Monthly report and budget status")
        print("3. Search expenses   8. Category report")
        print("4. Edit expense      9. Set monthly budget")
        print("5. Delete expense   10. All-time total")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Your expenses are saved. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            try:
                action()
            except OSError as error:
                print(f"Could not save the data: {error}")
        else:
            print("Please choose one of the menu options.")


if __name__ == "__main__":
    main()
