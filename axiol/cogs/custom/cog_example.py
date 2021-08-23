from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def my(self, ctx):
        await ctx.send('cabbage!')


def setup(client) -> None:
    client.add_cog(Test(client))
