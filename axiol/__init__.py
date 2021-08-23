import os

__version__: str = '2.0.0'

TEST_SERVER_ID: int = 843516084266729512

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
