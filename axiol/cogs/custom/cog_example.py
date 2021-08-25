from discord.ext import commands

from axiol.core.bot import Bot
from axiol.core.context import TimedContext
from axiol.core.embed import Embed


class Test(commands.Cog):

    def __init__(self, client: Bot) -> None:
        self.client: Bot = client
        Embed.load(self.client)

    @commands.command()
    async def my(self, ctx: TimedContext):
        await ctx.send(embed=Embed(ctx)(description="Cabbage"))


def setup(client: Bot) -> None:
    client.add_cog(Test(client))
