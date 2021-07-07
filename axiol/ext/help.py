import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix
import asyncio


def levelhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title=f"{var.E_LEVELING}  Leveling", description="Ah yes leveling, MEE6 who?", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"rank `<user>`", value="Shows server rank of the user! User field is optional for checking rank of yourself", inline=False
    ).add_field(name=getprefix(ctx)+"leaderboard", value="Shows the server leaderboard", inline=False
    ).add_field(name=getprefix(ctx)+"rankgraph `<amount>`", value="Shows a Bar chart of top users! Amount field is optional since 10 users are shown by default and max amount is 30", inline=False
    ).add_field(name=getprefix(ctx)+"givexp `<user>` `<amount>`", value="Gives user more XP", inline=False
    ).add_field(name=getprefix(ctx)+"removexp `<user>` `<amount>`", value="Removes user more XP", inline=False
    ).add_field(name=getprefix(ctx)+"levelinfo", value="Shows the server's leveling settings", inline=False
    ).add_field(name=getprefix(ctx)+"levelconfig", value=f"Configure leveling settings", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def modhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="🔨 Moderation", description="Reasons in every command are optional :)", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"ban `<user>` `<reason>`", value="Bans a user from the server", inline=False
    ).add_field(name=getprefix(ctx)+"unban `<user>`", value="Unbans any already banned user", inline=False
    ).add_field(name=getprefix(ctx)+"kick `<reason>`", value="Kicks the user out of the server", inline=False
    ).add_field(name=getprefix(ctx)+"mute `<member>`", value="Disables the ability for users to send text messages in all channels", inline=False
    ).add_field(name=getprefix(ctx)+"unmute `<member>`", value="Removes the 'Muted' role therefore lets the user send messages", inline=False
    ).add_field(name=getprefix(ctx)+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False
    ).add_field(name=getprefix(ctx)+"nick `<member>`", value="Changes nickname of a member", inline=False
    ).add_field(name=getprefix(ctx)+"addrole `<member>` `<role>`", value="Gives the member the role defined", inline=False
    ).add_field(name=getprefix(ctx)+"removerole `<member>` `<role>`", value="Removes the role defined from the member", inline=False
    ).add_field(name=getprefix(ctx)+"massrole `<role1>` `<role2>`", value="Members having role1 will be given role2", inline=False
    ).add_field(name=getprefix(ctx)+"massroleremove `<role1>` `<role2>`", value="Members having role1 will loose role2 if they have it", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def rrhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="✨ Reaction Roles", description="Whether it be default, custom, animated or even deleted after setting up - All types of emojis are allowed!", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"rr `<#channel>` `<messageid>` `<role>` `<emoji>`", value="Adds a reaction role", inline=False
    ).add_field(name=getprefix(ctx)+"removerr `<messageid>` `<emoji>`", value="Removes the reaction role", inline=False
    ).add_field(name=getprefix(ctx)+"allrr", value="Shows all active reaction roles in the server", inline=False
    ).add_field(name=getprefix(ctx)+"uniquerr `<messageid>`", value="Marks a message with unique reactions! Users would be able to react once hence take one role from the message", inline=False
    ).add_field(name=getprefix(ctx)+"removeunique `<messageid>`", value="Unmarks the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
    return embed

def welcomehelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="👋 Welcome", description="Greet new members with a nice welcome :D", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"welcomecard", value="Shows server welcome card", inline=False
    ).add_field(name=getprefix(ctx)+"welcomechannel `<#channel>`", value="Changes welcome channel", inline=False
    ).add_field(name=getprefix(ctx)+"welcomemessage", value="Changes welcome message", inline=False
    ).add_field(name=getprefix(ctx)+"welcomegreeting", value="Changes welcome greeting", inline=False
    ).add_field(name=getprefix(ctx)+"welcomeimage", value="Changes the welcome image", inline=False
    ).add_field(name=getprefix(ctx)+"welcomerole `<role>`", value="Assign automatic role to a member when they join", inline=False
    ).add_field(name=getprefix(ctx)+"welcomereset", value="Resets to the default welcome embed message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def verifyhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="✅ Verification", description="Keep the server safe from raiders and bots!", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"verifyinfo", value="Shows information of verification setup", inline=False
    ).add_field(name=getprefix(ctx)+"verifychannel `<#channel>`", value="Changes the verification channel", inline=False
    ).add_field(name=getprefix(ctx)+"verifyswitch", value="Switches between verification type", inline=False
    ).add_field(name=getprefix(ctx)+"verifyrole `<role>`", value="Give a role to users when they successfully verify", inline=False
    ).add_field(name=getprefix(ctx)+"verifyroleremove `<role>`", value="Remove a verified role if setted up", inline=False
    ).add_field(name=getprefix(ctx)+"verifyremove", value="Removes verification entirely by clearing all configs and disabling the plugin", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
    ).set_footer(text="For verify role, you can only set one at a time, if a verify role is already setted up then setting up another one will replace the existing one")
    return embed

def chatbothelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="🤖 Chatbot", description="I will reply to pings in every channel however setting up a bot chat channel won't require you ping me!" ,color=var.C_MAIN,
    ).add_field(name=getprefix(ctx)+"setchatbot `<#channel>`", value="Makes a channel for chatting with me! All messages sent there will be replied by me :D", inline=False
    ).add_field(name=getprefix(ctx)+"removechatbot `<#channel>`", value="Removes a chatbot channel", inline=False
    ).add_field(name=getprefix(ctx)+"chatbotchannels", value="Shows all channels where chat bot is enabled", inline=False
    ).add_field(name=getprefix(ctx)+"chatbotreport `<description>`", value="Sends report/bug related to the chatbot directly to the [Support server](https://discord.gg/KTn4TgwkUT)!"
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def automodhelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title=f"{var.E_AUTOMOD} Auto Moderation", description="Basically I'll delete all bad stuff :)" ,color=var.C_MAIN,
    ).add_field(name=getprefix(ctx)+"filters", value="Shows all available Auto-Moderation", inline=False
    ).add_field(name=getprefix(ctx)+"automodblacklist `<#channel>`", value="Blacklists a channel from Auto-Moderation, hence automod won't work there", inline=False
    ).add_field(name=getprefix(ctx)+"automodwhitelist", value="Whitelists a channel from Auto-Moderation, hence automod would work there", inline=False
    ).add_field(name=getprefix(ctx)+"ignorebots", value="Toggles between whether bots should be affect or not", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

def settingshelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title=f"{var.E_SETTINGS} Settings", description="Configure my settings and plugins for this server :D", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"plugins",value="Manage your plugins", inline=False
    ).add_field(name=getprefix(ctx)+"prefix", value="View or change my prefix", inline=False
    ).add_field(name=getprefix(ctx)+"permissions",value="Change the permissions for commands", inline=False)
    return embed


