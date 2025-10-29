import unittest

from block_errors import BlockErrors

class TestBlockErrors(unittest.TestCase):
    def test_ignore_error(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except ZeroDivisionError:
            self.fail("ZeroDivisionError не должен был быть проброшен")

    def test_raise_unexpected_error(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_nested_blocks(self):
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / "0"

    def test_ignore_child_exception(self):
        try:
            with BlockErrors({LookupError}):
                raise IndexError("child exception")
        except IndexError:
            self.fail("IndexError должен быть проигнорирован как дочерний LookupError")


if __name__ == "__main__":
    unittest.main()
