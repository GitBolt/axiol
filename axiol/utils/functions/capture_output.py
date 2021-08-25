import sys
from contextlib import contextmanager
from io import StringIO
from typing import Tuple


# Credits to: Rob Kennedy
# https://stackoverflow.com/questions/4219717/

@contextmanager
def captured_output() -> Tuple[StringIO, StringIO]:
    """Capture stdout, stderr and returns a tuple of their contents."""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr

    finally:
        sys.stdout, sys.stderr = old_out, old_err
