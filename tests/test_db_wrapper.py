import sys
import time
import unittest
from contextlib import contextmanager
from io import StringIO


from axiol.classes.db_wrapper import Database, Collections


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr

    finally:
        sys.stdout, sys.stderr = old_out, old_err


class MyTestCase(unittest.TestCase):

    def test_instanciation(self):
        for cls in (Collections, Database):
            with captured_output() as (out, err):
                cls(None)

            output = out.getvalue().strip()
            self.assertTrue('Warning' in output)

            print(output)

        time.sleep(0.01)  # avoid output issue


if __name__ == '__main__':
    unittest.main()
