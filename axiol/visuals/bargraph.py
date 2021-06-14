import discord
from discord.ext import commands
import requests
import variables as var


class BarGraph(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def levelchart(self, ctx, limit:int=10):
        if limit > 30:
            await ctx.send(embed=discord.Embed(
                        description=f"{var.E_ERROR} You cannot view more than 30 users in a bar graph, that's way to much haha",
                        color=var.C_RED
                        ))
        else:
            await ctx.send("Fetching data... Just a sec!")
            res = requests.get(f"https://axiol.up.railway.app/bargraph/leaderboard/{ctx.guild.id}?limit={limit}")
            await ctx.send(res.json()["message"])

    
def setup(bot):
    bot.add_cog(BarGraph(bot))