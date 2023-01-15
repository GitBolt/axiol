import disnake
from disnake.ext import commands
import constants as var
import database as db
from functions import get_prefix
import asyncio


async def levelhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(title=f"{var.E_LEVELING}  Leveling", color=var.C_MAIN)
        .add_field(
            name=prefix + "rank `<user>`",
            value=(
                "Shows server rank of the user!"
                " User field is optional for checking rank of yourself"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "leaderboard",
            value="Shows the server leaderboard",
            inline=False,
        )
        .add_field(
            name=prefix + "bargraph `<amount>`",
            value=(
                "Shows a Bar chart of top users! Amount field is optional since 10"
                " users are shown by default and max amount is 30"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "piechart `<amount>`",
            value="Shows a Pie chart of top 10 users!",
            inline=False,
        )
        .add_field(
            name=prefix + "givexp `<user>` `<amount>`",
            value="Gives user more XP",
            inline=False,
        )
        .add_field(
            name=prefix + "removexp `<user>` `<amount>`",
            value="Removes user more XP",
            inline=False,
        )
        .add_field(
            name=prefix + "levelinfo",
            value="Shows the server's leveling settings",
            inline=False,
        )
        .add_field(
            name=prefix + "levelconfig",
            value=f"Configure leveling settings",
            inline=False,
        )
        .set_thumbnail(
            url="https://cdn.disnakeapp.com/"
            "attachments/843519647055609856/845662999686414336/Logo1.png"
        )
    )


async def modhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)

    return (
        disnake.Embed(
            title="🔨 Moderation",
            description="Reasons in every command except warn is optional :)",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "ban `<user>` `<reason>`",
            value="Bans a user from the server",
            inline=False,
        )
        .add_field(
            name=prefix + "unban `<user>`",
            value="Unbans any already banned user",
            inline=False,
        )
        .add_field(
            name=prefix + "kick `<member>` `<reason>`",
            value="Kicks the user out of the server",
            inline=False,
        )
        .add_field(
            name=prefix + "mute `<member>`",
            value=(
                "Disables the ability for users to send text"
                " messages in all channels"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "unmute `<member>`",
            value="Removes the 'Muted' role therefore lets the user send messages",
            inline=False,
        )
        .add_field(
            name=prefix + "warn `<member>` `<reason>`",
            value="Warns a member, reason is mandatory",
            inline=False,
        )
        .add_field(
            name=prefix + "removewarn `<member>` `<warn_position>`",
            value="Removes the warn from the position defined from the member",
            inline=False,
        )
        .add_field(
            name=prefix + "warns `<member>`",
            value="Shows all warns of the member",
            inline=False,
        )
        .add_field(
            name=prefix + "purge `<amount>`",
            value=(
                "Deletes the number of messages defined "
                "in the command from the channel"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "nick `<member>` `<member>`",
            value="Changes nickname of a member",
            inline=False,
        )
        .add_field(
            name=prefix + "addrole `<member>` `<role>`",
            value="Gives the member the role defined",
            inline=False,
        )
        .add_field(
            name=prefix + "removerole `<member>` `<role>`",
            value="Removes the role defined from the member",
            inline=False,
        )
        .add_field(
            name=prefix + "massrole `<role1>` `<role2>`",
            value="Members having role1 will be given role2",
            inline=False,
        )
        .add_field(
            name=prefix + "massroleremove `<role1>` `<role2>`",
            value="Members having role1 will loose role2 if they have it",
            inline=False,
        )
        .add_field(
            name=prefix + "modlog", value="Toggle moderation action logs!", inline=False
        )
        .set_thumbnail(
            url="https://cdn.disnakeapp.com/attachments/"
            "843519647055609856/845662999686414336/Logo1.png"
        )
    )


async def rrhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title="✨ Reaction Roles",
            description=(
                "Whether it be default, custom, animated or even deleted after "
                "setting up - All types of emojis are allowed!"
            ),
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "rr `<#channel>` `<messageid>` `<role>` `<emoji>`",
            value="Adds a reaction role",
            inline=False,
        )
        .add_field(
            name=prefix + "removerr `<messageid>` `<emoji>`",
            value="Removes the reaction role",
            inline=False,
        )
        .add_field(
            name=prefix + "allrr",
            value="Shows all active reaction roles in the server",
            inline=False,
        )
        .add_field(
            name=prefix + "uniquerr `<messageid>`",
            value=(
                "Marks a message with unique reactions! Users would be able to"
                " react once hence take one role from the message"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "removeunique `<messageid>`",
            value=(
                "Unmarks the message with unique reactions! "
                "Users would be able to react multiple times hence take multiple"
                " roles from the message"
            ),
            inline=False,
        )
        .set_thumbnail(
            url="https://cdn.disnakeapp.com/attachments/843519647055609856/"
            "843530558126817280/Logo.png"
        )
    )


async def welcomehelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title="👋 Welcome",
            description="Greet new members with a nice welcome :D",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "wcard", value="Shows server welcome card", inline=False
        )
        .add_field(
            name=prefix + "wchannel `<#channel>`",
            value="Changes welcome channel",
            inline=False,
        )
        .add_field(
            name=prefix + "wmessage", value="Changes welcome message", inline=False
        )
        .add_field(
            name=prefix + "wgreeting", value="Changes welcome greeting", inline=False
        )
        .add_field(
            name=prefix + "wimage", value="Changes the welcome image", inline=False
        )
        .add_field(
            name=prefix + "wrole `<role>`",
            value="Assign automatic role to a member when they join",
            inline=False,
        )
        .add_field(
            name=prefix + "wbots",
            value="Changes whether bots should be greeted or not",
            inline=False,
        )
        .add_field(
            name=prefix + "wreset",
            value="Resets to the default welcome embed message",
            inline=False,
        )
        .set_thumbnail(
            url="https://cdn.disnakeapp.com/attachments/843519647055609856/"
            "845662999686414336/Logo1.png"
        )
    )


