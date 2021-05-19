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
        embed.add_field(name=pref+"suggest `<youridea>`",value="Suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)!", inline=False)
        embed.set_footer(text="🔨 for moderation help\n✨ for reaction roles")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
        helpmsg = await ctx.send(embed=embed)
        await helpmsg.add_reaction('🔨')
        await helpmsg.add_reaction('✨')
        await asyncio.sleep(1)

        modembed = discord.Embed(title="Moderation", descriptio="What's better than entering a sweet little ban command?", color=var.TEAL2)
        modembed.add_field(name=pref+"prefix", value="Check and change your server prefix!", inline=False)
        modembed.add_field(name=pref+"ban `<reason>`", value="Bans a user until unbanned, reason is optional", inline=False)
        modembed.add_field(name=pref+"unban", value="Unbans a banned user", inline=False)
        modembed.add_field(name=pref+"kick `<reason>`", value="Kicks the user out of the server, reason is optional", inline=False)
        modembed.add_field(name=pref+"mute", value="Assigns 'Muted' role to the user hence disabling their ability to send messages! If the role does not exist then I can make it on my own when the command is used!", inline=False)
        modembed.add_field(name=pref+"unmute", value="Removes the 'Muted' role therefore lets the user send messages.", inline=False)
        modembed.set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")


        rrembed = discord.Embed(title="Reaction Roles", color=var.BLUE)
        rrembed.add_field(name=pref+"rr `<messageid>` `<role>` `<emoji>`", value="Setup reaction roles in your server! For role either role ID or role ping can be used.", inline=False)
        rrembed.add_field(name=pref+"removerr `<messageid>` `<emoji>`", value="Remove any existing reaction role.", inline=False)
        rrembed.add_field(name=pref+"allrr", value="View all active reaction roles in the server!", inline=False)
        rrembed.add_field(name=pref+"uniquerr `<messageid>`", value="Mark a message with unique reactions! Users would be able to react once hence take one role from the message.", inline=False)
        rrembed.add_field(name=pref+"removeunique `<messageid>`", value="Unmark the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message.", inline=False)


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