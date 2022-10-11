import disnake
from typing import Union
from disnake.ext import commands
import database as db
import constants as var
from functions import get_prefix
from ext.permissions import has_command_permission


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if guild_doc.get("ReactionRoles"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Reaction Roles plugin"
                        " is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @commands.command()
    @has_command_permission()
    async def rr(
        self,
        ctx,
        channel: disnake.TextChannel = None,
        message_id: Union[int, None] = None,
        role: disnake.Role = None,
        emoji: Union[disnake.Emoji, str] = None,
    ):
        if type(emoji) == str and emoji.startswith("<"):
            raise commands.EmojiNotFound(ctx)

        if {channel, message_id, role, emoji} == {None}:
            return await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the channel, message, "
                        "role and emoji all three to add a reaction role,"
                        " make sure the IDs are numerical."
                    ),
                    color=var.C_RED,
                )
                .add_field(
                    name="Format",
                    value=(
                        f"`{await get_prefix(ctx)}rr"
                        " <#channel> <messageid> <role> <emoji>`"
                    ),
                )
                .set_footer(
                    text=(
                        "You can use either role ID or mention it (use ID if "
                        "you don't want to disturb everyone having the role)"
                    )
                )
            )

        bot_member = ctx.guild.get_member(self.bot.user.id)
        try:
            bot_role = bot_member.roles[1]
        except IndexError:
            bot_role = bot_member.roles[0]

        try:
            msg = channel.get_partial_message(message_id)

        except Exception:
            raise commands.MessageNotFound(ctx)

        if bot_role.position >= role.position:
            guild_doc = await db.REACTION_ROLES.find_one({"_id": ctx.guild.id})

            if guild_doc is None:
                await db.REACTION_ROLES.insert_one(
                    {
                        "_id": ctx.guild.id,
                        "reaction_roles": [
                            {
                                "messageid": msg.id,
                                "roleid": role.id,
                                "emoji": str(emoji),
                            }
                        ],
                        "unique_messages": [],
                    }
                )

                await msg.add_reaction(emoji)
                await ctx.send(
                    f"Reaction role for {role} using {emoji} setted up!"
                    f" https://disnake.com/channels/{ctx.message.guild.id}"
                    f"/{msg.channel.id}/{msg.id}"
                )

            else:
                guildrr_list = guild_doc["reaction_roles"]

                def check():
                    for i in guildrr_list:
                        if i.get("messageid") == msg.id and i.get("emoji") == str(
                            emoji
                        ):
                            return True

                if check():
                    await ctx.send(
                        "You have already setup this reaction role"
                        f" using {emoji} on that message :D "
                        "I can see it in the database!"
                    )

                else:
                    new_list = guildrr_list.copy()
                    new_list.append(
                        {"messageid": msg.id, "roleid": role.id, "emoji": str(emoji)}
                    )

                    new_data = {"$set": {"reaction_roles": new_list}}

                    await db.REACTION_ROLES.update_one(guild_doc, new_data)
                    await msg.add_reaction(emoji)
                    await ctx.send(
                        f"Reaction role for {role} using {emoji} setted up!"
                        f" https://disnake.com/channels/{ctx.message.guild.id}"
                        f"/{msg.channel.id}/{msg.id}"
                    )
        else:

            await ctx.send(
                embed=disnake.Embed(
                    title="Role position error",
                    description=(
                        f"The role {role.mention} is above my role "
                        f"({bot_role.mention}), in order for me to update any "
                        f"role (reaction roles) my role needs to be above that "
                        f"role, just move my role above your reaction role as "
                        f"shown below\n\n **Server Settings > Roles > Click on"
                        f" the {bot_role.mention} Role > Drag it above the "
                        f"{role.mention} Role **(Shown as the Developer role in"
                        f" the image below)"
                    ),
                    color=var.C_RED,
                ).set_image(
                    url=(
                        "https://cdn.disnakeapp.com/attachments/"
                        "843519647055609856/850711272726986802/unknown.png"
                    )
                )
            )

    @commands.command(name="removerr")
    @has_command_permission()
    async def remove_rr(
        self,
        ctx,
        message_id: Union[int, str] = None,
        emoji: Union[disnake.Emoji, str] = None,
    ):

        if {message_id, emoji} == {None}:
            return await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the message "
                        "and emoji both to remove a reaction role"
                    ),
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=(
                        f"`{await get_prefix(ctx)}removerr " f"<messageid> <emoji>`"
                    ),
                )
            )

        if type(emoji) == str and emoji.startswith("<"):
            raise commands.EmojiNotFound(ctx)

        if type(message_id) == str:
            return await ctx.send(
                embed=disnake.Embed(
                    description="Message ID needs to be numerical", color=var.C_ORANGE
                )
            )

        guild_doc = await db.REACTION_ROLES.find_one({"_id": ctx.guild.id})

        def rr_exists():
            for i in guild_doc["reaction_roles"]:
                if i.get("messageid") == message_id and i.get("emoji") == str(emoji):
                    return True

        if rr_exists():

            def get_pair(lst):
                for rr_pairs in lst:
                    if message_id == rr_pairs.get("messageid") and str(
                        emoji
                    ) == rr_pairs.get("emoji"):
                        return rr_pairs

            rr_list = guild_doc["reaction_roles"]
            new_list = rr_list.copy()
            pair = get_pair(new_list)
            new_list.remove(pair)
            new_data = {"$set": {"reaction_roles": new_list}}

            role = ctx.guild.get_role(pair["roleid"])
            await db.REACTION_ROLES.update_one(guild_doc, new_data)

            await ctx.send(
                embed=disnake.Embed(
                    title="Reaction role removed",
                    description=(
                        f"Reaction role for {role} using {emoji} "
                        f"on message with ID {message_id} has been removed"
                    ),
                    color=var.C_GREEN,
                )
            )

        else:
            await ctx.send("This reaction role does not exist")

    @commands.command(name="allrr", aliases=["rrall"])
    @has_command_permission()
    async def all_rr(self, ctx):

        guild_doc = await db.REACTION_ROLES.find_one({"_id": ctx.guild.id})

        if guild_doc is not None and guild_doc["reaction_roles"] != []:
            rr_amount = len(guild_doc.get("reaction_roles"))

            if rr_amount <= 10:
                exact_pages = 1

            else:
                exact_pages = rr_amount / 10
            all_pages = round(exact_pages)

            embed = disnake.Embed(title="All active reaction roles", color=var.C_MAIN)

            rr_count = 0
            for i in guild_doc["reaction_roles"]:
                rr_count += 1
                message_id = i.get("messageid")
                role = ctx.guild.get_role(i.get("roleid"))
                emoji = i.get("emoji")

                embed.add_field(
                    name="** **",
                    value=(
                        f"{emoji} for {role.mention if role else 'deleted role'} "
                        f"in message ID `{message_id}`"
                    ),
                    inline=False,
                )

                if rr_count == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")

            bot_msg = await ctx.send(embed=embed)
            await bot_msg.add_reaction("◀️")
            await bot_msg.add_reaction("⬅️")
            await bot_msg.add_reaction("➡️")
            await bot_msg.add_reaction("▶️")

            async def reaction_roles_pagination(current_page, embed):
                page_rn = current_page + 1
                embed.set_footer(text=f"Page {page_rn}/{all_pages}")
                embed.clear_fields()

                rr_count = current_page * 10
                rr_amount = current_page * 10

                for i in guild_doc["reaction_roles"][rr_amount:]:
                    rr_count += 1
                    message_id = i.get("messageid")
                    role = ctx.guild.get_role(i.get("roleid"))
                    emoji = i.get("emoji")

                    embed.add_field(
                        name=f"** **",
                        value=(
                            f"{emoji} for {role.mention if role else 'deleted role'}\n"
                            f"MessageID: `{message_id}`"
                        ),
                        inline=False,
                    )

                    if rr_count == (current_page) * 10 + 10:
                        break

            def reaction_check(r, u):
                if (
                    str(r.emoji) == "◀️"
                    or str(r.emoji) == "⬅️"
                    or str(r.emoji) == "➡️"
                    or str(r.emoji) == "▶️"
                ):
                    return u == ctx.author and r.message == bot_msg

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
                    await reaction_roles_pagination(current_page, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await bot_msg.remove_reaction("➡️", ctx.author)
                    except disnake.Forbidden:
                        pass
                    current_page += 1
                    await reaction_roles_pagination(current_page, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await bot_msg.remove_reaction("⬅️", ctx.author)
                    except disnake.Forbidden:
                        pass
                    current_page -= 1
                    if current_page < 0:
                        current_page += 1
                    await reaction_roles_pagination(current_page, embed)
                    await bot_msg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await bot_msg.remove_reaction("▶️", ctx.author)
                    except disnake.Forbidden:
                        pass
                    current_page = all_pages - 1
                    await reaction_roles_pagination(current_page, embed)
                    await bot_msg.edit(embed=embed)

        else:
            await ctx.send(
                "This server does not have any active reaction roles right now"
            )

    @commands.command(name="uniquerr")
    @has_command_permission()
    async def unique_rr(self, ctx, msg: disnake.Message = None):

        if msg is not None:
            guild_doc = await db.REACTION_ROLES.find_one({"_id": ctx.guild.id})
            if guild_doc is not None:
                unique_list = guild_doc["unique_messages"]

                all_msg_ids = [i.get("messageid") for i in guild_doc["reaction_roles"]]
                if msg.id in all_msg_ids:
                    new_list = unique_list.copy()

                    new_list.append(msg.id)
                    new_data = {"$set": {"unique_messages": new_list}}

                    await db.REACTION_ROLES.update_one(guild_doc, new_data)
                    await ctx.send(
                        embed=disnake.Embed(
                            title=(
                                "Successfully marked the message "
                                "with unique reactions"
                            ),
                            description=(
                                "Now users can only react to one emoji and "
                                "take one role in [this message]"
                                f"(https://disnake.com/channels/{ctx.guild.id}"
                                f"/{msg.channel.id}/{msg.id})"
                            ),
                            color=var.C_GREEN,
                        )
                    )

                else:
                    await ctx.send(
                        "Hmm it looks like that the message id "
                        "you entered does not have any reaction role."
                    )

            else:
                await ctx.send(
                    "Cannot mark that message with unique reactions "
                    "since this server does not have any reaction roles yet :("
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the message "
                        "in order to mark it with unique reactions"
                    ),
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}uniquerr <messageid>`",
                )
            )

    @commands.command(name="removeunique")
    @has_command_permission()
    async def remove_unique(self, ctx, msg: disnake.Message = None):

        if msg is not None:
            guild_doc = await db.REACTION_ROLES.find_one({"_id": ctx.guild.id})
            if guild_doc is not None:
                unique_list = guild_doc["unique_messages"]

                all_msg_ids = [i.get("messageid") for i in guild_doc["reaction_roles"]]
                if msg.id in all_msg_ids and msg.id in unique_list:
                    new_list = unique_list.copy()

                    new_list.remove(msg.id)
                    new_data = {"$set": {"unique_messages": new_list}}

                    await db.REACTION_ROLES.update_one(guild_doc, new_data)

                    await ctx.send(
                        embed=disnake.Embed(
                            title=(
                                "Successfully unmarked the "
                                "message with unique reactions"
                            ),
                            description=(
                                "Now users can react and take multiple roles "
                                "in [this message](https://disnake.com/channels"
                                f"/{ctx.guild.id}/{msg.channel.id}/{msg.id})"
                            ),
                            color=var.C_GREEN,
                        )
                    )

                else:
                    await ctx.send(
                        "Hmm it looks like that the message id you entered does"
                        " not have any reaction role so can't remove the unique"
                        " mark either."
                    )

            else:
                await ctx.send(
                    "Cannot remove the unique mark from that message since you"
                    " don't have any reaction roles yet :("
                )

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        "🚫 You need to define the message in order "
                        "to unmark it with unique reactions"
                    ),
                    color=var.C_RED,
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}uniquerr <messageid>`",
                )
            )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Listeners don't care about cog checks so need to add a check manually
        guild_doc = await db.REACTION_ROLES.find_one({"_id": payload.guild_id})

        if guild_doc is not None and guild_doc["reaction_roles"] is not None:
            for i in guild_doc["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(
                    payload.emoji
                ) == i.get("emoji"):
                    role_id = i.get("roleid")

                    guild = self.bot.get_guild(payload.guild_id)
                    assign_role = guild.get_role(role_id)

                    if not payload.member.bot:
                        await payload.member.add_roles(assign_role)

        if guild_doc is not None and payload.message_id in guild_doc["unique_messages"]:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            for r in message.reactions:
                if (
                    payload.member in await r.users().flatten()
                    and not payload.member.bot
                    and str(r) != str(payload.emoji)
                ):
                    await message.remove_reaction(r.emoji, payload.member)

    @commands.Cog.listener()
    # Listeners don't care about cog checks so need to add a check manually
    async def on_raw_reaction_remove(self, payload):
        guild_doc = await db.REACTION_ROLES.find_one({"_id": payload.guild_id})

        if guild_doc is not None and guild_doc["reaction_roles"] is not None:
            for i in guild_doc["reaction_roles"]:
                if payload.message_id == i.get("messageid") and str(
                    payload.emoji
                ) == i.get("emoji"):
                    role_id = i.get("roleid")

                    member = self.bot.get_guild(payload.guild_id).get_member(
                        payload.user_id
                    )

                    if member is not None:
                        guild = self.bot.get_guild(payload.guild_id)
                        remove_role = guild.get_role(role_id)
                        await member.remove_roles(remove_role)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
