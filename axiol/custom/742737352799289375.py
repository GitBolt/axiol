import discord
from discord.ext import commands
from discord.ext.commands import check, Context
import database as db
import variables as var
from functions import get_prefix


def is_user(*user_ids):
    async def predicate(ctx: Context):
        return ctx.author.id in user_ids

    return check(predicate)


# Custom cog for Chemistry Help discord server | 742737352799289375
class ChemistryHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        """Simple check this custom cog only runs on this server."""
        return ctx.guild.id == 742737352799289375 or 807140294276415510

    @commands.command(name="chem_addmsg")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_add_msg(self, ctx, *, msg: str = None):
        if msg is not None:

            guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]

            data = guild_col.find_one({"_id": 0})
            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()
                await guild_col.insert_one({
                    "_id": 0,
                    trigger: response
                })
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Added the message **{msg}**"
                            f" with response **{response}**"
                        ),
                        color=var.C_BLUE)
                )

            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ')

                await guild_col.update(data, {"$set": {trigger: response}})
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Added the message **{trigger}**"
                            f" with response **{response}**"
                        ),
                        color=var.C_BLUE)
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define both "
                        "the message and it's response"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}addmsg <msg> | <response>`"
                )
            )

    @commands.command(name="chem_removemsg")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_remove_msg(self, ctx, *, msg: str = None):
        if msg is None:
            return

        guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]
        data = guild_col.find_one({"_id": 0})

        if data is None:
            await ctx.send("You haven't setted up any message yet...")

        elif msg.lower() in data.keys():
            res = data.get(msg.lower())
            await guild_col.update_one(
                data, {"$unset": {msg.lower(): ""}}
            )

            await ctx.send(
                f"Successfully removed the message **msg**"
                f" which was having the response **{res}**"
            )

        else:
            await ctx.send("This message has no responses setted up")

    @commands.command(name="chem_allmsgs")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_all_msgs(self, ctx):
        guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]
        data = guild_col.find_one({"_id": 0})
        if data is not None:
            rr_amount = len(data)

            if rr_amount <= 10:
                exact_pages = 1
            else:
                exact_pages = rr_amount / 10

            if type(exact_pages) != int:
                all_pages = round(exact_pages) + 1
            else:
                all_pages = exact_pages

            embed = discord.Embed(
                title="All message responses",
                color=var.C_MAIN
            )

            async def pagination(current_page, all_pages, embed):
                page_rn = current_page + 1
                embed.set_footer(text=f"Page {page_rn}/{all_pages}")
                embed.clear_fields()

                rr_count = current_page * 10
                rr_amount = current_page * 10

                for i in list(data.items())[rr_amount:]:
                    rr_count += 1
                    embed.add_field(name=i[0], value=i[1], inline=False)

                    if rr_count == current_page * 10 + 10:
                        break

            rr_count = 0

            for i in data:
                rr_count += 1
                embed.add_field(name=i, value=data.get(i), inline=False)
                if rr_count == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction("◀️")
            await bot_msg.add_reaction("⬅️")
            await bot_msg.add_reaction("➡️")
            await bot_msg.add_reaction("▶️")

            def reaction_check(r, u):
                if (
                    str(r.emoji) == "◀️"
                    or str(r.emoji) == "⬅️"
                    or str(r.emoji) == "➡️"
                        or str(r.emoji) == "▶️"
                ):
                    return u == ctx.author and reaction.message == bot_msg

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
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await bot_msg.remove_reaction("➡️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await bot_msg.remove_reaction("⬅️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page -= 1
                    if current_page < 0:
                        current_page += 1

                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await bot_msg.remove_reaction("▶️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page = all_pages - 1
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

        else:
            await ctx.send("There are no message reactions yet")

    @commands.command(name="chem_addreact")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_add_react(self, ctx, *, msg: str = None):
        if msg is not None:
            guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]

            data = guild_col.find_one({"_id": 1})

            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(
                        embed=discord.Embed(
                            description=(
                                f"Added the message **{msg}**"
                                f" with reaction **{emoji}**"
                            ),
                            color=var.C_BLUE)
                    )

                except Exception:
                    await ctx.send(
                        "Sorry but it seems like either the emoji is invalid"
                        " or it's a custom emoji from a server where I am not"
                        " in hence can't use this emoji either :("
                    )

                await guild_col.insert_one({"_id": 1, trigger: emoji})

            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(
                        embed=discord.Embed(
                            description=(
                                f"Added the message **{msg}**"
                                f" with reaction **{emoji}**"
                            ),
                            color=var.C_BLUE)
                    )

                except Exception:
                    await ctx.send(
                        "Sorry but it seems like either the emoji is invalid "
                        "or it's a custom emoji from a server where I am not "
                        "in hence can't use this emoji either :("
                    )

                await guild_col.update(data, {"$set": {trigger: emoji}})

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define both "
                        "the message and it's reaction"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}addreaction <msg> <emoji>`"
                )
            )

    @commands.command(name="chem_removereact")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_remove_react(self, ctx, *, msg: str = None):
        if msg is not None:
            guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]
            data = await guild_col.find_one({"_id": 1})

            if data is not None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')

                if trigger in data.keys():
                    await guild_col.update(
                        data, {"$unset": {trigger.lower(): emoji}}
                    )

                    await ctx.send(
                        f"Successfully removed {emoji}"
                        f" reaction from **{trigger}** message"
                    )

                else:
                    await ctx.send(
                        "This message and emoji combination does not exist"
                    )

            else:
                await ctx.send("You haven't setted up any reaction yet...")

    @commands.command(name="chem_allreacts")
    @is_user(565059698399641600, 791950104680071188)
    async def chem_all_reacts(self, ctx):
        guild_col = await db.CUSTOM_DATABASE[str(ctx.guild.id)]
        data = await guild_col.find_one({"_id": 1})

        if data is not None:
            rr_amount = len(data)
            if rr_amount <= 10:
                exact_pages = 1
            else:
                exact_pages = rr_amount / 10

            if type(exact_pages) != int:
                all_pages = round(exact_pages) + 1

            else:
                all_pages = exact_pages

            embed = discord.Embed(
                title="All message reactions",
                color=var.C_MAIN
            )

            async def pagination(current_page, all_pages, embed):
                page_rn = current_page + 1
                embed.set_footer(text=f"Page {page_rn}/{all_pages}")
                embed.clear_fields()

                rr_count = current_page * 10
                rr_amount = current_page * 10

                for i in list(data.items())[rr_amount:]:
                    rr_count += 1
                    embed.add_field(name=i[0], value=i[1], inline=False)

                    if rr_count == (current_page) * 10 + 10:
                        break

            rr_count = 0
            for i in data:
                rr_count += 1
                embed.add_field(name=i, value=data.get(i), inline=False)

                if rr_count == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")
            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction("◀️")
            await bot_msg.add_reaction("⬅️")
            await bot_msg.add_reaction("➡️")
            await bot_msg.add_reaction("▶️")

            def reaction_check(r, u):
                if (
                    str(r.emoji) == "◀️"
                    or str(r.emoji) == "⬅️"
                    or str(r.emoji) == "➡️"
                    or str(r.emoji) == "▶️"
                ):
                    return u == ctx.author and reaction.message == bot_msg

            current_page = 0
            while True:
                reaction, _ = await self.bot.wait_for(
                    "reaction_add", check=reaction_check
                )

                if str(reaction.emoji) == "◀️":
                    try:
                        await bot_msg.remove_reaction("◀️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page = 0
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await bot_msg.remove_reaction("➡️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await bot_msg.remove_reaction("⬅️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page -= 1
                    if current_page < 0:
                        current_page += 1

                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await bot_msg.remove_reaction("▶️", ctx.author)

                    except discord.Forbidden:
                        pass

                    current_page = all_pages - 1
                    await pagination(current_page, all_pages, embed)
                    await bot_msg.edit(embed=embed)

        else:
            await ctx.send("There are no message reactions yet")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        if message.channel.id in [
            742848285416357970, 742849666256732170,
            844657766794788884, 846840113543905383
        ] and not message.author.bot:

            guild_col = db.CUSTOM_DATABASE[str(message.guild.id)]
            msg_data = await guild_col.find_one({"_id": 0})
            reaction_data = await guild_col.find_one({"_id": 1})

            if (
                    msg_data is not None
                    and message.content.lower() in msg_data.keys()
            ):
                await message.channel.send(
                    msg_data.get(message.content.lower())
                )

            if (
                reaction_data is not None
                and message.content.lower() in reaction_data.keys()
            ):
                await message.add_reaction(
                    reaction_data.get(message.content.lower()))


def setup(bot):
    bot.add_cog(ChemistryHelp(bot))