async def verifyhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    embed = (
        disnake.Embed(
            title="✅ Verification",
            description="Keep the server safe from raiders and bots!",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "verifyinfo",
            value="Shows information of verification setup",
            inline=False,
        )
        .add_field(
            name=prefix + "verifychannel `<#channel>`",
            value="Changes the verification channel",
            inline=False,
        )
        .add_field(
            name=prefix + "verifyswitch",
            value="Switches between verification type",
            inline=False,
        )
        .add_field(
            name=prefix + "verifyrole `<role>`",
            value="Give a role to users when they successfully verify",
            inline=False,
        )
        .add_field(
            name=prefix + "verifyroleremove `<role>`",
            value="Remove a verified role if setted up",
            inline=False,
        )
        .add_field(
            name=prefix + "verifyremove",
            value=(
                "Removes verification entirely by clearing all configs"
                " and disabling the plugin"
            ),
            inline=False,
        )
        .set_thumbnail(
            url="https://cdn.disnakeapp.com/attachments/843519647055609856/"
            "845662999686414336/Logo1.png"
        )
        .set_footer(
            text=(
                "For verify role, you can only set one at a time, if a verify role"
                " is already setup then setting up another one will replace the"
                " existing one"
            )
        )
    )

    return embed


async def chatbothelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title="🤖 Chatbot",
            description=(
                "I will reply to pings in every channel however setting up "
                "a bot chat channel won't require you ping me!"
            ),
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "setchatbot `<#channel>`",
            value="Makes a channel for chatting with me! All messages sent there will be replied by me :D",
            inline=False,
        )
        .add_field(
            name=prefix + "removechatbot `<#channel>`",
            value="Removes a chatbot channel",
            inline=False,
        )
        .add_field(
            name=prefix + "chatbotchannels",
            value="Shows all channels where chat bot is enabled",
            inline=False,
        )
        .add_field(
            name=prefix + "chatbotreport `<description>`",
            value=(
                "Sends report/bug related to the chatbot directly to the"
                " [Support server](https://disnake.gg/KTn4TgwkUT)!"
            ),
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


async def automodhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title="🛡️ Auto Moderation",
            description="I will try my best to keep the chats clean!",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "filters",
            value="Shows all available Auto-Moderation",
            inline=False,
        )
        .add_field(
            name=prefix + "automodblacklist `<#channel>`",
            value=(
                "Blacklists a channel from Auto-Moderation,"
                " hence automod won't work there"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "automodwhitelist `<#channel>`",
            value=(
                "Whitelists a channel from Auto-Moderation,"
                " hence automod would work there"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "addmodrole",
            value=(
                "Adds a mod role, members with this role are immune to all"
                " Auto-Moderation actions"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "removemodrole",
            value=(
                "Removes any existing mod role which would make the role "
                "affected by Auto-Moderation"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "allmodroles",
            value="Shows all mod roles which are immune to Auto-Moderation",
            inline=False,
        )
        .add_field(
            name=prefix + "ignorebots",
            value="Toggles between whether bots should be affect or not",
            inline=False,
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


async def karmahelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)

    return (
        disnake.Embed(
            title="🎭 Karma",
            description="Let's see who is the nicest member!",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "karma `<user>`",
            value=(
                "Shows server karma of the user! "
                "User field is optional for checking karma of yourself"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "karmaboard",
            value="Shows the karma leaderboard of server members",
            inline=False,
        )
        .add_field(
            name=prefix + "kblacklist",
            value=(
                "Blacklists a channel from karma system hence members "
                "won't gain any karma there"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "kwhitelist",
            value=(
                "Whitelists a channel therefore letting users"
                " gain karma again in that channel"
            ),
            inline=False,
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


async def settingshelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title=f"{var.E_SETTINGS} Settings",
            description="Configure my settings and plugins for this server :D",
            color=var.C_MAIN,
        )
        .add_field(name=prefix + "plugins", value="Manage your plugins", inline=False)
        .add_field(
            name=prefix + "prefix", value="View or change my prefix", inline=False
        )
        .add_field(
            name=prefix + "setperm `<plugin>`",
            value=(
                "Adds a command role permission, users with the role defined will"
                " be able to use the command from the plugin"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "removeperm `<command_name>` `<role>`",
            value=(
                "Removes command role permission, users with that role defined "
                "would no longer be able to use the command"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "allperms",
            value="Shows all commands with the roles that have permission to use it",
            inline=False,
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


async def funhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title=f"🎯 Fun",
            description="Let's have some fun!",
            color=var.C_MAIN,
        )
        .add_field(
            name=prefix + "typeracer",
            value=(
                "Quickly join a type racing queue with most players! "
                "Make sure that I can DM you for this to work"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "typeracer new `<player_count>`",
            value=(
                "Create your own type racing match,"
                " share the code with your friends for them to join!"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "typeracer join `<code>`",
            value=("Join a type racing match. Make sure the code is valid!"),
            inline=False,
        )
        .add_field(
            name=prefix + "typeracer exit",
            value="Leave the type racing queue in which you are currently in",
            inline=False,
        )
        .add_field(
            name=prefix + "typingtest `<duration>`",
            value=(
                "Starts a solo typing test! If duration is not specified then a quick test with small text and 60 seconds duration is started"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "avatar `<user>`",
            value=(
                "Shows avatar of any user! "
                "Works with users outside the server if User ID is correct"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "embed `<#channel>`",
            value="Generate an embed!",
            inline=False,
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
            )
        )
    )


async def giveawayhelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)

    return (
        disnake.Embed(title=f"🎉 Giveaway", description="", color=var.C_MAIN)
        .add_field(name=prefix + "gstart", value="Starts a new giveaway!", inline=False)
        .add_field(
            name=prefix + "gend `<message_id>`",
            value=(
                "Ends a giveaway, this does not cancel it instead "
                "ends the giveaway regardless of time left"
            ),
            inline=False,
        )
        .add_field(
            name=prefix + "gshow", value="Shows all active giveaways", inline=False
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


async def extrahelp(ctx: commands.Context):
    prefix = await get_prefix(ctx)
    return (
        disnake.Embed(
            title="▶️ Extras",
            description=(
                "Commands that are useful but don't belong to other categories!"
            ),
            color=var.C_MAIN,
        )
        .add_field(name=prefix + "stats", value="Shows server statistics", inline=False)
        .add_field(
            name=prefix + "about", value="Shows information about me!", inline=False
        )
        .add_field(
            name=prefix + "suggest `<youridea>`",
            value="Sends an idea directly to the support server!",
            inline=False,
        )
        .add_field(
            name=prefix + "invite", value="Sends my bot invite link!", inline=False
        )
        .add_field(
            name=prefix + "source",
            value="Sends link to my Github repository since I am open source :D",
            inline=False,
        )
        .set_thumbnail(
            url=(
                "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )
    )


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, invoke_without_command=True)
    async def help(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id}, {"_id": 0})
        prefix = await get_prefix(ctx)
        embed = (
            disnake.Embed(
                title=(
                    "Help subcommands for all **enabled plugins**\nEnable/Disable "
                    "plugins to view more/less help"
                ),
                description=(
                    "[Donation](https://paypal.me/palbolt) "
                    "[Vote](https://top.gg/bot/843484459113775114/vote) "
                    "[Support](https://disnake.gg/hxc73psNsB)"
                ),
                color=var.C_MAIN,
            )
            .set_footer(text="Either use the subcommand or react to the emojis below")
            .set_thumbnail(
                url=(
                    "https://cdn.disnakeapp.com/attachments/843519647055609856/"
                    "845662999686414336/Logo1.png"
                )
            )
        )

        for i in guild_doc:
            if guild_doc.get(i):
                help_name = i.lower()

                # Reaction roles command doesn't have space
                # in between reaction and roles
                if i.lower() == "reactionroles":
                    help_name = i.lower().replace(" ", "")

                embed.add_field(
                    name=f"{prefix}help {help_name}",
                    value=f"{var.DICT_PLUGIN_EMOJIS.get(i)} {i} Help",
                    inline=False,
                )

        embed.add_field(
            name=f"{prefix}help extras", value=f"▶️ Non plugin commands", inline=False
        )

        embed.add_field(
            name=f"{prefix}help settings",
            value=f"{var.E_SETTINGS} Configure settings",
            inline=False,
        )

        help_msg = await ctx.send(embed=embed)

        for i in guild_doc:
            if guild_doc.get(i):
                await help_msg.add_reaction(var.DICT_PLUGIN_EMOJIS.get(i))

        await help_msg.add_reaction("▶️")
        await help_msg.add_reaction(var.E_SETTINGS)

        def check(r, u):
            return u == ctx.author and r.message == help_msg

        help_dict = {
            "Leveling": levelhelp,
            "Moderation": modhelp,
            "ReactionRoles": rrhelp,
            "Welcome": welcomehelp,
            "Verification": verifyhelp,
           # "Chatbot": chatbothelp,
            "AutoMod": automodhelp,
            # "Karma": karmahelp,
            "Fun": funhelp,
            "Giveaway": giveawayhelp,
        }

        try:
            while True:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=30.0
                )

                if str(reaction.emoji) in var.DICT_PLUGIN_EMOJIS.values():
                    help_type = list(var.DICT_PLUGIN_EMOJIS.keys())[
                        list(var.DICT_PLUGIN_EMOJIS.values()).index(str(reaction.emoji))
                    ]

                    await help_msg.edit(embed=await help_dict.get(help_type)(ctx))

                    try:
                        await help_msg.remove_reaction(str(reaction.emoji), ctx.author)

                    except disnake.Forbidden:
                        pass

                # Since extra help and plugin is always there
                if str(reaction.emoji) == "▶️":
                    await help_msg.edit(embed=await extrahelp(ctx))

                    try:
                        await help_msg.remove_reaction("▶️", ctx.author)

                    except disnake.Forbidden:
                        pass

                if str(reaction.emoji) == var.E_SETTINGS:
                    await help_msg.edit(embed=await settingshelp(ctx))

                    try:
                        await help_msg.remove_reaction(var.E_SETTINGS, ctx.author)

                    except disnake.Forbidden:
                        pass

        except asyncio.TimeoutError:
            try:
                await help_msg.clear_reactions()

            except disnake.Forbidden:
                await help_msg.remove_reaction(var.E_SETTINGS, self.bot.user)

                for i in guild_doc:
                    if guild_doc.get(i):
                        await help_msg.remove_reaction(
                            var.DICT_PLUGIN_EMOJIS.get(i), self.bot.user
                        )

                await help_msg.remove_reaction("▶️", self.bot.user)

    @help.command(aliases=["levels"])
    async def leveling(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Leveling"):
            await ctx.send(embed=await levelhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Leveling plugin is "
                        "disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command(aliases=["mod", "moderator"])
    async def moderation(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Moderation") == True:
            await ctx.send(embed=await modhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Moderation plugin "
                        "is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command(
        name="reactionroles", aliases=["reaction_roles", "rr", "reaction-roles"]
    )
    async def reaction_roles(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("ReactionRoles"):
            await ctx.send(embed=await rrhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Reaction Roles plugin"
                        f" is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def welcome(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Welcome"):
            await ctx.send(embed=await welcomehelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Welcome plugin "
                        f"is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command(aliases=["verify"])
    async def verification(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Verification"):
            await ctx.send(embed=await verifyhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Verification plugin "
                        "is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def chatbot(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Chatbot"):
            await ctx.send(embed=await chatbothelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Chatbot plugin "
                        "is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command(aliases=["automoderation", "automoderator"])
    async def automod(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("AutoMod"):
            await ctx.send(embed=await automodhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Auto-Moderation plugin"
                        f" is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def karma(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Karma"):
            await ctx.send(embed=await karmahelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Karma plugin"
                        " is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def fun(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Fun"):
            await ctx.send(embed=await funhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Fun plugin is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def giveaway(self, ctx):
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Giveaway"):
            await ctx.send(embed=await giveawayhelp(ctx))

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Fun plugin" f" is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @help.command()
    async def extras(self, ctx):
        await ctx.send(embed=await extrahelp(ctx))

    @help.command()
    async def settings(self, ctx):
        await ctx.send(embed=await settingshelp(ctx))

    @commands.command(name="levelconfig")
    @commands.has_permissions(administrator=True)
    async def level_config(self, ctx):
        prefix = await get_prefix(ctx)
        embed = (
            disnake.Embed(title="Configure leveling for this server", color=var.C_TEAL)
            .add_field(
                name=prefix + "xprange `<leastamount>` `<highestamount>`",
                value=(
                    "Set the range between which users "
                    "will be awarded with random xp"
                ),
                inline=False,
            )
            .add_field(
                name=prefix + "blacklist `<#channel>`",
                value=f"Add the channel where you don't want users to gain xp.",
                inline=False,
            )
            .add_field(
                name=prefix + "whitelist `<#channel>`",
                value=f"Whitelist an xp blacklisted channel.",
                inline=False,
            )
            .add_field(
                name=prefix + "alertchannel `<#channel>`",
                value="Define the channel where alerts will be sent for level ups!",
                inline=False,
            )
            .add_field(
                name=prefix + "togglealerts",
                value="Disable or Enable alert message for level ups!",
                inline=False,
            )
            .add_field(
                name=prefix + "reward `<level>` `<role>`",
                value=(
                    "Setup awards for reaching certain level! "
                    "For level only use the number"
                ),
                inline=False,
            )
            .add_field(
                name=prefix + "removereward `<level>`",
                value="Removes the role reward for that level!",
                inline=False,
            )
            .set_footer(
                text=(
                    f"Leveling is a plugin so to disable it, use the command"
                    f" {prefix}plugins and click on the leveling emoji to toggle"
                )
            )
        )
        # ).add_field(name=prefix+"maxlevel `<amount>`",
        # value="Define the max level which can be achieved by a user",
        # inline=False

        # ).add_field(name=prefix+"alertmessage `<message>`",
        # value=f"Change the alert message! Use these values in between:\n[
        # user] [xp] [level]\n Make sure to put them between square brackets!",
        # inline=False
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
