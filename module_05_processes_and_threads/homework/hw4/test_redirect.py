import unittest
import io
import sys
import traceback
from redirect import Redirect


class TestRedirect(unittest.TestCase):
    def test_redirect_stdout(self):
        buf = io.StringIO()
        with Redirect(stdout=buf):
            print("hello stdout")
        self.assertIn("hello stdout", buf.getvalue())

    def test_redirect_stderr(self):
        buf = io.StringIO()
        try:
            with Redirect(stderr=buf):
                raise ValueError("oops")
        except ValueError:
            traceback.print_exc()
        self.assertIn("oops", buf.getvalue())

    def test_redirect_both(self):
        out_buf = io.StringIO()
        err_buf = io.StringIO()
        try:
            with Redirect(stdout=out_buf, stderr=err_buf):
                print("to stdout")
                raise RuntimeError("to stderr")
        except RuntimeError:
            pass
        self.assertIn("to stdout", out_buf.getvalue())
        self.assertIn("to stderr", err_buf.getvalue())

    def test_no_redirect(self):
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        with Redirect():
            self.assertIs(sys.stdout, old_stdout)
            self.assertIs(sys.stderr, old_stderr)

if __name__ == "__main__":
    unittest.main()
