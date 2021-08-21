from axiol.classes.logger import log
import unittest

import sys
from contextlib import contextmanager
from io import StringIO


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

    def test_base(self):
        for log_func in (log.success, log.inform, log.warn, log.db):
            with captured_output() as (out, err):
                log_func('test')

            output = out.getvalue().strip()
            self.assertTrue(output.endswith('test'))
            print(output)

    def test_error(self):
        with self.assertRaises(SystemExit) as cm:
            log.error('test')

        the_exception = cm.exception
        self.assertIsInstance(the_exception, SystemExit)


if __name__ == '__main__':
    unittest.main()
