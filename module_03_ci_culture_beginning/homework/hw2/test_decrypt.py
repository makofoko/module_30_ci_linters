import unittest
from decrypt import decrypt

class TestDecrypt(unittest.TestCase):

    def test_single_dot_cases(self):
        """Случаи с одной точкой"""
        cases = {
            "абра-кадабра.": "абра-кадабра",
            ".": "",
        }
        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot_cases(self):
        """Случаи с двумя точками подряд"""
        cases = {
            "абраа..-кадабра": "абра-кадабра",
            "абраа..-.кадабра": "абра-кадабра",
            "абра--..кадабра": "абра-кадабра",
            "абр......a.": "a",
            "1..2.3": "23",
        }
        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_many_dots_cases(self):
        """Случаи с большим количеством точек"""
        cases = {
            "абрау...-кадабра": "абра-кадабра",
            "абра........": "",
            "1.......................": "",
        }
        for encrypted, expected in cases.items():
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

if __name__ == "__main__":
    unittest.main(verbosity=2)