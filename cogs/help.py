import discord
import asyncio
from discord.ext import commands
import utils.vars as var


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        try:
            pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
        except AttributeError:
            pref = var.DEFAULT_PREFIX

        embed = discord.Embed(title="Axiol Help", description=f"Characters inside `<>` are variables, enter the value and remove the `<>`", color=var.TEAL)
        embed.add_field(name=pref+"source", value="My Github source code!", inline=False)
        embed.add_field(name=pref+"suggest `<youridea>`",value="Use the command to suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)", inline=False)
        embed.set_footer(text="🔨 for moderation help\n✨ for reaction roles")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🔨')
        await helpmsg.add_reaction('✨')
        await asyncio.sleep(1)

        modembed = discord.Embed(title="Moderation", descriptio="What's better than entering a sweet little ban command?", color=var.TEAL2)
        modembed.add_field(name=pref+"prefix", value="Use this command to see and change your server prefix!", inline=False)
        modembed.add_field(name=pref+"rr `<messageid>` `<role>` `<emoji>`", value="Use this command to setup reaction roles in your server! For role either role ID or role ping can be used", inline=False)
        modembed.add_field(name=pref+"ban `<reason>`", value="Bans a user until banned, reason is optional", inline=False)
        modembed.add_field(name=pref+"unban", value="Unbans a banned user", inline=False)
        modembed.add_field(name=pref+"kick `<reason>`", value="Kicks the user out of server, reason is optional", inline=False)
        modembed.add_field(name=pref+"mute", value="Assigns the user the 'Muted' role, if the role does not exist then I can make it on my own when the command is used!", inline=False)
        modembed.add_field(name=pref+"unmute", value="Removes the 'Muted' role therefore lets the user speak", inline=False)
        modembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")


        rrembed = discord.Embed(title="Reaction Roles", color=var.BLUE)
        rrembed.add_field(name=pref+"rr `<messageid>` `<role>` `<emoji>`", value="Use this command to setup reaction roles in your server! For role either role ID or role ping can be used", inline=False)
        rrembed.add_field(name=pref+"removerr `<messageid>` `<emoji>`", value="Use this command to remove any existing reaction role!", inline=False)
        rrembed.add_field(name=pref+"allrr", value="Use this command to view all active reaction roles in the server!", inline=False)
        

        def check(reaction, user):
            return str(reaction.emoji) == '🔨' or '✨' and reaction.message == helpmsg and user == ctx.author
        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        
        if str(reaction.emoji) == '🔨':
            await helpmsg.edit(embed=modembed)
            await helpmsg.clear_reactions()
        if str(reaction.emoji) == '✨':
            await helpmsg.edit(embed=rrembed)
            await helpmsg.clear_reactions()


def setup(bot):
    bot.add_cog(Help(bot))