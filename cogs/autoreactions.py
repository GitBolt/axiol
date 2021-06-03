import discord
from discord.ext import commands
import utils.variables as var
from utils.functions import getprefix


class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def autoreact(self, ctx, message:discord.Message, emoji):
        if message and emoji is not None:
            pass
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the message and emoji both to add an autoreact",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}autoreact <messageid> <emoji>`"
            ))




def setup(bot):
    bot.add_cog(AutoReactions(bot))