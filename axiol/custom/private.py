import discord
from discord.ext import commands


class Private(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def serverid(self, ctx):
        gl = []
        for i in self.bot.guilds:
            gl.append(i.id)
        await ctx.send(gl)


def setup(bot):
    bot.add_cog(Private(bot))