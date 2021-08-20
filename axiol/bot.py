"""Axiol Bot Core."""

import os
import dotenv

from discord.ext import commands
from classes.logger import log

TOKEN_KEY: str = 'TOKEN'


class Bot(commands.Bot):
    """Axiol custom bot class."""

    def __init__(self) -> None:
        log.inform("Initializing bot...")

        super(Bot, self).__init__(command_prefix=',')
        self.remove_command('help')

    def run(self) -> None:
        log.inform("Starting bot...")

        super(Bot, self).run(
            os.environ.get(TOKEN_KEY)
            or dotenv.dotenv_values('.env').get(TOKEN_KEY)
        )

    async def on_connect(self) -> None:
        log.success(f"Logging in as {self.user}.")

    async def on_ready(self) -> None:
        log.info(f"{self.user} is ready for use.")
