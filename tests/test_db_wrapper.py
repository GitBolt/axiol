import time
import unittest

from database.db_wrapper import Database, Collections
from tests.utils import captured_output


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
