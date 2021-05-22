import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import currentprefix

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="My Github Source Code Woohoo", 
        description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", 
        color=var.CTEAL
        ).set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/shift-logotypes/32/Github-512.png")

        await ctx.send(embed=embed)



    @commands.command()
    async def suggest(self, ctx, *, desc=None):
        if desc is not None:
            channel = self.bot.get_channel(843548616505294848) #Support server suggestion channel id

            embed = discord.Embed(title=f"{ctx.author}'s idea", 
            description=f"This idea came from a server named **{ctx.guild.name}**!", 
            color=var.CBLUE
            ).add_field(name="Suggestion", value=desc)

            msg = await channel.send(embed=embed)
            await msg.add_reaction(var.ACCEPT)
            await msg.add_reaction(var.DECLINE)
            await ctx.send("Suggestion sent to the support server!")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format\n```{currentprefix(ctx)} <description of your idea>```\nDon't forget the space after prefix :D")


    @commands.command()
    async def invite(self, ctx):

        embed = discord.Embed(title="Axiol invite",
        description="[Invite the bot from here](https://discord.com/api/oauth2/authorize?client_id=843484459113775114&permissions=8&scope=bot)",
        color=var.CBLUE
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))