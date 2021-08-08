import discord
from discord.ext import commands
import requests
import variables as var


class PieChart(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=["piegraph", "rankpiechart", "rankpiegraph"])
    async def piechart(self, ctx):
            botmsg = await ctx.send(f"Fetching data {var.E_LOADING} Just a second!")
            await ctx.trigger_typing()
            res = requests.get(f"https://axiol.up.railway.app/piechart/{ctx.guild.id}")
            await ctx.send(res.json()["message"])
            await botmsg.delete()
    
def setup(bot):
    bot.add_cog(PieChart(bot))
