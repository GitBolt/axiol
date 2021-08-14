import discord
from discord.ext import commands
import variables as var
import database as db
from functions import get_prefix
import asyncio


async def levelhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title=f"{var.E_LEVELING}  Leveling", description="Ah yes leveling, MEE6 who?", color=var.C_MAIN
    ).add_field(name=prefix+"rank `<user>`", value="Shows server rank of the user! User field is optional for checking rank of yourself", inline=False
    ).add_field(name=prefix+"leaderboard", value="Shows the server leaderboard", inline=False
    ).add_field(name=prefix+"bargraph `<amount>`", value="Shows a Bar chart of top users! Amount field is optional since 10 users are shown by default and max amount is 30", inline=False
    ).add_field(name=prefix+"piechart `<amount>`", value="Shows a Pie chart of top 10 users!", inline=False
    ).add_field(name=prefix+"givexp `<user>` `<amount>`", value="Gives user more XP", inline=False
    ).add_field(name=prefix+"removexp `<user>` `<amount>`", value="Removes user more XP", inline=False
    ).add_field(name=prefix+"levelinfo", value="Shows the server's leveling settings", inline=False
    ).add_field(name=prefix+"levelconfig", value=f"Configure leveling settings", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def modhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="🔨 Moderation", description="Reasons in every command except warn is optional :)", color=var.C_MAIN
    ).add_field(name=prefix+"ban `<user>` `<reason>`", value="Bans a user from the server", inline=False
    ).add_field(name=prefix+"unban `<user>`", value="Unbans any already banned user", inline=False
    ).add_field(name=prefix+"kick `<member>` `<reason>`", value="Kicks the user out of the server", inline=False
    ).add_field(name=prefix+"mute `<member>`", value="Disables the ability for users to send text messages in all channels", inline=False
    ).add_field(name=prefix+"unmute `<member>`", value="Removes the 'Muted' role therefore lets the user send messages", inline=False
    ).add_field(name=prefix+"warn `<member>` `<reason>`", value="Warns a member, reason is mandatory", inline=False
    ).add_field(name=prefix+"removewarn `<member>` `<warn_position>`", value="Removes the warn from the position defined from the member", inline=False
    ).add_field(name=prefix+"warns `<member>`", value="Shows all warns of the member", inline=False
    ).add_field(name=prefix+"purge `<amount>`", value="Deletes the number of messages defined in the command from the channel", inline=False
    ).add_field(name=prefix+"nick `<member>` `<member>`", value="Changes nickname of a member", inline=False
    ).add_field(name=prefix+"addrole `<member>` `<role>`", value="Gives the member the role defined", inline=False
    ).add_field(name=prefix+"removerole `<member>` `<role>`", value="Removes the role defined from the member", inline=False
    ).add_field(name=prefix+"massrole `<role1>` `<role2>`", value="Members having role1 will be given role2", inline=False
    ).add_field(name=prefix+"massroleremove `<role1>` `<role2>`", value="Members having role1 will loose role2 if they have it", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def rrhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="✨ Reaction Roles", description="Whether it be default, custom, animated or even deleted after setting up - All types of emojis are allowed!", color=var.C_MAIN
    ).add_field(name=prefix+"rr `<#channel>` `<messageid>` `<role>` `<emoji>`", value="Adds a reaction role", inline=False
    ).add_field(name=prefix+"removerr `<messageid>` `<emoji>`", value="Removes the reaction role", inline=False
    ).add_field(name=prefix+"allrr", value="Shows all active reaction roles in the server", inline=False
    ).add_field(name=prefix+"uniquerr `<messageid>`", value="Marks a message with unique reactions! Users would be able to react once hence take one role from the message", inline=False
    ).add_field(name=prefix+"removeunique `<messageid>`", value="Unmarks the message with unique reactions! Users would be able to react multiple times hence take multiple roles from the message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/843530558126817280/Logo.png")
    return embed

