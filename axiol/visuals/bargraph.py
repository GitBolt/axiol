import discord
from discord.ext import commands
import requests
import variables as var


class BarGraph(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command(aliases=["rankchart", "levelgraph", "levelchart"])
    async def rankgraph(self, ctx, limit:int=10):
        if limit > 30:
            await ctx.send(embed=discord.Embed(
                        description=f"{var.E_ERROR} You cannot view more than 30 users in a bar graph, that's way to much haha",
                        color=var.C_RED
                        ))
        else:
            botmsg = await ctx.send(f"Fetching data {var.E_LOADING} Just a second!")
            await ctx.trigger_typing()
            res = requests.get(f"https://axiol.up.railway.app/bargraph/rank/{ctx.guild.id}?limit={limit}")
            await ctx.send(res.json()["message"])
            await botmsg.delete()
    
def setup(bot):
    bot.add_cog(BarGraph(bot))