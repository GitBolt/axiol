from discord.ext import commands
from discord.ext.commands import Context

from core.bot import Bot
from core.embed import Embed


class Test(commands.Cog):

    def __init__(self, client: Bot) -> None:
        self.client = client

        Embed.load(
            self.client,
            name="test"
        )

    @commands.command()
    async def my(self, ctx: Context):

        await ctx.send(
            embed=Embed(ctx)(description="Cabbage")
        )

    @commands.command()
    async def hello(self, ctx: Context):
        await ctx.send(
            embed=Embed(ctx)(description="world!")
        )


def setup(client) -> None:
    client.add_cog(Test(client))
