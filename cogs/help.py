import discord
import asyncio
from discord.ext import commands
import emojis

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Axiol Help", description=f"Characters inside `<>` are variables, enter the variable without `<>`", color=discord.Color.purple())
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        embed.add_field(name="source", value="My Github source code!", inline=False)
        embed.add_field(name="suggest `<youridea>`",value="Use the command to suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)", inline=False)
        embed.set_footer(text="🔨 for moderation help")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🔨')
        await asyncio.sleep(1)

        modembed = discord.Embed(title="Moderation Help", color=discord.Colour.orange())
        modembed.add_field(name="prefix", value="Use this command to see and change your prefix!", inline=False)
        modembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")

        def check(reaction, user):
            return str(reaction.emoji) == '🔨' and reaction.message == helpmsg
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        
        if str(reaction.emoji) == '🔨' and user == ctx.author:
            await helpmsg.edit(embed=modembed)
            await helpmsg.clear_reaction('🔨')

def setup(bot):
    bot.add_cog(Help(bot))