async def welcomehelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="👋 Welcome", description="Greet new members with a nice welcome :D", color=var.C_MAIN
    ).add_field(name=prefix+"welcomecard", value="Shows server welcome card", inline=False
    ).add_field(name=prefix+"welcomechannel `<#channel>`", value="Changes welcome channel", inline=False
    ).add_field(name=prefix+"welcomemessage", value="Changes welcome message", inline=False
    ).add_field(name=prefix+"welcomegreeting", value="Changes welcome greeting", inline=False
    ).add_field(name=prefix+"welcomeimage", value="Changes the welcome image", inline=False
    ).add_field(name=prefix+"welcomerole `<role>`", value="Assign automatic role to a member when they join", inline=False
    ).add_field(name=prefix+"welcomereset", value="Resets to the default welcome embed message", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def verifyhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="✅ Verification", description="Keep the server safe from raiders and bots!", color=var.C_MAIN
    ).add_field(name=prefix+"verifyinfo", value="Shows information of verification setup", inline=False
    ).add_field(name=prefix+"verifychannel `<#channel>`", value="Changes the verification channel", inline=False
    ).add_field(name=prefix+"verifyswitch", value="Switches between verification type", inline=False
    ).add_field(name=prefix+"verifyrole `<role>`", value="Give a role to users when they successfully verify", inline=False
    ).add_field(name=prefix+"verifyroleremove `<role>`", value="Remove a verified role if setted up", inline=False
    ).add_field(name=prefix+"verifyremove", value="Removes verification entirely by clearing all configs and disabling the plugin", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
    ).set_footer(text="For verify role, you can only set one at a time, if a verify role is already setted up then setting up another one will replace the existing one")
    return embed

