import os
import dotenv

from discord.ext import commands

TOKEN_KEY: str = 'TOKEN'


class Bot(commands.Bot):

    def __init__(self):
        super(Bot, self).__init__(command_prefix=',')
        self.remove_command('help')

    def run(self):
        super(Bot, self).run(
            os.environ.get(TOKEN_KEY)
            or dotenv.dotenv_values('.env').get(TOKEN_KEY)
        )

    async def on_connect(self):
        print("Logged int as", self.user)