def extrahelp(ctx: commands.Context) -> discord.Embed:
    embed = discord.Embed(title="▶️ Extras", 
    description="[Vote](https://top.gg/bot/843484459113775114) "+
    "[Invite](https://discord.com/oauth2/authorize?client_id=843484459113775114&permissions=473295959&scope=bot) "+
    "[Support Server](https://discord.gg/hxc73psNsB) \n"+
    "Commands that are useful but don't belong to other categories!", color=var.C_MAIN
    ).add_field(name=getprefix(ctx)+"embed `<#channel>`",value="Generate an embed!", inline=False
    ).add_field(name=getprefix(ctx)+"avatar `<user>`", value="Shows avatar of any user! Works with users outside the server if User ID is correct", inline=False
    ).add_field(name=getprefix(ctx)+"stats", value="Shows server statistics", inline=False
    ).add_field(name=getprefix(ctx)+"about", value="Shows information about me!", inline=False
    ).add_field(name=getprefix(ctx)+"suggest `<youridea>`",value="Sends an idea directly to the support server!", inline=False
    ).add_field(name=getprefix(ctx)+"invite",value="Sends my bot invite link!", inline=False
    ).add_field(name=getprefix(ctx)+"source", value="Sends link to my Github repository since I am open source :D", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})

        embed = discord.Embed(
        title="Axiol Help",
        description=f"Help subcommands for all **enabled plugins**\n For all users, members, roles and channels either their ID or mention can be used.",
        color=var.C_MAIN
        ).set_footer(text="Either use the subcommand or react to the emojis below"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")

        for i in GuildDoc:
            if GuildDoc.get(i) == True:
                helpname = i.lower()
                if i.lower() == "reaction roles": #Reaction roles command doesn't have space in between reaction and roles
                    helpname = i.lower().replace(" ", "")
                embed.add_field(name=f"{getprefix(ctx)}help {helpname}", value=f"{var.DICT_PLUGINEMOJIS.get(i)} {i} Help", inline=False)

        embed.add_field(name=f"{getprefix(ctx)}help extras", value=f"▶️ Non plugin commands", inline=False)
        embed.add_field(name=f"{getprefix(ctx)}help settings", value=f"{var.E_SETTINGS} Configure settings", inline=False)
        helpmsg = await ctx.send(embed=embed)

        for i in GuildDoc:
            if GuildDoc.get(i) == True:
                await helpmsg.add_reaction(var.DICT_PLUGINEMOJIS.get(i))
        await helpmsg.add_reaction("▶️")
        await helpmsg.add_reaction(var.E_SETTINGS)
        
        def check(reaction, user):
            return user == ctx.author and reaction.message == helpmsg


        HelpDict = {
            "Leveling": levelhelp,
            "Moderation": modhelp,
            "Reaction Roles":rrhelp,
            "Welcome": welcomehelp,
            "Verification": verifyhelp,
            "Chatbot": chatbothelp,
            "AutoMod": automodhelp
            
        }

        try:
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
                if str(reaction.emoji) in var.DICT_PLUGINEMOJIS.values():

                    helptype = list(var.DICT_PLUGINEMOJIS.keys())[list(var.DICT_PLUGINEMOJIS.values()).index(str(reaction.emoji))]
                    await helpmsg.edit(embed=HelpDict.get(helptype)(ctx))
                    try:
                        await helpmsg.remove_reaction(str(reaction.emoji), ctx.author)
                    except discord.Forbidden:
                        pass
                
                #Since extra help and plugin is always there
                if str(reaction.emoji) == "▶️":
                    await helpmsg.edit(embed=extrahelp(ctx))
                    try:
                        await helpmsg.remove_reaction("▶️", ctx.author)
                    except discord.Forbidden:
                        pass
                if str(reaction.emoji) == var.E_SETTINGS:
                    await helpmsg.edit(embed=settingshelp(ctx))
                    try:
                        await helpmsg.remove_reaction(var.E_SETTINGS, ctx.author)
                    except discord.Forbidden:
                        pass

        except asyncio.TimeoutError:
            try:
                await helpmsg.clear_reactions()
            except discord.Forbidden:
                await helpmsg.remove_reaction(var.E_SETTINGS, self.bot.user)
                for i in GuildDoc:
                    if GuildDoc.get(i) == True:
                        await helpmsg.remove_reaction(var.DICT_PLUGINEMOJIS.get(i), self.bot.user)
                await helpmsg.remove_reaction("▶️", self.bot.user)


           
    @help.command()
    async def leveling(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Leveling") == True:
            await ctx.send(embed=levelhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Leveling plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def moderation(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Moderation") == True:
            await ctx.send(embed=modhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def reactionroles(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Reaction Roles") == True:
            await ctx.send(embed=rrhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Reaction Roles plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def welcome(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome") == True:
            await ctx.send(embed=welcomehelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def verification(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification") == True:
            await ctx.send(embed=verifyhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Verification plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def chatbot(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot") == True:
            await ctx.send(embed=chatbothelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Chatbot plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def automod(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("AutoMod") == True:
            await ctx.send(embed=automodhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Auto-Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def extras(self, ctx):
        await ctx.send(embed=extrahelp(ctx))
    
    @help.command()
    async def settings(self, ctx):
        await ctx.send(embed=settingshelp(ctx))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelconfig(self, ctx):
        
        embed = discord.Embed(title="Configure leveling for this server",
        color=var.C_TEAL
        ).add_field(name=getprefix(ctx)+"xprange `<leastamount>` `<highestamount>`",value="Set the range between which users will be awarded with random xp", inline=False
        ).add_field(name=getprefix(ctx)+"blacklist `<#channel>`",value=f"Add the channel where you don't want users to gain xp.", inline=False
        ).add_field(name=getprefix(ctx)+"whitelist `<#channel>`",value=f"Whitelist an xp blacklisted channel.", inline=False
        ).add_field(name=getprefix(ctx)+"alertchannel `<#channel>`", value="Define the channel where alerts will be sent for level ups!", inline=False
        ).add_field(name=getprefix(ctx)+"togglealerts", value="Disable or Enable alert message for level ups!", inline=False
        ).add_field(name=getprefix(ctx)+"reward `<level>` `<role>`", value="Setup awards for reaching certain level! For level only use the number", inline=False
        ).set_footer(text=f"Leveling is a plugin so to disable it, use the command {getprefix(ctx)}plugins and click on the leveling emoji to toggle")
        #).add_field(name=getprefix(ctx)+"maxlevel `<amount>`", value="Define the max level which can be achieved by a user", inline=False
        #).add_field(name=getprefix(ctx)+"alertmessage `<message>`", value=f"Change the alert message! Use these values in between:\n[user] [xp] [level]\n Make sure to put them between square brackets!", inline=False
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))