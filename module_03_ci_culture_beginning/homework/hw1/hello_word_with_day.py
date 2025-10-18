import unittest
from datetime import datetime
from app import app, GREETINGS

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_today_greeting(self):
        """Проверяем, что приветствие соответствует сегодняшнему дню"""
        weekday = datetime.today().weekday()
        expected = GREETINGS[weekday]
        response = self.client.get("/hello-world/Мағжан")
        self.assertEqual(response.status_code, 200)
        self.assertIn(expected, response.get_data(as_text=True))

    def test_username_with_day_in_text(self):
        """Проверяем, что имя не влияет на выбор дня недели"""
        weekday = datetime.today().weekday()
        expected = GREETINGS[weekday]
        response = self.client.get("/hello-world/Хорошей среды")
        text = response.get_data(as_text=True)
        self.assertIn(expected, text)
