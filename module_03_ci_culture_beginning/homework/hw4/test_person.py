import unittest
import datetime
from person import Person

class TestPerson(unittest.TestCase):

    def setUp(self):
        self.p = Person("Alice", 2000, "Wonderland")

    def test_get_name(self):
        self.assertEqual(self.p.get_name(), "Alice")

    def test_set_name(self):
        self.p.set_name("Bob")
        self.assertEqual(self.p.get_name(), "Bob")

    def test_get_address(self):
        self.assertEqual(self.p.get_address(), "Wonderland")

    def test_set_address(self):
        self.p.set_address("New City")
        self.assertEqual(self.p.get_address(), "New City")

    def test_get_age(self):
        current_year = datetime.datetime.now().year
        expected_age = current_year - 2000
        self.assertEqual(self.p.get_age(), expected_age)

    def test_is_homeless_false(self):
        self.assertFalse(self.p.is_homeless())

    def test_is_homeless_true(self):
        p2 = Person("Charlie", 1995)
        self.assertTrue(p2.is_homeless())
