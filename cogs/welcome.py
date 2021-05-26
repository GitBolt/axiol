from discord.ext import commands
import discord

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

def setup(bot):
    bot.add_cog(Welcome(bot))