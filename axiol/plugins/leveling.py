import random
import discord
from discord.ext import commands
import axiol.variables as var
import axiol.database as db
from axiol.functions import get_prefix, get_xprange
from axiol.ext.permissions import has_command_permission


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Leveling"):
            return True

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"{var.E_DISABLE} The Leveling plugin "
                        f"is disabled in this server"
                    ),
                    color=var.C_ORANGE
                )
            )

    @commands.command()
    @has_command_permission()
    async def rank(self, ctx, rank_user: discord.User = None):
        if rank_user is None:
            user = ctx.author
        else:
            user = rank_user

        guild_col = db.LEVEL_DATABASE[str(ctx.guild.id)]
        userdata = await guild_col.find_one({"_id": user.id})

        if userdata is None:
            await ctx.send("This user does not have any rank yet...")

        else:
            xp = userdata["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))

            try:
                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)

            except Exception:
                boxes = 0

            ranking = guild_col.find().sort("xp", -1)

            async for x in ranking:
                rank += 1
                if userdata["_id"] == x["_id"]:
                    break

            embed = discord.Embed(
                title=f"Level stats for {user.name}",
                color=var.C_TEAL
            ).add_field(
                name="Rank",
                value=f"{rank}/{await guild_col.estimated_document_count() - 1}",
                inline=True
            ).add_field(
                name="XP",
                value=f"{xp}/{int(200 * ((1 / 2) * lvl))}",
                inline=True
            ).add_field(
                name="Level", value=lvl, inline=True
            ).add_field(
                name="Progress",
                value=(
                    boxes * "<:current:850041599139905586>"
                    + (20 - boxes) * "<:left:850041599127584776>"
                ),
                inline=False
            ).set_thumbnail(url=user.avatar_url)

            await ctx.send(embed=embed)

    @commands.command(aliases=["lb"])
    @has_command_permission()
    async def leaderboard(self, ctx):
        guild_col = db.LEVEL_DATABASE[str(ctx.guild.id)]

        rankings = [
            x async for x in guild_col.find(
                # Removing ID 0 (Config doc, unrelated to user xp)
                {"_id": {"$ne": 0}}
            ).sort("xp", -1)
        ]

        if len(rankings) < 10:
            exact_pages = 1

        else:
            exact_pages = len(rankings) / 10

        if type(exact_pages) != int:
            all_pages = round(exact_pages) + 1

        else:
            all_pages = exact_pages

        embed = discord.Embed(
            title=f"Leaderboard",
            description=(
                "◀️ First page\n"
                "⬅️ Previous page\n"
                "<:RankChart:854068306285428767> Bar graph of top 10 users\n"
                "➡️ Next page\n"
                "▶️ Last page\n"
            ),
            color=var.C_BLUE
        ).set_thumbnail(url=ctx.guild.icon_url)

        rank_count = 0
        for i in rankings:
            rank_count += 1
            try:
                user = self.bot.get_user(i.get("_id"))
                xp = i.get("xp")
                embed.add_field(
                    name=f"{rank_count}: {user}",
                    value=f"Total XP: {xp}",
                    inline=False
                )

            except Exception:
                print(f"Not found {i}")

            if rank_count == 10:
                break

        embed.set_footer(text=f"Page 1/{all_pages}")
        bot_msg = await ctx.send(embed=embed)
        await bot_msg.add_reaction("◀️")
        await bot_msg.add_reaction("⬅️")
        await bot_msg.add_reaction("<:RankChart:854068306285428767>")
        await bot_msg.add_reaction("➡️")
        await bot_msg.add_reaction("▶️")

        async def leaderboard_pagination(current_page, embed, all_pages):
            page_rn = current_page + 1
            embed.set_footer(text=f"Page {page_rn}/{all_pages}")
            embed.clear_fields()

            rank_count = (current_page) * 10
            user_amount = current_page * 10
            rankings = guild_col.find(
                # Removing ID 0 (Config doc, unrelated to user xp)
                {"_id": {"$ne": 0}}
            ).sort("xp", -1).limit(user_amount)

            async for i in rankings:
                rank_count += 1
                user = self.bot.get_user(i.get("_id"))
                xp = i.get("xp")

                embed.add_field(
                    name=f"{rank_count}: {user}",
                    value=f"Total XP: {xp}",
                    inline=False
                )

                if rank_count == current_page * 10 + 10:
                    break

        def reaction_check(r, u):
            return u == ctx.author and r.message == bot_msg

        current_page = 0
        while True:
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            if str(reaction.emoji) == "◀️":
                try:
                    await bot_msg.remove_reaction("◀️", ctx.author)

                except discord.Forbidden:
                    pass

                current_page = 0
                await leaderboard_pagination(current_page, embed, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "➡️":
                try:
                    await bot_msg.remove_reaction("➡️", ctx.author)

                except discord.Forbidden:
                    pass

                current_page += 1
                if current_page > all_pages:
                    current_page -= 1

                await leaderboard_pagination(current_page, embed, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "<:RankChart:854068306285428767>":
                try:
                    await bot_msg.clear_reactions()

                except discord.Forbidden:
                    pass

                await ctx.invoke(self.bot.get_command('barchart'))

            if str(reaction.emoji) == "⬅️":
                try:
                    await bot_msg.remove_reaction("⬅️", ctx.author)

                except discord.Forbidden:
                    pass

                current_page -= 1
                if current_page < 0:
                    current_page += 1

                await leaderboard_pagination(current_page, embed, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "▶️":
                try:
                    await bot_msg.remove_reaction("▶️", ctx.author)

                except discord.Forbidden:
                    pass

                current_page = all_pages - 1
                await leaderboard_pagination(current_page, embed, all_pages)
                await bot_msg.edit(embed=embed)

    @commands.command()
    @has_command_permission()
    async def level_info(self, ctx):
        guild_col = db.LEVEL_DATABASE[str(ctx.guild.id)]
        settings_doc = await guild_col.find_one({"_id": 0})
        xp_range = " - ".join(str(i) for i in settings_doc["xprange"])

        bl = [
            self.bot.get_channel(i)
            for i in settings_doc["blacklistedchannels"]
            if self.bot.get_channel(i) != None
        ]

        blacklisted_channels = ', '.join(bl) if not bl == [] else None

        max_rank = [
            x async for x in guild_col.find(
                # Removing ID 0 (Config doc, unrelated to user xp)
                {"_id": {"$ne": 0}}
            ).sort("xp", -1).limit(1)
        ]

        max_rank_user = await self.bot.fetch_user(max_rank[0]["_id"])

        def get_alert_channel():
            if settings_doc.get("alertchannel") is not None:
                alert_channel = self.bot.get_channel(
                    settings_doc.get("alertchannel")
                )

                if alert_channel is not None:
                    return alert_channel.mention

                else:
                    return "deleted channel"

            else:
                return None

        status = "Enabled" if settings_doc["alerts"] else "Disabled"
        rewards = settings_doc["rewards"]

        embed = discord.Embed(
            title="Server leveling information",
            color=var.C_BLUE
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).add_field(
            name="Highest XP Member",
            value=max_rank_user,
            inline=False
        ).add_field(
            name="Leveling XP Range",
            value=xp_range,
            inline=False
        ).add_field(
            name="Blacklisted channels",
            value=blacklisted_channels,
            inline=False
        ).add_field(
            name="Alert Status",
            value=status,
            inline=False
        ).add_field(
            name="Alert channel",
            value=get_alert_channel(),
            inline=False
        ).add_field(
            name="Level rewards",
            value=(
                f"React to {var.E_CONTINUE}"
                if settings_doc["rewards"] else
                "There are no level rewards right now"
            ),
            inline=False
        )

        bot_msg = await ctx.send(embed=embed)
        if settings_doc["rewards"]:
            await bot_msg.add_reaction(var.E_CONTINUE)

            def reaction_check(reaction, user):
                if str(reaction.emoji) == var.E_CONTINUE:
                    return (
                        user == ctx.author
                        and reaction.message == bot_msg
                    )

            await self.bot.wait_for("reaction_add", check=reaction_check)

            try:
                await bot_msg.clear_reactions()

            except Exception:
                pass

            rewards = settings_doc.get("rewards")
            embed.title = "Level rewards"
            embed.clear_fields()

            for i in rewards:
                role = ctx.guild.get_role(rewards.get(i))
                embed.add_field(
                    name=f"Level {i}",
                    value=role.mention if role is not None else "deleted role",
                    inline=False
                )

            await bot_msg.edit(embed=embed)

    @commands.command(name="givexp")
    @has_command_permission()
    async def give_xp(
        self, ctx, user: discord.Member = None, amount: int = None
    ):
        if user and amount is not None:
            if amount > 10000000:
                await ctx.send(
                    embed=discord.Embed(
                        description="🚫 Ayo that's too much",
                        color=var.C_RED
                    )
                )

            else:
                guild_col = db.LEVEL_DATABASE[str(ctx.guild.id)]
                data = await guild_col.find_one({"_id": user.id})

                if data is None:
                    await guild_col.insert_one({"_id": user.id, "xp": amount})
                    await ctx.send(
                        f"Successfully awarded {user} with {amount} xp!"
                    )

                elif data.get("xp") > 10000000:
                    await ctx.send(
                        embed=discord.Embed(
                            description=(
                                "🚫 Cannot give more xp to the user,"
                                " they are too rich already"
                            ),
                            color=var.C_RED
                        )
                    )

                else:
                    new_data = {
                        "$set": {
                            "xp": data.get("xp") + amount
                        }
                    }

                    await guild_col.update_one(data, new_data)

                    await ctx.send(
                        f"Successfully awarded {user} with {amount} xp!"
                    )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the member"
                        " and the amount to give them xp"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}givexp <user> <amount>```"
                ).set_footer(
                    text="For user either user mention or user ID can be used"
                )
            )

    @commands.command(name="removexp")
    @has_command_permission()
    async def remove_xp(
            self, ctx, user: discord.Member = None, amount: int = None
    ):
        if user and amount is not None:
            if amount > 10000000:
                await ctx.send(
                    embed=discord.Embed(
                        description="🚫 Ayo that's too much",
                        color=var.C_RED
                    )
                )

            else:
                guild_col = db.LEVEL_DATABASE[str(ctx.guild.id)]
                data = await guild_col.find_one({"_id": user.id})

                new_data = {
                    "$set": {
                        "xp": data.get("xp") - amount
                    }
                }

                await guild_col.update_one(data, new_data)
                await ctx.send(f"Successfully removed {amount} xp from {user}!")

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the member "
                        "and the amount to remove their xp"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}removexp <user> <amount>`"
                ).set_footer(
                    text="For user either user mention or user ID can be used"
                )
            )

    @commands.command()
    @has_command_permission()
    async def xp_range(self, ctx, min_val: int = None, max_val: int = None):
        if min_val and max_val is not None:
            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            new_data = {
                "$set": {
                    "xprange": [min_val, max_val]
                }
            }

            await guild_col.update_one(settings, new_data)

            await ctx.send(
                embed=discord.Embed(
                    description=f"New xp range is now {min_val} - {max_val}!",
                    color=var.C_GREEN
                )
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="🚫 You need to define the xp range",
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}xprange <min_xp> <max_xp>`"
                )
            )

    @commands.command()
    @has_command_permission()
    async def blacklist(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            new_settings = settings.get("blacklistedchannels").copy()
            new_settings.append(channel.id)

            new_data = {
                "$set": {
                    "blacklistedchannels": new_settings
                }
            }

            await guild_col.update_one(settings, new_data)

            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"{channel.mention} has been blacklisted,"
                        f" hence users won't gain any xp in that channel."
                    ),
                    color=var.C_GREEN
                )
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the channel to blacklist it"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}blacklist <#channel>`"
                )
            )

    @commands.command()
    @has_command_permission()
    async def whitelist(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            new_settings = settings.get("blacklistedchannels").copy()

            if channel.id in new_settings:
                new_settings.remove(channel.id)

                new_data = {
                    "$set": {
                        "blacklistedchannels": new_settings
                    }
                }

                await guild_col.update_one(settings, new_data)
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"{channel.mention} has been removed from blacklist"
                            f", hence users will be able to gain xp again in"
                            f" that channel."
                        ),
                        color=var.C_GREEN
                    )
                )
            else:
                await ctx.send(f"{channel.mention} was not blacklisted")

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the channel to whitelist it"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}whitelist <#channel>`"
                )
            )

    @commands.command(name="togglealerts", aliases=["removealerts"])
    @has_command_permission()
    async def toggle_alerts(self, ctx):
        guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
        guild_config = await guild_col.find_one({"_id": 0})

        if guild_config.get("alerts"):
            new_data = {
                "$set": {
                    "alerts": False
                }
            }

            await ctx.send(
                embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Successfully disabled alerts!",
                    color=var.C_GREEN
                )
            )

        else:
            new_data = {
                "$set": {
                    "alerts": True
                }
            }

            await ctx.send(
                embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Successfully enabled alerts!",
                    color=var.C_GREEN
                )
            )

        await guild_col.update_one(guild_config, new_data)

    @commands.command()
    @has_command_permission()
    async def alert_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            new_data = {
                "$set": {"alertchannel": channel.id}
            }

            await guild_col.update_one(settings, new_data)
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"{channel.mention} has been marked as the alert "
                        "channel, hence users who will level up will get "
                        "mentioned here!"
                    ),
                    color=var.C_GREEN
                )
            )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the channel "
                        "to make it the alert channel"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}alertchannel <#channel>`"
                )
            )

    @commands.command(aliases=["addreward"])
    @has_command_permission()
    async def reward(self, ctx, level: str = None, role: discord.Role = None):
        if level and role is not None and level.isnumeric():
            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            existing_data = settings.get("rewards")
            new_dict = existing_data.copy()

            new_dict.update({level: role.id})
            new_data = {
                "$set": {
                    "rewards": new_dict
                }
            }

            await guild_col.update_one(settings, new_data)
            await ctx.send(embed=discord.Embed(
                description=(
                    f"Successfully added {role.mention} "
                    f"as the reward to Level {level}!"
                ),
                color=var.C_GREEN)
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the level"
                        " and role both to add a reward!"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}reward <level> <role>`"
                ).set_footer(
                    text=(
                        f"Make sure that for level you only the enter level "
                        f"number, example: {await get_prefix(ctx)}reward 2 "
                        f"@somerole\nNot {await get_prefix(ctx)}reward level2 "
                        f"@somerole"
                    )
                )
            )

    @commands.command(name="removereward")
    @has_command_permission()
    async def remove_reward(self, ctx, level: str = None):
        if level is not None:

            guild_col = db.LEVEL_DATABASE.get_collection(str(ctx.guild.id))
            settings = await guild_col.find_one({"_id": 0})

            existing_data = settings.get("rewards")

            if not level in existing_data.keys():
                await ctx.send("This level does not have any rewards setted up")

            else:
                new_dict = existing_data.copy()
                role = ctx.guild.get_role(new_dict.get(level))
                new_dict.pop(level)

                new_data = {
                    "$set": {
                        "rewards": new_dict
                    }
                }
                await guild_col.update_one(settings, new_data)

                dp_role = role.mention if role is not None else 'deleted role'

                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Successfully removed **{dp_role}** "
                            f"as the reward from Level **{level}**!"
                        ),
                        color=var.C_GREEN
                    )
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the level to remove it's reward!"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}removereward <level>`"
                ).set_footer(
                    text=(
                        f"Make sure that for level you only the enter level"
                        f" number, example: {await get_prefix(ctx)}removereward"
                        f" 2 \nNot {await get_prefix(ctx)}removereward level2 "
                    )
                )
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        guild_level_col = db.LEVEL_DATABASE[str(message.guild.id)]
        guild_plugin_doc = await db.PLUGINS.find_one({"_id": message.guild.id})
        guild_settings_doc = await guild_level_col.find_one({"_id": 0})

        if (
            not guild_plugin_doc["Leveling"]
            or message.channel.id in guild_settings_doc["blacklistedchannels"]
            or message.author.bot
        ):
            return

        userdata = await guild_level_col.find_one({"_id": message.author.id})

        if userdata is None:
            await guild_level_col.insert_one(
                {"_id": message.author.id, "xp": 0}
            )

        else:
            xp = userdata["xp"]

            init_lvl = 0
            while True:
                if xp < ((50 * (init_lvl ** 2)) + (50 * init_lvl)):
                    break
                init_lvl += 1

            xp_range = await get_xprange(message.guild.id)
            xp = userdata["xp"] + random.randint(xp_range[0], xp_range[1])
            await guild_level_col.update_one(userdata, {"$set": {"xp": xp}})

            level_now = 0
            while True:
                if xp < ((50 * (level_now ** 2)) + (50 * level_now)):
                    break

                level_now += 1

            if level_now > init_lvl and guild_settings_doc["alerts"]:
                ch = self.bot.get_channel(guild_settings_doc["alertchannel"])

                embed = discord.Embed(
                    title="You leveled up!",
                    description=(
                        f"{var.E_ACCEPT} You are now level {level_now}!"
                    ),
                    color=var.C_MAIN
                )

                try:
                    if ch is not None:
                        await ch.send(
                            content=message.author.mention,
                            embed=embed
                        )

                    else:
                        await message.channel.send(
                            content=message.author.mention, embed=embed
                        )

                except discord.Forbidden:
                    pass

            rewards = guild_settings_doc["rewards"]
            if str(level_now) in rewards.keys():
                role_id = rewards.get(str(level_now))
                role = message.guild.get_role(role_id)

                if role is not None and role not in message.author.roles:
                    await message.author.add_roles(role)


def setup(bot):
    bot.add_cog(Leveling(bot))
