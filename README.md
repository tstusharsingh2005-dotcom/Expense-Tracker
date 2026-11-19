# Personal Expense Tracker

A beginner-friendly Python console app for recording expenses, organizing them into categories, tracking monthly budgets, and viewing reports. It uses only Python's standard library.

## Project files

```text
expense-tracker/
├── main.py          # menu, input prompts, tracker class, reports
├── data.json        # created automatically when you save the first change
├── test_tracker.py  # automated checks
└── README.md
```

## Run it in VS Code

1. Install Python 3.10 or newer and open this folder in VS Code.
2. Open `main.py`. If VS Code prompts you, install the Microsoft Python extension and select your Python interpreter.
3. Open **Terminal → New Terminal**.
4. Run `python main.py` (on some Windows installations, use `py main.py`).
5. Choose a menu number. The app creates `data.json` beside `main.py` and saves after each change. Keep that file to preserve your expenses.

## Features

- Add expenses with a name, amount, category, and date. Press Enter for today's date.
- View, search, edit, and delete records. Delete asks for confirmation.
- Set budgets by month and see spending, remaining budget, or amount over budget.
- Daily, monthly, category, and all-time reports.
- Checks amounts, dates, categories, menu choices, and required names.
- Saves records and budgets in readable JSON.

Dates use `YYYY-MM-DD`; budget and report months use `YYYY-MM`. Categories are Food, Travel, Bills, Shopping, Health, Entertainment, and Other. Edit prompts keep the existing value when you press Enter.

## How the code is organized

- `Expense` is a **dataclass**: one expense record with a name, amount, category, and date.
- `ExpenseTracker` is a **class** that owns the list of expenses and a dictionary of monthly budgets. Its methods load, save, add, update, delete, and calculate totals.
- `expenses` is a **list** because it holds any number of expense records. `budgets` is a **dictionary** because a month (such as `2026-10`) maps directly to its budget amount.
- Small **functions** handle prompts, validation, displaying tables, and reports. The main loop prints the menu and calls the selected function.
- `data.json` is plain text in JSON format. You can back it up by copying the file.

## Run the checks

From this folder, run:

```text
python -m unittest -v
```

The tests use temporary files, so they do not change your personal `data.json`.

## Reset your data

Exit the app and remove or rename `data.json`. The next run starts with an empty tracker. Make a backup first if you may want those records later.
