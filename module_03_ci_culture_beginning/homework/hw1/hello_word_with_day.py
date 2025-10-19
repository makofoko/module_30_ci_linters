import unittest
from datetime import datetime, timedelta
from app import app, GREETINGS
from freezegun import freeze_time

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_all_weekdays_greetings(self):
        """Проверяем, что приветствие соответствует каждому дню недели"""
        base_date = datetime(2025, 1, 6)  # это понедельник
        for weekday in range(7):
            test_date = base_date + timedelta(days=weekday)
            expected = GREETINGS[weekday]

            with freeze_time(test_date):
                response = self.client.get("/hello-world/Мағжан")
                self.assertEqual(response.status_code, 200)
                text = response.get_data(as_text=True)
                self.assertIn(expected, text, f"Ошибка для дня {weekday}")

    def test_username_does_not_affect_greeting(self):
        """Имя пользователя не влияет на выбор приветствия"""
        base_date = datetime(2025, 1, 6)  # понедельник
        for weekday in range(7):
            test_date = base_date + timedelta(days=weekday)
            expected = GREETINGS[weekday]

            with freeze_time(test_date):
                response = self.client.get("/hello-world/Хорошей среды")
                text = response.get_data(as_text=True)
                self.assertIn(expected, text, f"Ошибка для дня {weekday}")
