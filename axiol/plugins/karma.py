import nltk
import disnake
from disnake.ext import commands
from nltk.sentiment import SentimentIntensityAnalyzer
import database as db
import constants as var
from functions import get_prefix
from ext.permissions import has_command_permission


nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


class Karma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Karma"):
            return True
        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Karma plugin is"
                        " disabled in this server"
                    ),
                    color=var.C_ORANGE
                )
            )

    @commands.command()
    @has_command_permission()
    async def karma(self, ctx, karma_user: disnake.User = None):
        user = ctx.author if karma_user is None else karma_user
        guild_col = db.KARMA_DATABASE[str(ctx.guild.id)]
        userdata = await guild_col.find_one({"_id": user.id})

        karmas = [
            x async for x in guild_col.find(
                {
                    "_id": {"$ne": 0},
                    # Removing ID 0 (Config doc, unrelated to user xp)
                }
            ).sort("karma", -1)
        ]

        if userdata is None:
            await ctx.send("This user does not have any karma yet...")
        else:
            # Index starts with zero
            position = karmas.index(userdata) + 1
            embed = disnake.Embed(
                title=f"Karma for {user.name}",
                color=var.C_MAIN
            ).add_field(
                name="Karma", value=userdata["karma"]
            ).add_field(
                name="Position", value=f"{position}/{len(karmas)}", inline=False
            ).set_thumbnail(url=user.avatar.url)

            total_karma = sum(i["karma"] for i in karmas)
            average = total_karma/len(karmas)

            if userdata["karma"] > average:
                embed.description = (
                    f"Your karma is better than the average {user.name}! :)"
                )

            if userdata["karma"] < average:
                embed.description = (
                    f"Your karma is lower than the average {user.name}, "
                    f"is it because you don't talk much or you are not nice "
                    f"enough? :eyes:"
                )

            if position == 1:
                embed.description = (
                    f"Woohoo {user.name}, you are the nicest "
                    f"person in the server!"
                )

            await ctx.channel.send(embed=embed)

    @commands.command(name="karmaboard", aliases=["kb"])
    @has_command_permission()
    async def karma_board(self, ctx):
        guild_col = db.KARMA_DATABASE[str(ctx.guild.id)]

        karmas = [
            # Removing ID 0 (Config doc, unrelated to user xp)
            x async for x in
            guild_col.find({"_id": {"$ne": 0}}).sort("karma", -1)
        ]

        if len(karmas) < 10:
            exact_pages = 1
        else:
            exact_pages = len(karmas) / 10

        if type(exact_pages) != int:
            all_pages = round(exact_pages) + 1

        else:
            all_pages = exact_pages

        total_karma = 0
        for i in karmas:
            total_karma += i["karma"]

        average = total_karma/len(karmas)

        embed = disnake.Embed(
            title=f"Karma Board",
            description=f"The average karma in this server is **{average}**",
            color=var.C_BLUE
        ).set_thumbnail(url=ctx.guild.icon.url)

        count = 0
        for i in karmas:
            count += 1
            try:
                user = self.bot.get_user(i.get("_id"))
                karma = i.get("karma")
                embed.add_field(
                    name=f"{count}: {user}",
                    value=f"Total Karma: {karma}",
                    inline=False
                )

            except Exception:
                print(f"Not found {i}")

            if count == 10:
                break

        embed.set_footer(text=f"Page 1/{all_pages}")
        bot_msg = await ctx.send(embed=embed)
        await bot_msg.add_reaction("◀️")
        await bot_msg.add_reaction("⬅️")
        await bot_msg.add_reaction("➡️")
        await bot_msg.add_reaction("▶️")

        def reaction_check(r, u):
            return u == ctx.author and r.message == bot_msg

        async def pagination(ctx, current_page, embed, GuildCol, all_pages):
            page_rn = current_page + 1
            embed.set_footer(text=f"Page {page_rn}/{all_pages}")
            embed.clear_fields()

            rank_count = current_page * 10
            user_amount = current_page*10

            karmas = [
                x async for x in GuildCol.find(
                    # Removing ID 0 (Config doc, unrelated to user xp)
                    {"_id": {"$ne": 0}}
                ).sort("karma", -1).limit(user_amount)
            ]

            for i in karmas:
                rank_count += 1
                user = self.bot.get_user(i.get("_id"))
                karma = i.get("karma")

                embed.add_field(
                    name=f"{rank_count}: {user}",
                    value=f"Total Karma: {karma}",
                    inline=False
                )

                if rank_count == current_page * 10 + 10:
                    break

        current_page = 0
        while True:
            reaction, user = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            if str(reaction.emoji) == "◀️":
                try:
                    await bot_msg.remove_reaction("◀️", ctx.author)

                except disnake.Forbidden:
                    pass

                current_page = 0
                await pagination(ctx, current_page, embed, guild_col, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "➡️":
                try:
                    await bot_msg.remove_reaction("➡️", ctx.author)

                except disnake.Forbidden:
                    pass

                current_page += 1
                if current_page > all_pages:
                    current_page -= 1

                await pagination(ctx, current_page, embed, guild_col, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "⬅️":
                try:
                    await bot_msg.remove_reaction("⬅️", ctx.author)

                except disnake.Forbidden:
                    pass

                current_page -= 1
                if current_page < 0:
                    current_page += 1

                await pagination(ctx, current_page, embed, guild_col, all_pages)
                await bot_msg.edit(embed=embed)

            if str(reaction.emoji) == "▶️":
                try:
                    await bot_msg.remove_reaction("▶️", ctx.author)

                except disnake.Forbidden:
                    pass

                current_page = all_pages-1
                await pagination(ctx, current_page, embed, guild_col, all_pages)
                await bot_msg.edit(embed=embed)

    @commands.command(name="kblacklist")
    @has_command_permission()
    async def k_blacklist(self, ctx, channel: disnake.TextChannel = None):
        if channel is not None:
            guild_col = db.KARMA_DATABASE[(str(ctx.guild.id))]
            settings = await guild_col.find_one({"_id": 0})

            new_settings = settings.get("blacklists").copy()
            if channel.id in new_settings:
                await ctx.send("This channel is already blacklisted")

            else:
                new_settings.append(channel.id)
                new_data = {
                    "$set": {
                        "blacklists": new_settings
                    }
                }

                await guild_col.update_one(settings, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            f"{channel.mention} has been blacklisted, "
                            f"hence users won't gain any karma in that channel."
                        ),
                        color=var.C_GREEN
                    )
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the channel to blacklist it!"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}kblacklist <#channel>```"
                )
            )

    @commands.command(name="kwhitelist")
    @has_command_permission()
    async def k_whitelist(self, ctx, channel: disnake.TextChannel = None):
        if channel is not None:
            guild_col = db.KARMA_DATABASE[(str(ctx.guild.id))]
            settings = await guild_col.find_one({"_id": 0})

            new_settings = settings.get("blacklists").copy()

            if channel.id not in new_settings:
                await ctx.send("This channel is not blacklisted")

            else:
                new_settings.remove(channel.id)
                new_data = {
                    "$set": {
                        "blacklists": new_settings
                    }
                }

                await guild_col.update_one(settings, new_data)

                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            f"{channel.mention} has been whitelisted, hence "
                            "users would be able to gain karma again in that "
                            "channel."
                        ),
                        color=var.C_GREEN
                    )
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the channel to whitelist it!"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}kwhitelist <#channel>```"
                )
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        plugin_doc = await db.PLUGINS.find_one({"_id": message.guild.id})
        guild_col = db.KARMA_DATABASE[str(message.guild.id)]
        settings_doc = await guild_col.find_one({"_id": 0})

        if plugin_doc["Karma"] and not message.author.bot:
            if not message.channel.id in settings_doc["blacklists"]:
                userdata = await guild_col.find_one({"_id": message.author.id})
                polarity = sia.polarity_scores(message.content)
                result = max(polarity, key=polarity.get)

                def get_karma():
                    if result == "neg":
                        return -polarity[result]

                    elif result == "pos":
                        return polarity[result]

                    return 0

                if userdata is None:
                    await guild_col.insert_one(
                        {"_id": message.author.id, "karma": get_karma()}
                    )

                else:
                    new_karma = get_karma()
                    new_karma += userdata["karma"]
                    await guild_col.update_one(
                        userdata, {"$set": {"karma": new_karma}}
                    )


def setup(bot):
    bot.add_cog(Karma(bot))
