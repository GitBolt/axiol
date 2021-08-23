"""Axiol Bot Core."""
import os
import sys

import dotenv
from discord.ext import commands

from axiol.cogs import cogs
from axiol import DOTENV_PATH, PREVENT_DOUBLE_RUNTIME_ERROR
from utils.logger import log

TOKEN_KEY: str = 'TOKEN'


class Bot(commands.Bot):
    """Axiol custom bot class."""

    def __init__(self, prefix) -> None:
        log.inform("Initializing bot...")

        super(Bot, self).__init__(command_prefix=prefix)
        self.remove_command('help')

        for cog in cogs:
            self.load_extension(cog)

    def run(self) -> None:
        log.inform("Starting bot...")

        super(Bot, self).run(
            os.environ.get(TOKEN_KEY)
            or dotenv.dotenv_values(DOTENV_PATH).get(TOKEN_KEY)
        )

    def load_extension(self, name: str, *, _package=None) -> None:
        cog_path: str = f'cogs.{name}'
        cog_name: str = cog_path.split('.')[1]

        log.inform(f"Loading {cog_name} extension...")

        try:
            super(Bot, self).load_extension(cog_path)

        except commands.ExtensionFailed as error:
            log.warn(
                f"Could not load component '{cog_name}' "
                f"due to {error.__cause__}"
            )

        else:
            log.success(f"loaded {cog_name}")

    async def on_connect(self) -> None:
        log.success(f"Logging in as {self.user}.")

    async def on_ready(self) -> None:
        log.inform(f"{self.user} is ready for use.")

    if PREVENT_DOUBLE_RUNTIME_ERROR:
        def __del__(self):
            # Prevents RuntimeError when Ctrl-C.
            sys.stderr.close()
