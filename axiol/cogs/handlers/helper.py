from discord.ext import commands

from axiol.core.bot import Bot
from axiol.core.context import TimedContext
from axiol.core.embed import Embed


class Helper(commands.Cog):

    def __init__(self, bot):
        self.bot: Bot = bot

        Embed.load(self.bot)

    @commands.command(name='cmds')
    async def all_commands(self, ctx: TimedContext):
        await ctx.send(
            embed=Embed(ctx)(
                description=(
                    f"> {len(self.bot.all_commands)} commands available"
                )
            ).add_fields(
                field_list=self.bot.cogs.items(),
                map_values=lambda cog: ','.join(
                    f'`{cmd.name}`' for cmd in cog.get_commands()
                )
            )
        )


def setup(bot):
    bot.add_cog(Helper(bot))
