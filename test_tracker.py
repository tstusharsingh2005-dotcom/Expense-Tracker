import json
import tempfile
import unittest
from pathlib import Path

from main import Expense, ExpenseTracker


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "data.json"
        self.tracker = ExpenseTracker(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_update_delete_and_total(self):
        self.tracker.add_expense("Lunch", 125.5, "Food", "2026-10-30")
        self.tracker.add_expense("Bus", 30, "Travel", "2026-10-30")
        self.assertEqual(self.tracker.total(), 155.5)
        self.tracker.update_expense(0, "Dinner", 150, "Food", "2026-10-29")
        self.assertEqual(self.tracker.expenses[0].name, "Dinner")
        removed = self.tracker.delete_expense(1)
        self.assertEqual(removed.name, "Bus")
        self.assertEqual(self.tracker.total(), 150)

    def test_json_persistence_and_monthly_budget(self):
        self.tracker.add_expense("Rent", 12000, "Bills", "2026-10-01")
        self.tracker.set_budget("2026-10", 15000)
        reloaded = ExpenseTracker(self.data_file)
        self.assertEqual(reloaded.expenses, [Expense("Rent", 12000, "Bills", "2026-10-01")])
        self.assertEqual(reloaded.budgets["2026-10"], 15000)
        self.assertEqual(reloaded.total(reloaded.expenses_for_month("2026-10")), 12000)

    def test_json_contains_both_collections(self):
        self.tracker.set_budget("2026-11", 5000)
        data = json.loads(self.data_file.read_text(encoding="utf-8"))
        self.assertEqual(data["expenses"], [])
        self.assertEqual(data["budgets"]["2026-11"], 5000)


if __name__ == "__main__":
    unittest.main()
