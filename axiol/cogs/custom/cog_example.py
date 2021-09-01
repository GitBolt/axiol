from discord.ext import commands

from axiol.core.bot import Bot
from axiol.core.context import TimedContext
from axiol.core.embed import Embed


class Test(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot
        Embed.load(self.bot)

    @commands.command()
    async def my(self, ctx: TimedContext):
        await ctx.send(embed=Embed(ctx)(description="Cabbage"))


def setup(bot: Bot) -> None:
    bot.add_cog(Test(bot))
