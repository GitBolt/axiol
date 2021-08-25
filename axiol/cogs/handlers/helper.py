from discord.ext import commands

from axiol.core.bot import Bot
from axiol.core.context import TimedContext
from axiol.core.embed import Embed


class Helper(commands.Cog):

    def __init__(self, client):
        self.client: Bot = client

        Embed.load(self.client)

    @commands.command(name='cmds')
    async def all_commands(self, ctx: TimedContext):
        await ctx.send(
            embed=Embed(ctx)(
                description=(
                    f"> {len(self.client.all_commands)} commands available"
                )
            ).add_fields(
                field_list=self.client.cogs.items(),
                map_values=lambda cog: ','.join(
                    f'`{cmd.name}`' for cmd in cog.get_commands()
                )
            )
        )


def setup(client):
    client.add_cog(Helper(client))
