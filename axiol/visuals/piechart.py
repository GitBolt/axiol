import discord
from aiohttp import request
from discord.ext import commands
import variables as var



class PieChart(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=["piegraph", "rankpiechart", "rankpiegraph"])
    async def piechart(self, ctx):
            botmsg = await ctx.send(f"Fetching data {var.E_LOADING} Just a second!")
            await ctx.trigger_typing()
            async with request("GET", f"https://axiol.up.railway.app/piechart/{ctx.guild.id}") as res:
                response = await res.json()
                await ctx.send(response["message"])
                await botmsg.delete()

def setup(bot):
    bot.add_cog(PieChart(bot))
