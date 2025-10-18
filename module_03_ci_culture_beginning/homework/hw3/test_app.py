import unittest
from app import app, storage

class FinanceAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        storage.clear()
        storage.update({
            "20250101": 1000,
            "20250102": 500,
            "20250105": 200
        })
        cls.client = app.test_client()

    def setUp(self):
        storage.clear()
        storage.update({
            "20250101": 1000,
            "20250102": 500,
            "20250105": 200
        })

    def test_add_valid_entry(self):
        response = self.client.post("/add/", json={"date": "20250110", "amount": 300})
        self.assertEqual(response.status_code, 200)
        self.assertIn("20250110", storage)
        self.assertEqual(storage["20250110"], 300)

    def test_add_existing_date_updates(self):
        response = self.client.post("/add/", json={"date": "20250101", "amount": 1500})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(storage["20250101"], 1500)

    def test_add_invalid_date_format(self):
        response = self.client.post("/add/", json={"date": "01-01-2025", "amount": 100})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Date must be in format YYYYMMDD", response.data)

    def test_calculate_sum(self):
        response = self.client.get("/calculate/sum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 1700)  # 1000+500+200

    def test_calculate_average(self):
        response = self.client.get("/calculate/average")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 1700/3)

    def test_calculate_with_empty_storage(self):
        storage.clear()
        response = self.client.get("/calculate/sum")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 0)

    def test_calculate_average_empty_storage(self):
        storage.clear()
        response = self.client.get("/calculate/average")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["result"], 0)

    def test_add_non_numeric_amount(self):
        response = self.client.post("/add/", json={"date": "20250103", "amount": "abc"})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Amount must be a number", response.data)
