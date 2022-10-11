import asyncio
import disnake
from disnake.ext import commands
from disnake.ext.commands import check, Context
import constants as var
import database as db
from functions import get_prefix


def user_or_admin(my_id):
    async def predicate(ctx: Context):
        return ctx.author.id == my_id or ctx.author.guild_permissions.administrator

    return check(predicate)


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["plugin", "extensions", "extentions", "addons"])
    @user_or_admin(791950104680071188)  # This me
    async def plugins(self, ctx):
        guild_doc = await db.PLUGINS.find_one(
            {"_id": ctx.guild.id}, {"_id": False}
        )  # Getting guild's plugin document and removing the ID

        enabled_amount = len(
            [keys for keys, values in guild_doc.items() if values == True]
        )

        total_amount = len(guild_doc)

        embed = (
            disnake.Embed(
                title="All available plugins",
                description=(
                    "React to the respective emojis below to enable/disable them!"
                ),
                color=var.C_MAIN,
            )
            .set_footer(
                text=(
                    f"{enabled_amount}/{total_amount}"
                    " plugins are enabled in this server"
                )
            )
            .set_thumbnail(
                url=(
                    "https://cdn.discord.com/attachments/843519647055609856/"
                    "845662999686414336/Logo1.png"
                )
            )
        )

        for i in guild_doc:
            status = "Enabled" if guild_doc.get(i) == True else "Disabled"
            embed.add_field(
                name=i, value=f"{var.DICT_PLUGIN_EMOJIS.get(i)} {status}", inline=False
            )

        bot_msg = await ctx.send(embed=embed)

        for i in guild_doc:
            print(i, var.DICT_PLUGIN_EMOJIS.get(i))
            await bot_msg.add_reaction(var.DICT_PLUGIN_EMOJIS.get(i))

        def reaction_check(r, user):
            if str(r.emoji) in var.DICT_PLUGIN_EMOJIS.values():
                return user == ctx.author and r.message == bot_msg

        def enable_check(r, user):
            if str(r.emoji) == var.E_ENABLE:
                return user == ctx.author and r.message == enabled_bot_msg

        def disable_check(r, user):
            if str(r.emoji) == var.E_DISABLE:
                return user == ctx.author and r.message == enabled_bot_msg

        while True:
            try:
                reaction, _ = await self.bot.wait_for(
                    "reaction_add", check=reaction_check, timeout=60.0
                )

                guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

                try:
                    await bot_msg.clear_reactions()

                except disnake.Forbidden:
                    pass

                plugin_type = list(var.DICT_PLUGIN_EMOJIS.keys())[
                    list(var.DICT_PLUGIN_EMOJIS.values()).index(str(reaction.emoji))
                ]

                embed = disnake.Embed(
                    title=f"{plugin_type} Plugin",
                )

                if guild_doc.get(plugin_type):
                    embed.description = (
                        f"{var.E_ENABLE} {plugin_type} is currently enabled"
                    )

                    embed.color = var.C_GREEN

                    enabled_bot_msg = await ctx.send(embed=embed)
                    await enabled_bot_msg.add_reaction(var.E_DISABLE)

                    await self.bot.wait_for("reaction_add", check=disable_check)

                    new_data = {"$set": {plugin_type: False}}

                    await db.PLUGINS.update_one(guild_doc, new_data)

                    embed.title = f"{plugin_type} disabled"
                    embed.description = (
                        f"{var.E_DISABLE} {plugin_type}" f" plugin has been disabled"
                    )

                    embed.color = var.C_RED
                    await enabled_bot_msg.edit(embed=embed)

                    try:
                        await enabled_bot_msg.clear_reactions()

                    except disnake.Forbidden:
                        pass

                else:
                    embed.description = (
                        f"{var.E_DISABLE} {plugin_type} is currently disabled"
                    )

                    embed.color = var.C_RED
                    enabled_bot_msg = await ctx.send(embed=embed)
                    await enabled_bot_msg.add_reaction(var.E_ENABLE)

                    await self.bot.wait_for("reaction_add", check=enable_check)

                    new_data = {"$set": {plugin_type: True}}

                    await db.PLUGINS.update_one(guild_doc, new_data)

                    embed.title = f"{plugin_type} enabled"
                    embed.description = (
                        f"{var.E_ENABLE} {plugin_type}" " extension has been enabled"
                    )

                    embed.color = var.C_GREEN
                    await enabled_bot_msg.edit(embed=embed)
                    try:
                        await enabled_bot_msg.clear_reactions()
                    except disnake.Forbidden:
                        pass

                    # Since welcome and verification is not enabled by
                    # default, the time plugin is enabled,
                    # there is no information available in the db.

                    # Hence we ask for the channel and insert the data
                    # With leveling we just insert the default configs
                    if str(reaction.emoji) == "👋" and (
                        await db.WELCOME.find_one({"_id": ctx.guild.id}) is None
                    ):
                        await ctx.invoke(self.bot.get_command("welcomesetup"))

                    if str(reaction.emoji) == "✅" and (
                        await db.VERIFY.find_one({"_id": ctx.guild.id}) is None
                    ):
                        await ctx.invoke(self.bot.get_command("verifysetup"))

                    if str(reaction.emoji) == "🎭" and (
                        str(ctx.guild.id)
                        not in await db.KARMA_DATABASE.list_collection_names()
                    ):
                        guild_doc = await db.KARMA_DATABASE.create_collection(
                            str(ctx.guild.id)
                        )
                        guild_doc.insert_one(
                            {
                                "_id": 0,
                                "blacklists": [],
                            }
                        )

                    if str(reaction.emoji) == var.E_LEVELING and (
                        str(ctx.guild.id)
                        not in await db.LEVEL_DATABASE.list_collection_names()
                    ):
                        guild_doc = await db.LEVEL_DATABASE.create_collection(
                            str(ctx.guild.id)
                        )
                        guild_doc.insert_one(
                            {
                                "_id": 0,
                                "xprange": [15, 25],
                                "alertchannel": None,
                                "blacklistedchannels": [],
                                "alerts": True,
                                "rewards": {},
                            }
                        )

                    if str(reaction.emoji) == "🛡️" and (
                        await db.AUTO_MOD.find_one({"_id": ctx.guild.id}) is None
                    ):
                        await db.AUTO_MOD.insert_one(
                            {
                                "_id": ctx.guild.id,
                                "BadWords": {
                                    "status": True,
                                    "words": [
                                        "fuck",
                                        "bitch",
                                        "porn",
                                        "slut",
                                        "asshole",
                                    ],
                                    "response": "You aren't allowed to say that!",
                                },
                                "Invites": {
                                    "status": True,
                                    "response": "You can't send invites here!",
                                },
                                "Links": {
                                    "status": True,
                                    "response": "You can't send links here!",
                                },
                                "Mentions": {
                                    "status": False,
                                    "response": "You can't mention so many people!",
                                    "amount": 5,
                                },
                                "Settings": {
                                    "ignorebots": False,
                                    "blacklists": [],
                                    "modroles": [],
                                },
                            }
                        )

            except asyncio.TimeoutError:
                try:
                    await bot_msg.clear_reactions()
                except disnake.Forbidden:
                    pass

    @commands.command()
    @user_or_admin(791950104680071188)  # This me
    async def prefix(self, ctx):
        embed = disnake.Embed(
            title="Prefix :D that's the way you control me aye!",
            description=(
                f"The prefix for this server is\n"
                f"```{await get_prefix(ctx)}```\n"
                f"Wanna change it? React to the {var.E_SETTINGS} emoji below!"
            ),
            color=var.C_MAIN,
        )

        bot_msg = await ctx.send(embed=embed)
        await bot_msg.add_reaction(var.E_SETTINGS)

        def reaction_check(reaction, user):
            return user == ctx.author and reaction.message == bot_msg

        await self.bot.wait_for("reaction_add", check=reaction_check)

        await ctx.send(
            embed=disnake.Embed(
                description=(
                    "Next message which you will send will become the prefix "
                    ":eyes:\nTo cancel it enter\n"
                    f"```{await get_prefix(ctx)}cancel```"
                ),
                color=var.C_ORANGE,
            ).set_footer(text="Automatic cancellation after 1 minute")
        )

        try:
            await bot_msg.clear_reactions()

        except disnake.Forbidden:
            pass

        def message_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            user_msg = await self.bot.wait_for(
                "message", check=message_check, timeout=60.0
            )

            # Cancel
            if user_msg.content == await get_prefix(ctx) + "cancel":
                await ctx.send("Cancelled prefix change :ok_hand:")

            # Same prefixes so deleting the doc
            elif user_msg.content == var.DEFAULT_PREFIX:
                await db.PREFIXES.delete_one({"_id": ctx.guild.id})
                await ctx.send(
                    "Changed your prefix to the default one\n"
                    f"```{var.DEFAULT_PREFIX}```"
                )

            # If current prefix is default then insert new
            elif await get_prefix(ctx) == var.DEFAULT_PREFIX:
                await db.PREFIXES.insert_one(
                    {"_id": ctx.guild.id, "prefix": user_msg.content}
                )

                await ctx.send(
                    f"Updated your new prefix, it's\n```{user_msg.content}```"
                )

            else:  # Exists so just update it
                guild_doc = await db.PREFIXES.find_one({"_id": user_msg.guild.id})

                new_data = {"$set": {"prefix": user_msg.content}}

                await db.PREFIXES.update_one(guild_doc, new_data)
                await ctx.send(
                    f"Updated your new prefix, it's\n```{user_msg.content}```"
                )

        except asyncio.TimeoutError:
            await ctx.send(
                "You took too long to enter your "
                f"new prefix {ctx.author.mention} ;-;"
            )


def setup(bot):
    bot.add_cog(Settings(bot))
