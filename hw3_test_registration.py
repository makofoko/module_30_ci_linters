import unittest
from hw1_registration import app


class RegistrationFormTestCase(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def post_data(self, data):
        return self.client.post("/registration", data=data, follow_redirects=True)

    def test_valid_email(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": 123456,
            "comment": "ok"
        })
        self.assertEqual(resp.status_code, 200)

    def test_invalid_email(self):
        resp = self.post_data({
            "email": "not-an-email",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"email", resp.data)

    def test_valid_phone(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 200)

    def test_invalid_phone_length(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "12345",  # слишком короткий
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"phone", resp.data)

    def test_missing_name(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"name", resp.data)

    def test_missing_address(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"address", resp.data)

    def test_valid_index(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": 123456
        })
        self.assertEqual(resp.status_code, 200)

    def test_invalid_index(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": -5
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn(b"index", resp.data)

    def test_optional_comment(self):
        resp = self.post_data({
            "email": "test@example.com",
            "phone": "1234567890",
            "name": "Иван",
            "address": "Москва",
            "index": 123456

        })
        self.assertEqual(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
