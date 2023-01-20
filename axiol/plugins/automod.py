import re
import disnake
from disnake.ext import commands
import database as db
import constants as var
from functions import get_prefix
from ext.permissions import has_command_permission


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if guild_doc.get("AutoMod"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Auto-Moderation plugin"
                        " is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @commands.group(pass_context=True, invoke_without_command=True, aliases=["filter"])
    @has_command_permission()
    async def filters(self, ctx):
        embed = disnake.Embed(
            title="All Auto-Moderation filters",
            description=("Use the subcommand to configure each filter seperately!"),
            color=var.C_MAIN,
        )

        embed.set_footer(
            text=(
                "The emoji before filter name is their status "
                "whether they are enabled or disabled"
            )
        )

        guild_doc = await db.AUTO_MOD.find_one(
            {"_id": ctx.guild.id}, {"_id": 0, "Settings": 0}
        )

        for i in guild_doc:
            status = var.E_ENABLE if guild_doc[i]["status"] == True else var.E_DISABLE

            embed.add_field(
                name=status + " " + i,
                value=f"{await get_prefix(ctx)}filters {i.lower()}",
                inline=False,
            )

        await ctx.send(embed=embed)

    async def manage_filter(self, filter_name, embed, guild_doc, ctx):
        if guild_doc[filter_name]["status"]:
            embed.description = (
                f"{var.E_ENABLE} This Auto-Moderation filter" f" is currently enabled"
            )

            embed.color = var.C_GREEN
            if filter_name == "BadWords":
                embed.add_field(
                    name=f"{await get_prefix(ctx)}addbadword `<word>`",
                    value="Adds a word to bad word list",
                    inline=False,
                )

                embed.add_field(
                    name=f"{await get_prefix(ctx)}removebadword `<word>`",
                    value="Removes a word from bad word list",
                    inline=False,
                )

                embed.add_field(
                    name=f"{await get_prefix(ctx)}allbadwords",
                    value="Shows all bad words",
                    inline=False,
                )

            if filter_name == "Mentions":
                embed.add_field(
                    name=f"{await get_prefix(ctx)}mentionamount `<amount>`",
                    value=("Change the mention amount to delete, by default it's 5"),
                    inline=False,
                )

            embed.add_field(name="Response", value=f"React to {var.E_SETTINGS}")
            embed.add_field(name="Disable", value=f"React to {var.E_DISABLE}")
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction(var.E_SETTINGS)
            await bot_msg.add_reaction(var.E_DISABLE)

            def reaction_check(r, u):
                if str(r.emoji) in [var.E_DISABLE, var.E_SETTINGS]:
                    return u == ctx.author and r.message == bot_msg

            reaction, user = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            if str(reaction.emoji) == var.E_DISABLE:
                current_data = guild_doc[filter_name]
                new_dict = current_data.copy()
                new_dict["status"] = False

                new_data = {"$set": {filter_name: new_dict}}

                await db.AUTO_MOD.update_one(guild_doc, new_data)
                embed.title = f"{filter_name} filter disabled"
                embed.description = (
                    f"{var.E_DISABLE} This Auto-Moderation " "filter has been disabled"
                )

                embed.color = var.C_RED
                embed.clear_fields()
                await bot_msg.edit(embed=embed)
                try:
                    await bot_msg.clear_reactions()

                except disnake.Forbidden:
                    pass

            else:
                await ctx.send(
                    f"The next message which you will send will become the "
                    f"**{filter_name}** Auto-Moderation response!\n"
                    f"Type `cancel` to stop this proccess"
                )

                def message_check(message):
                    return (
                        message.author == ctx.author
                        and message.channel.id == ctx.channel.id
                    )

                user_msg = await self.bot.wait_for("message", check=message_check)

                if user_msg.content in ["cancel", "`cancel`", "```cancel```"]:
                    await ctx.send(f"Cancelled {filter_name} response change")

                else:
                    current_data = guild_doc[filter_name]
                    new_dict = current_data.copy()
                    new_dict["response"] = user_msg.content

                    new_data = {"$set": {filter_name: new_dict}}

                    await db.AUTO_MOD.update_one(guild_doc, new_data)
                    await ctx.send(
                        embed=disnake.Embed(
                            description=(
                                f"Successfully changed Auto-Moderation "
                                f"{filter_name} response to \n"
                                f"**{user_msg.content}**"
                            ),
                            color=var.C_GREEN,
                        )
                    )
        else:
            embed.description = (
                f"{var.E_DISABLE} This Auto-Moderation filter " f"is currently disabled"
            )

            embed.color = var.C_RED
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction(var.E_ENABLE)

            def enable_check(r, u):
                if str(r.emoji) == var.E_ENABLE:
                    return u == ctx.author and r.message == bot_msg

            reaction, user = await self.bot.wait_for("reaction_add", check=enable_check)

            current_data = guild_doc[filter_name]
            new_dict = current_data.copy()
            new_dict["status"] = True

            new_data = {"$set": {filter_name: new_dict}}

            await db.AUTO_MOD.update_one(guild_doc, new_data)

            embed.title = f"{filter_name} filter enabled"
            embed.description = (
                f"{var.E_ENABLE} This Auto-Moderation filter has been enabled"
            )

            embed.color = var.C_GREEN
            await bot_msg.edit(embed=embed)

            try:
                await bot_msg.clear_reactions()

            except disnake.Forbidden:
                pass

    @filters.command()
    @has_command_permission()
    async def invites(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id}, {"_id": 0})

        embed = disnake.Embed(title="Invites filter")
        await self.manage_filter("Invites", embed, guild_doc, ctx)

    @filters.command()
    @has_command_permission()
    async def links(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id}, {"_id": 0})
        embed = disnake.Embed(title="Links filter")
        await self.manage_filter("Links", embed, guild_doc, ctx)

    @filters.command(name="badwords")
    @has_command_permission()
    async def bad_words(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id}, {"_id": 0})
        embed = disnake.Embed(title="BadWords filter")
        await self.manage_filter("BadWords", embed, guild_doc, ctx)

    @filters.command()
    @has_command_permission()
    async def mentions(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id}, {"_id": 0})

        embed = disnake.Embed(title="Mentions filter")
        await self.manage_filter("Mentions", embed, guild_doc, ctx)

    @commands.command(name="addmodrole")
    @has_command_permission()
    async def add_mod_role(self, ctx, role: disnake.Role = None):
        if role is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            current_list = guild_doc["Settings"]["modroles"]
            new_list = current_list.copy()

            if role.id not in current_list:
                new_list.append(role.id)

                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"Settings.modroles": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        title="Successfully added mod role",
                        description=(
                            f"{role.mention} is immune from auto moderation now!"
                        ),
                        color=var.C_GREEN,
                    )
                )

            else:
                await ctx.send("This role is already a mod role")

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the role too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}addmodrole <role>```",
                )
            )

    @commands.command(name="removemodrole")
    @has_command_permission()
    async def remove_mod_role(self, ctx, role: disnake.Role = None):
        if role is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            current_list = guild_doc["Settings"]["modroles"]
            new_list = current_list.copy()

            if role.id in current_list:
                new_list.remove(role.id)

                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"Settings.modroles": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        title="Successfully removed mod role",
                        description=(
                            f"{role.mention} is not immune " "from auto moderation now!"
                        ),
                        color=var.C_GREEN,
                    )
                )

            else:
                await ctx.send("This role is not a mod role")

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the role too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}addmodrole <role>```",
                )
            )

    @commands.command(name="allmodroles")
    @has_command_permission()
    async def all_mod_roles(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
        if guild_doc is not None:
            embed = disnake.Embed(
                title="Moderator roles",
                description="These roles are immune to auto-moderation by me!",
                color=var.C_MAIN,
            )

            value = ""
            for i in guild_doc["Settings"]["modroles"]:
                role = ctx.guild.get_role(i)
                value += f"{role.mention} "

            if value != "":
                embed.add_field(name="Immune roles", value=value)
                await ctx.send(embed=embed)

            else:
                await ctx.send("There are no mod roles yet")

        else:
            await ctx.send("Auto moderation is not setted up yet")

    @commands.command(name="automodblacklist")
    @has_command_permission()
    async def automod_black_list(self, ctx, channel: disnake.TextChannel = None):
        if channel is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            if (
                guild_doc is not None
                and channel.id not in guild_doc["Settings"]["blacklists"]
            ):
                current_list = guild_doc["Settings"]["blacklists"]
                new_list = current_list.copy()
                new_list.append(channel.id)

                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"Settings.blacklists": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        title="Successfully blacklisted",
                        description=(
                            f"{channel.mention} is immune " "from auto moderation now!"
                        ),
                        color=var.C_GREEN,
                    )
                )

            else:
                await ctx.send("This channel is already blacklisted")

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the channel too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=(
                        f"```{await get_prefix(ctx)}automodblacklist" " <#channel>```"
                    ),
                )
            )

    @commands.command(name="automodwhitelist")
    @has_command_permission()
    async def auto_mod_whitelist(self, ctx, channel: disnake.TextChannel = None):
        if channel is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            if (
                guild_doc is not None
                and channel.id in guild_doc["Settings"]["blacklists"]
            ):
                current_list = guild_doc["Settings"]["blacklists"]
                new_list = current_list.copy()
                new_list.remove(channel.id)

                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"Settings.blacklists": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        title="Successfully whitelisted",
                        description=(
                            f"{channel.mention} is whitelisted hence affected "
                            "with auto moderation now!"
                        ),
                        color=var.C_GREEN,
                    )
                )

            else:
                await ctx.send(
                "This channel is not blacklisted hence" " can't whitelist either"
            )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the channel too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=(
                        f"```{await get_prefix(ctx)}automodblacklist" " <#channel>```"
                    ),
                )
            )

    @commands.command(name="allautomodwhitelists")
    async def all_auto_mod_whitelists(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})

        if guild_doc is not None:
            embed = disnake.Embed(
                title="All Auto-Moderation whitelists",
                description="Messages in these channel are immune from automod",
                color=var.C_MAIN,
            )

            desc = "".join(f"{i.mention} " for i in guild_doc["Settings"]["blacklists"])

            if desc != "":
                await ctx.send(embed=embed)
            else:
                await ctx.send("There are no blacklisted channels right now")

        else:
            await ctx.send("This server does not have automod setup right now")

    @commands.command(name="ignorebots")
    @has_command_permission()
    async def ignore_bots(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
        ignored = guild_doc["Settings"]["ignorebots"]
        embed = disnake.Embed(title="Ignore auto-moderation on bots")

        if ignored:
            embed.description = (
                f"{var.E_ENABLE} Bots are currently ignored "
                "hence immune from Auto-Moderation"
            )

            embed.color = var.C_GREEN
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction(var.E_DISABLE)

            def disable_check(reaction, user):
                if str(reaction.emoji) == var.E_DISABLE:
                    return user == ctx.author and reaction.message == bot_msg

            await self.bot.wait_for("reaction_add", check=disable_check)
            await db.AUTO_MOD.update_one(
                guild_doc, {"$set": {"Settings.ignorebots": False}}
            )

            embed.description = (
                f"{var.E_DISABLE} Bots are now not ignored"
                " hence affected by Auto-Moderation"
            )

            embed.color = var.C_RED
            await bot_msg.edit(embed=embed)

            try:
                await bot_msg.clear_reactions()

            except disnake.Forbidden:
                pass

        else:
            embed.description = (
                f"{var.E_DISABLE} Bots are currently not ignored"
                " hence affected by Auto-Moderation"
            )

            embed.color = var.C_RED
            bot_msg = await ctx.send(embed=embed)

            await bot_msg.add_reaction(var.E_ENABLE)

            def enable_check(reaction, user):
                if str(reaction.emoji) == var.E_ENABLE:
                    return user == ctx.author and reaction.message == bot_msg

            await self.bot.wait_for("reaction_add", check=enable_check)
            await db.AUTO_MOD.update_one(
                guild_doc, {"$set": {"Settings.ignorebots": True}}
            )

            embed.description = (
                f"{var.E_ENABLE} Bots are now ignored hence "
                "immune from Auto-Moderation"
            )

            embed.color = var.C_GREEN
            await bot_msg.edit(embed=embed)

            try:
                await bot_msg.clear_reactions()

            except disnake.Forbidden:
                pass

    @commands.command(name="mentionamount")
    @has_command_permission()
    async def mention_amount(self, ctx, amount: int = None):
        if amount is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            await db.AUTO_MOD.update_one(
                guild_doc, {"$set": {"Mentions.amount": amount}}
            )

            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "Successfully changed the amount of "
                        f"mentions to be deleted to **{amount}**"
                    ),
                    color=var.C_GREEN,
                )
            )
        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the amount too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}mentionamount <amount>```",
                )
            )

    @commands.command(name="addbadword")
    @has_command_permission()
    async def add_bad_word(self, ctx, word: str = None):
        if word is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            current_list = guild_doc["BadWords"]["words"]
            new_list = current_list.copy()

            if word not in new_list:
                new_list.append(word)
                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"BadWords.words": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            f"Successfully added the word **{word}**"
                            " in badwords list"
                        ),
                        color=var.C_GREEN,
                    )
                )

            else:
                await ctx.send(
                    embed=disnake.Embed(
                        description=("This word already exists in the bad word list"),
                        color=var.C_RED,
                    )
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the word too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}addbadword <word>```",
                )
            )

    @commands.command(name="removebadword")
    @has_command_permission()
    async def remove_bad_word(self, ctx, word: str = None):
        if word is not None:
            guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})
            current_list = guild_doc["BadWords"]["words"]
            new_list = current_list.copy()

            try:
                new_list.remove(word)
                await db.AUTO_MOD.update_one(
                    guild_doc, {"$set": {"BadWords.words": new_list}}
                )

                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            f"Successfully added the word **{word}**"
                            " in badwords list"
                        ),
                        color=var.C_GREEN,
                    )
                )

            except ValueError:
                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            f"The word **{word}** does not exist in the bad "
                            f"word list hence can't remove it either"
                        ),
                        color=var.C_RED,
                    )
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    title="Not enough arguments",
                    description="You need to define the word too!",
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}removebadword <word>```",
                )
            )

    @commands.command(name="allbadwords")
    @has_command_permission()
    async def all_bad_words(self, ctx):
        guild_doc = await db.AUTO_MOD.find_one({"_id": ctx.guild.id})

        if guild_doc is not None:
            embed = disnake.Embed(
                title="Bad Words",
                description=("All other forms of each bad words are also deleted"),
                color=var.C_TEAL,
            )

            all_banned_words = "".join(
                f"`{i}` " for i in guild_doc["BadWords"]["words"]
            )

            if all_banned_words == "":
                await ctx.send("This server does not have any bad word right now.")

            else:
                embed.add_field(name="All bad words", value=all_banned_words)
                await ctx.send(embed=embed)

        else:
            await ctx.send("This server does not have automod setted up")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        plugin_doc = await db.PLUGINS.find_one({"_id": message.guild.id})

        if plugin_doc["AutoMod"]:
            guild_doc = await db.AUTO_MOD.find_one({"_id": message.guild.id})
            if (
                guild_doc is not None
                and message.author != self.bot.user
                and message.channel.id not in guild_doc["Settings"]["blacklists"]
                and all(
                    item not in guild_doc["Settings"]["modroles"]
                    for item in [i.id for i in message.author.roles]
                )
                and (not message.author.bot or guild_doc["Settings"]["ignorebots"])
            ):

                if guild_doc["Links"]["status"]:
                    regex = re.compile(
                        r"(?:http|ftp)s?://"  # http:// or https://
                        # domain...
                        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
                        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
                        r"(?::\d+)?",  # optional port
                        # r"([a-zA-Z0-9\-]+)",
                        flags=re.IGNORECASE,
                    )

                    if regex.findall(message.content):
                        await message.delete()
                        res = guild_doc["Links"]["response"]
                        await message.channel.send(
                            f"{message.author.mention} {res}", delete_after=2
                        )

                if guild_doc["Invites"]["status"]:
                    regex = re.compile(
                        r"(?:disnake(?:[\.,]|dot)gg|"  # Could be disnake.gg/
                        # or disnake.com/invite/
                        r"disnake(?:[\.,]|dot)com(?:\/|slash)invite|"
                        # or disnakeapp.com/invite/
                        r"disnakeapp(?:[\.,]|dot)com(?:\/|slash)invite|"
                        r"disnake(?:[\.,]|dot)me|"  # or disnake.me
                        r"disnake(?:[\.,]|dot)li|"  # or disnake.li
                        r"disnake(?:[\.,]|dot)io"  # or disnake.io.
                        r")(?:[\/]|slash)"  # / or 'slash'
                        r"([a-zA-Z0-9\-]+)",  # the invite code itself
                        flags=re.IGNORECASE,
                    )

                    if regex.findall(message.content):
                        await message.delete()
                        res = guild_doc["Invites"]["response"]
                        await message.channel.send(
                            f"{message.author.mention} {res}", delete_after=2
                        )

                if guild_doc["Mentions"]["status"]:
                    amount = guild_doc["Mentions"]["amount"]
                    if len(message.mentions) >= amount:
                        await message.delete()
                        res = guild_doc["Mentions"]["response"]
                        await message.channel.send(
                            f"{message.author.mention} {res}", delete_after=2
                        )

                if guild_doc["BadWords"]["status"]:
                    bad_words = guild_doc["BadWords"]["words"]
                    if len([i for i in bad_words if i in message.content]) > 0:
                        await message.delete()
                        res = guild_doc["BadWords"]["response"]
                        await message.channel.send(
                            f"{message.author.mention} {res}", delete_after=2
                        )


def setup(bot):
    bot.add_cog(AutoMod(bot))
