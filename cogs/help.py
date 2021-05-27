import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix
import asyncio

def mainhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Axiol Help", description="Either enter the sub command or react to the emojis below!", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"help levels", value=f"Leveling help {var.LVL}", inline=False
    ).add_field(name=getprefix(ctx)+"help mod", value="Moderation help 🔨", inline=False
    ).add_field(name=getprefix(ctx)+"help rr", value="Reaction role help ✨", inline=False
    ).add_field(name=getprefix(ctx)+"help verification", value="Member verification help ✅", inline=False
    ).add_field(name=getprefix(ctx)+"help welcome", value="Welcome greetings help 👋", inline=False
    ).add_field(name=getprefix(ctx)+"help extras", value=f"Commands that don't belong do the categories above ➡️", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def levelhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Ah yes leveling, MEE6 who?", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"levels", value="Setup and configure leveling!", inline=False
    ).add_field(name=getprefix(ctx)+"rank `<user>`", value="Shows server rank of the user, user id or user mention can be used to check ranks, user field is optional for checking rank of yourself.", inline=False
    ).add_field(name=getprefix(ctx)+"leaderboard", value="Shows server leaderboard!", inline=False
    ).add_field(name=getprefix(ctx)+"givexp `<user>` `<amount>`", value="Gives user more XP! For user either user can be mentioned or ID can be used", inline=False
    ).add_field(name=getprefix(ctx)+"removexp `<user>` `<amount>`", value="Removes user more XP! For user either user can be mentioned or ID can be used", inline=False
    ).add_field(name=getprefix(ctx)+"levelconfig", value="Configure leveling settings!", inline=False
    #).add_field(name=getprefix(ctx)+"award", value="Setup awards for reaching certain amount of xp!", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def modhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Moderation", description="What's better than entering a sweet little ban command?", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"prefix", value="Check and change your server prefix!", inline=False
    ).add_field(name=getprefix(ctx)+"ban `<reason>`", value="Bans a user until unbanned, reason is optional", inline=False
    ).add_field(name=getprefix(ctx)+"unban", value="Unbans a banned user", inline=False
    ).add_field(name=getprefix(ctx)+"kick `<reason>`", value="Kicks the user out of the server, reason is optional", inline=False
    ).add_field(name=getprefix(ctx)+"mute", value="Assigns 'Muted' role to the user hence disabling their ability to send messages! If the role does not exist then I can make it on my own when the command is used!", inline=False
    ).add_field(name=getprefix(ctx)+"unmute", value="Removes the 'Muted' role therefore lets the user send messages.", inline=False
    ).add_field(name=getprefix(ctx)+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def rrhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Reaction Roles", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"rr `<messageid>` `<role>` `<emoji>`", value="Setup reaction roles in your server! For role either role ID or role ping can be used.", inline=False
    ).add_field(name=getprefix(ctx)+"removerr `<messageid>` `<emoji>`", value="Remove any existing reaction role.", inline=False
    ).add_field(name=getprefix(ctx)+"allrr", value="View all active reaction roles in the server!", inline=False
    ).add_field(name=getprefix(ctx)+"uniquerr `<messageid>`", value="Mark a message with unique reactions! Users would be able to react once hence take one role from the message.", inline=False
    ).add_field(name=getprefix(ctx)+"removeunique `<messageid>`", value="Unmark the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message.", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
    return embed

def verifyhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Verification", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"verification", value="Setup and configure verification for your server!", inline=False
    ).add_field(name=getprefix(ctx)+"verifytype", value="Get information about the type of verification server has!", inline=False
    ).add_field(name=getprefix(ctx)+"verifyswitch", value="Switch between verification type", inline=False
    ).add_field(name=getprefix(ctx)+"verifyremove", value="Remove verification from your server (if enabled)", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def welcomehelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Welcome Greetings", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"welcome", value="Setup and configure welcome greetings for new joining server members!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomechannel <#channel>", value="Change welcome channel!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomemessage", value="Change welcome message!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomeimage", value="Change the welcome image!", inline=False
    ).add_field(name=getprefix(ctx)+"welcomerole `<role>`", value="Assign automatic role to a member when they join! For role either role mention or id can be used.", inline=False
    ).add_field(name=getprefix(ctx)+"welcomeremove", value="Remove welcome greetings (if enabled)", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed
    
def extrahelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="Extras", description="Commands that are useful bot don't belong to other categories!", color=var.CMAIN
    ).add_field(name=getprefix(ctx)+"embed `<#channel>`",value="Generate an embed!", inline=False
    ).add_field(name=getprefix(ctx)+"about", value="Information about me :sunglasses:", inline=False
    ).add_field(name=getprefix(ctx)+"suggest `<youridea>`",value="Suggest an idea which will be sent in the official [Axiol Support Server](https://discord.gg/KTn4TgwkUT)!", inline=False
    ).add_field(name=getprefix(ctx)+"invite",value="My invite link!", inline=False
    ).add_field(name=getprefix(ctx)+"source", value="My Github source code!", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        helpmsg = await ctx.send(embed=mainhelp(ctx))
        await helpmsg.add_reaction(var.LVL)
        await helpmsg.add_reaction('🔨')
        await helpmsg.add_reaction('✨')
        await helpmsg.add_reaction('✅')
        await helpmsg.add_reaction('👋')
        await helpmsg.add_reaction('➡️')

        def check(reaction, user):
            return user == ctx.author and reaction.message == helpmsg
      
        try:
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
                if str(reaction.emoji) == var.LVL:
                    await helpmsg.edit(embed=levelhelp(ctx))
                    await helpmsg.remove_reaction(var.LVL, ctx.author)
                if str(reaction.emoji) == '🔨':
                    await helpmsg.edit(embed=modhelp(ctx))
                    await helpmsg.remove_reaction('🔨', ctx.author)
                if str(reaction.emoji) == '✨':
                    await helpmsg.edit(embed=rrhelp(ctx))
                    await helpmsg.remove_reaction('✨', ctx.author)
                if str(reaction.emoji) == '✅':
                    await helpmsg.edit(embed=verifyhelp(ctx))
                    await helpmsg.remove_reaction('✅', ctx.author)
                if str(reaction.emoji) == '👋':
                    await helpmsg.edit(embed=welcomehelp(ctx))
                    await helpmsg.remove_reaction('👋', ctx.author)
                if str(reaction.emoji) == '➡️':
                    await helpmsg.edit(embed=extrahelp(ctx))
                    await helpmsg.remove_reaction('➡️', ctx.author)

        except asyncio.TimeoutError:
            await helpmsg.clear_reactions()


    @help.command(aliases=["level"])
    async def levels(self, ctx):
        await ctx.send(embed=levelhelp(ctx))

    @help.command()
    async def mod(self, ctx):
        await ctx.send(embed=modhelp(ctx))

    @help.command()
    async def rr(self, ctx):
        await ctx.send(embed=rrhelp(ctx))

    @help.command()
    async def verification(self, ctx):
        await ctx.send(embed=verifyhelp(ctx))
    
    @help.command()
    async def welcome(self, ctx):
        await ctx.send(embed=welcomehelp(ctx))

    @help.command()
    async def extras(self, ctx):
        await ctx.send(embed=verifyhelp(ctx))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelconfig(self, ctx):
        
        embed = discord.Embed(title="Configure leveling for this server",
        color=var.CTEAL
        ).add_field(name=getprefix(ctx)+"xprange `<leastamount>` `<highestamount>`",value="Set the range between which users will be awarded with random xp", inline=False
        ).add_field(name=getprefix(ctx)+"blacklist `<#channel>`",value=f"Add the channel where you don't want users to gain xp.", inline=False
        ).add_field(name=getprefix(ctx)+"whitelist `<#channel>`",value=f"Whitelist an xp blacklisted channel.", inline=False
        ).add_field(name=getprefix(ctx)+"alertchannel `<#channel>`", value="Define the channel where alerts will be sent for level ups!", inline=False
        #).add_field(name=getprefix(ctx)+"maxlevel `<amount>`", value="Define the max level which can be achieved by a user", inline=False
        #).add_field(name=getprefix(ctx)+"alertmessage `<message>`", value=f"Change the alert message! Use these values in between:\n[user] [xp] [level]\n Make sure to put them between square brackets!", inline=False
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))