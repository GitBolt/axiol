import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(title="My Github Source Code Woohoo", description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/octicons/1024/mark-github-512.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, ideadesc=None):
    
        if ideadesc is not None:
            channel = self.bot.get_channel(843548616505294848)
            embed = discord.Embed(title=f"{ctx.author.name}'s idea", description=f"This idea came from server **{ctx.author.guild.name}**!", color=discord.Color.teal())
            embed.add_field(name="Suggestion", value=ideadesc)
            msg = await channel.send(embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format: ```# <YourIdeaDescription>```")


def setup(bot):
    bot.add_cog(Commands(bot))