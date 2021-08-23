from typing import TYPE_CHECKING

from discord.ext import commands
from discord.ext.commands import Context

if TYPE_CHECKING:
    from core.bot import Bot


class Test(commands.Cog):

    def __init__(self, client: Bot) -> None:
        self.client = client

    @commands.command()
    async def my(self, ctx: Context):
        await ctx.send('cabbage!')


def setup(client) -> None:
    client.add_cog(Test(client))
