import os

__version__: str = '2.0.0'

DOTENV_PATH: str = os.path.abspath(
    os.path.join(
        __file__,
        os.path.pardir,
        os.path.pardir,
        '.env'
    )
)