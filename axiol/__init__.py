import os
from typing import Tuple

from axiol.utils.logger import log

__version__: str = '2.0.0'

TEST_SERVER_ID: int = 843516084266729512

OWNER_ID: int = 812699388815605791

DEVS_ID: Tuple[int, int, int] = (
    812699388815605791,
    723971496107573328,
    791950104680071188
)


DOTENV_PATH: str = os.path.abspath(
    os.path.join(
        __file__,
        os.path.pardir,
        os.path.pardir,
        '.env'
    )
)

# WARNING --------------------------------------------------------------
# This is cancelling any fatal exceptions from bot class when activated.
# If you have any problem with this, consider setting it to False.
PREVENT_DOUBLE_RUNTIME_ERROR: bool = True

if PREVENT_DOUBLE_RUNTIME_ERROR:
    log.warn("PREVENT DOUBLE RUNTIME ERROR mode activated.")
