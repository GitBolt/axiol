import unittest

from core.classes.logger import log
from tests.utils import captured_output


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
