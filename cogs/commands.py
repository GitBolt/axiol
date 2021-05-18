import discord
from discord.ext import commands
import utils.vars as var

DATABASE = var.MONGOCLIENT['Axiol']
PREFIXES = DATABASE["Prefixes"] #Prefixes Collection

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="My Github Source Code Woohoo", description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", color=var.MAGENTA2)
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/shift-logotypes/32/Github-512.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, ideadesc=None):

        try:
            pref = PREFIXES.find_one({"serverid": ctx.author.guild.id}).get("prefix")
        except AttributeError:
            pref = var.DEFAULT_PREFIX

        if ideadesc is not None:
            channel = self.bot.get_channel(843548616505294848) #Support server suggestion channel id
            embed = discord.Embed(title=f"{ctx.author.name}'s idea", description=f"This idea came from server **{ctx.author.guild.name}**!", color=var.MAGENTA3)
            embed.add_field(name="Suggestion", value=ideadesc)
            msg = await channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format: ```{pref} <YourIdeaDescription>``` Don't forget the space after prefix :D")


def setup(bot):
    bot.add_cog(Commands(bot))