async def chatbothelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="🤖 Chatbot", description="I will reply to pings in every channel however setting up a bot chat channel won't require you ping me!" ,color=var.C_MAIN,
    ).add_field(name=prefix+"setchatbot `<#channel>`", value="Makes a channel for chatting with me! All messages sent there will be replied by me :D", inline=False
    ).add_field(name=prefix+"removechatbot `<#channel>`", value="Removes a chatbot channel", inline=False
    ).add_field(name=prefix+"chatbotchannels", value="Shows all channels where chat bot is enabled", inline=False
    ).add_field(name=prefix+"chatbotreport `<description>`", value="Sends report/bug related to the chatbot directly to the [Support server](https://discord.gg/KTn4TgwkUT)!"
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def automodhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="🛡️ Auto Moderation", description="I will try my best to keep the chats clean!" ,color=var.C_MAIN,
    ).add_field(name=prefix+"filters", value="Shows all available Auto-Moderation", inline=False
    ).add_field(name=prefix+"automodblacklist `<#channel>`", value="Blacklists a channel from Auto-Moderation, hence automod won't work there", inline=False
    ).add_field(name=prefix+"automodwhitelist `<#channel>`", value="Whitelists a channel from Auto-Moderation, hence automod would work there", inline=False
    ).add_field(name=prefix+"addmodrole", value="Adds a mod role, members with this role are immune to all Auto-Moderation actions", inline=False
    ).add_field(name=prefix+"removemodrole", value="Removes any existing mod role which would make the role affected by Auto-Moderation", inline=False
    ).add_field(name=prefix+"allmodroles", value="Shows all mod roles which are immune to Auto-Moderation", inline=False
    ).add_field(name=prefix+"ignorebots", value="Toggles between whether bots should be affect or not", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def karmahelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="🎭 Karma", description="Let's see who is the nicest member!" ,color=var.C_MAIN,
    ).add_field(name=prefix+"karma `<user>`", value="Shows server karma of the user! User field is optional for checking karma of yourself", inline=False
    ).add_field(name=prefix+"karmaboard", value="Shows the karma leaderboard of server members", inline=False
    ).add_field(name=prefix+"kblacklist", value="Blacklists a channel from karma system hence members won't gain any karma there", inline=False
    ).add_field(name=prefix+"kwhitelist", value="Whitelists a channel therefore letting users gain karma again in that channel", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def settingshelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title=f"{var.E_SETTINGS} Settings", description="Configure my settings and plugins for this server :D", color=var.C_MAIN
    ).add_field(name=prefix+"plugins",value="Manage your plugins", inline=False
    ).add_field(name=prefix+"prefix", value="View or change my prefix", inline=False
    ).add_field(name=prefix+"setperm `<plugin>`",value="Adds a command role permission, users with the role defined will be able to use the command from the plugin", inline=False
    ).add_field(name=prefix+"removeperm `<command_name>` `<role>`",value="Removes command role permission, users with that role defined would no longer be able to use the command", inline=False
    ).add_field(name=prefix+"allperms",value="Shows all commands with the roles that have permission to use it", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def funhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title=f"🎯 Fun", description="Let's have some fun!", color=var.C_MAIN
    ).add_field(name=prefix+"typeracer", value="Quickly join a type racing queue with most players! Make sure that I can DM you for this to work", inline=False
    ).add_field(name=prefix+"typeracer new `<player_count>`", value="Create your own type racing match, share the code with your friends for them to join!", inline=False
    ).add_field(name=prefix+"typeracer join `<code>`", value="Join a type racing match. Make sure the code is valid!", inline=False
    ).add_field(name=prefix+"typeracer exit", value="Leave the type racing queue in which you are currently in", inline=False
    ).add_field(name=prefix+"typingtest `<type>`",value="Starts a solo typing test! There are two types: `time` and `word`", inline=False
    ).add_field(name=prefix+"avatar `<user>`", value="Shows avatar of any user! Works with users outside the server if User ID is correct", inline=False
    ).add_field(name=prefix+"embed `<#channel>`",value="Generate an embed!", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def giveawayhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title=f"🎉 Giveaway", description="", color=var.C_MAIN
    ).add_field(name=prefix+"gstart", value="Starts a new giveaway!", inline=False
    ).add_field(name=prefix+"gend `<message_id>`", value="Ends a giveaway, this does not cancel it instead ends the giveaway regardless of time left", inline=False
    ).add_field(name=prefix+"gshow", value="Shows all active giveaways", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed

async def extrahelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = discord.Embed(title="▶️ Extras", 
    description="Commands that are useful but don't belong to other categories!", color=var.C_MAIN
    ).add_field(name=prefix+"stats", value="Shows server statistics", inline=False
    ).add_field(name=prefix+"about", value="Shows information about me!", inline=False
    ).add_field(name=prefix+"suggest `<youridea>`",value="Sends an idea directly to the support server!", inline=False
    ).add_field(name=prefix+"invite",value="Sends my bot invite link!", inline=False
    ).add_field(name=prefix+"source", value="Sends link to my Github repository since I am open source :D", inline=False
    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
    return embed


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id}, {"_id": 0})
        prefix = await get_prefix(ctx)
        embed = discord.Embed(
        title="Help subcommands for all **enabled plugins**\nEnable/Disable plugins to view more/less help",
        description="[Donation](https://paypal.me/palbolt) [Vote](https://top.gg/bot/843484459113775114/vote) [Support](https://discord.gg/hxc73psNsB)",
        color=var.C_MAIN
        ).set_footer(text="Either use the subcommand or react to the emojis below"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")

        for i in GuildDoc:
            if GuildDoc.get(i):
                helpname = i.lower()
                if i.lower() == "reactionroles": #Reaction roles command doesn't have space in between reaction and roles
                    helpname = i.lower().replace(" ", "")
                embed.add_field(name=f"{prefix}help {helpname}", value=f"{var.DICT_PLUGINEMOJIS.get(i)} {i} Help", inline=False)

        embed.add_field(name=f"{prefix}help extras", value=f"▶️ Non plugin commands", inline=False)
        embed.add_field(name=f"{prefix}help settings", value=f"{var.E_SETTINGS} Configure settings", inline=False)
        helpmsg = await ctx.send(embed=embed)

        for i in GuildDoc:
            if GuildDoc.get(i):
                await helpmsg.add_reaction(var.DICT_PLUGINEMOJIS.get(i))
        await helpmsg.add_reaction("▶️")
        await helpmsg.add_reaction(var.E_SETTINGS)
        
        def check(reaction, user):
            return user == ctx.author and reaction.message == helpmsg


        HelpDict = {
            "Leveling": levelhelp,
            "Moderation": modhelp,
            "ReactionRoles":rrhelp,
            "Welcome": welcomehelp,
            "Verification": verifyhelp,
            "Chatbot": chatbothelp,
            "AutoMod": automodhelp,
            "Karma": karmahelp,
            "Fun": funhelp,
            "Giveaway": giveawayhelp
            
        }

        try:
            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30.0)
                if str(reaction.emoji) in var.DICT_PLUGINEMOJIS.values():

                    helptype = list(var.DICT_PLUGINEMOJIS.keys())[list(var.DICT_PLUGINEMOJIS.values()).index(str(reaction.emoji))]
                    await helpmsg.edit(embed=await HelpDict.get(helptype)(ctx))
                    try:
                        await helpmsg.remove_reaction(str(reaction.emoji), ctx.author)
                    except discord.Forbidden:
                        pass
                
                #Since extra help and plugin is always there
                if str(reaction.emoji) == "▶️":
                    await helpmsg.edit(embed=await extrahelp(ctx))
                    try:
                        await helpmsg.remove_reaction("▶️", ctx.author)
                    except discord.Forbidden:
                        pass
                if str(reaction.emoji) == var.E_SETTINGS:
                    await helpmsg.edit(embed=await settingshelp(ctx))
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


           
    @help.command(aliases=["levels"])
    async def leveling(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Leveling") == True:
            await ctx.send(embed=await levelhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Leveling plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command(aliases=["mod", "moderator"])
    async def moderation(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Moderation") == True:
            await ctx.send(embed=await modhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command(aliases=["reaction_roles", "rr", "reaction-roles"])
    async def reactionroles(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("ReactionRoles") == True:
            await ctx.send(embed=await rrhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Reaction Roles plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def welcome(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome") == True:
            await ctx.send(embed=await welcomehelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command(aliases=["verify"])
    async def verification(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification") == True:
            await ctx.send(embed=await verifyhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Verification plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def chatbot(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot") == True:
            await ctx.send(embed=await chatbothelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Chatbot plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command(aliases=["automoderation", "automoderator"])
    async def automod(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("AutoMod") == True:
            await ctx.send(embed=await automodhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Auto-Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def karma(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Karma") == True:
            await ctx.send(embed=await karmahelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Karma plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def fun(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Fun") == True:
            await ctx.send(embed=await funhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Fun plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def giveaway(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Giveaway") == True:
            await ctx.send(embed=await giveawayhelp(ctx))
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Fun plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @help.command()
    async def extras(self, ctx):
        await ctx.send(embed=await extrahelp(ctx))
    
    @help.command()
    async def settings(self, ctx):
        await ctx.send(embed=await settingshelp(ctx))


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def levelconfig(self, ctx):
        prefix = await get_prefix(ctx)
        embed = discord.Embed(title="Configure leveling for this server",
        color=var.C_TEAL
        ).add_field(name=prefix+"xprange `<leastamount>` `<highestamount>`",value="Set the range between which users will be awarded with random xp", inline=False
        ).add_field(name=prefix+"blacklist `<#channel>`",value=f"Add the channel where you don't want users to gain xp.", inline=False
        ).add_field(name=prefix+"whitelist `<#channel>`",value=f"Whitelist an xp blacklisted channel.", inline=False
        ).add_field(name=prefix+"alertchannel `<#channel>`", value="Define the channel where alerts will be sent for level ups!", inline=False
        ).add_field(name=prefix+"togglealerts", value="Disable or Enable alert message for level ups!", inline=False
        ).add_field(name=prefix+"reward `<level>` `<role>`", value="Setup awards for reaching certain level! For level only use the number", inline=False
        ).add_field(name=prefix+"removereward `<level>`", value="Removes the role reward for that level!", inline=False
        ).set_footer(text=f"Leveling is a plugin so to disable it, use the command {prefix}plugins and click on the leveling emoji to toggle")
        #).add_field(name=prefix+"maxlevel `<amount>`", value="Define the max level which can be achieved by a user", inline=False
        #).add_field(name=prefix+"alertmessage `<message>`", value=f"Change the alert message! Use these values in between:\n[user] [xp] [level]\n Make sure to put them between square brackets!", inline=False
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
