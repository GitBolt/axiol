import discord
from aiohttp import request
from discord.ext import commands
import axiol.variables as var


class BarGraph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="bargraph", aliases=["barchart", "rankbarchart", "rankbargraph"]
    )
    async def bar_graph(self, ctx, limit: int = 10):
        if limit > 30:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You cannot view more than 30 users in a bar "
                        "graph, that's way to much haha"
                    ),
                    color=var.C_RED
                )
            )

        else:
            bot_msg = await ctx.send(
                f"Fetching data {var.E_LOADING} Just a second!"
            )

            await ctx.trigger_typing()
            async with request(
                "GET",
                f"https://axiol.up.railway.app/bargraph/{ctx.guild.id}"
                f"?limit={limit}"
            ) as res:
                response = await res.json()

                await ctx.send(response["message"])
                await bot_msg.delete()


def setup(bot):
    bot.add_cog(BarGraph(bot))
