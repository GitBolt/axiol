import discord
import asyncio
from typing import Union
from discord.ext import commands
import variables as var
import database as db
from functions import get_prefix
from ext.permissions import has_command_permission


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Moderation"):
            return True

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"{var.E_DISABLE} The Moderation plugin "
                        "is disabled in this server"
                    ),
                    color=var.C_ORANGE
                )
            )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @has_command_permission()
    async def ban(
            self, ctx, user: discord.User = None, *, reason="No reason given"
    ):
        if user is not None and user != ctx.author:

            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Applied ban to `{user}` :ok_hand:")

            try:
                await user.send(
                    embed=discord.Embed(
                        title=f"You have been banned from {ctx.guild.name}",
                        description=(
                            "Sorry I'm just a bot and I follow orders :("
                        ),
                        color=var.C_RED
                    ).add_field(
                        name="Reason",
                        value=reason
                    ).add_field(
                        name="Banned by", value=ctx.author
                    )
                )

            except discord.Forbidden:
                pass

        elif user == ctx.author:
            await ctx.send("You can't ban yourself :eyes:")

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the user to ban them,"
                        " reason is optional"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}ban <user> <reason>`"
                ).set_footer(
                    text="For user either User mention or User ID can be used")
                )

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to ban the user, "
                        "make sure that my I have ban members permission"
                        " and role is placed above the highest role which"
                        " the user has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @has_command_permission()
    async def unban(self, ctx, user: discord.User = None):
        if user is not None:
            bans = await ctx.guild.bans()
            banned_users = [ban.user for ban in bans]

            if user in banned_users:
                await ctx.guild.unban(user)
                await ctx.send(f'Successfully unbanned `{user}` :ok_hand:')

                try:
                    await user.send(
                        embed=discord.Embed(
                            title=(
                                f"You have been unbanned from {ctx.guild.name}!"
                            ),
                            description="Yay I would be happy to see you back!",
                            color=var.C_GREEN
                        ).add_field(
                            name="Unbanned by", value=ctx.author)
                        )

                except discord.Forbidden:
                    pass
            else:
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"The user `{user}` is not banned, "
                            "therefore cannot unban them."
                        ),
                        color=var.C_ORANGE
                    )
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description="🚫 You need to define the user to unban them",
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}unban <user>`"
                ).set_footer(
                    text="For user either User mention or User ID can be used")
                )

    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to unban the user, make "
                        "sure that I have ban members permission and my role "
                        "is placed above the highest role which the user has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @has_command_permission()
    async def mute(self, ctx, member: discord.Member = None):
        if member is not None:
            if not discord.utils.get(ctx.guild.roles, name='Muted'):
                muted_role = await ctx.guild.create_role(
                    name="Muted", colour=discord.Colour(0xa8a8a8)
                )

                for i in ctx.guild.text_channels:
                    await i.set_permissions(muted_role, send_messages=False)

            else:
                muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

            await member.add_roles(muted_role)
            await ctx.send(f"Applied chat mute to `{member}` :mute:")

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define member in order to mute them"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}mute <member>`"
                ).set_footer(
                    text=(
                        "For user either Member mention "
                        "or Member ID can be used"
                    )
                )
            )

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to mute the member, make"
                        " sure that I have manage roles permission and my role"
                        " is placed above the highest role which the member has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @has_command_permission()
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the member to unmute them"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}unmute <member>`"
                ).set_footer(
                    text=(
                        "For user either Member mention "
                        "or Member ID can be used"
                    )
                )
            )
        elif not discord.utils.get(ctx.guild.roles, name='Muted'):
            await ctx.send(
                "There is no muted role yet hence I cannot unmute, "
                "Muting someone automatically makes one."
            )

        else:
            muted_role = discord.utils.get(ctx.guild.roles, name='Muted')

            await member.remove_roles(muted_role)
            await ctx.send(f"Unmuted `{member}` :sound:")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to unmute the user, "
                        "make sure that I have manage roles permission and "
                        "my role is placed above the highest role which the "
                        "user has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @has_command_permission()
    async def kick(
        self, ctx, member: discord.Member = None, *, reason="No reason provided"
    ):
        if member is not None and member != ctx.author:
            await member.kick(reason=reason)
            await ctx.send(f"`{member}` have been kicked from the server")

            try:
                await member.send(
                    embed=discord.Embed(
                        title=f"You have been kicked from {ctx.guild.name}",
                        color=var.C_RED
                    ).add_field(
                        name="Reason", value=reason
                    ).add_field(
                        name="Kicked by", value=ctx.author
                    )
                )

            except discord.Forbidden:
                pass

        elif member == ctx.author:
            await ctx.send("You can't kick yourself :eyes:")

        else:
            await ctx.send(embed=discord.Embed(
                description="🚫 You need to define the member to kick them",
                color=var.C_RED
            ).add_field(
                name="Format",
                value=f"`{await get_prefix(ctx)}kick <member>`"
            ).set_footer(
                text="For user either Member mention or Member ID can be used")
            )

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to kick the member,"
                        " make sure that I have kick members permission"
                        " and my role is placed above the highest role "
                        "which the member has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command(aliases=["nickname", "changenick"])
    @commands.has_permissions(change_nickname=True)
    @has_command_permission()
    async def nick(self, ctx, member: discord.Member = None, *, nick=None):
        if member and nick is not None:
            await member.edit(nick=nick)
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        f"{var.E_ACCEPT} Nickname changed "
                        f"for `{member}` to {nick}"
                    ),
                    color=var.C_GREEN
                )
            )

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define both the member"
                        " and their new nick"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}nick <member> <new nick>`"
                ).set_footer(
                    text="For Member either mention or Member ID can be used"
                )
            )

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description=(
                        "🚫 I don't have permissions to change the nickname "
                        "of the member, make sure that I have change nickname "
                        "permission and my role is placed above the highest "
                        "role which the member has"
                    ),
                    color=var.C_RED
                )
            )

    @commands.command(aliases=["clean", "clear"])
    @commands.has_permissions(manage_messages=True)
    @has_command_permission()
    async def purge(self, ctx, limit: int = None):
        if limit is not None:
            await ctx.channel.purge(limit=limit + 1)

            info = await ctx.send(embed=discord.Embed(
                description=f"Deleted {limit} messages",
                color=var.C_ORANGE)
            )
            await asyncio.sleep(1)
            await info.delete()

        else:
            await ctx.send(
                embed=discord.Embed(
                    description=(
                        "🚫 You need to define the amount"
                        " to delete messages too! Make sure the amount is numerical."
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"`{await get_prefix(ctx)}purge <amount>`"
                )
            )

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(
                embed=discord.Embed(
                    title="Permission error",
                    description="🚫 I don't have permissions to delete messages",
                    color=var.C_RED
                )
            )

    @commands.command(aliases=["giverole"])
    @has_command_permission()
    async def addrole(
        self, ctx, member: discord.Member = None, role: discord.Role = None
    ):
        if member and role is not None:
            try:
                await member.add_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Successfully updated {member.mention} "
                            f"with {role.mention} role"
                        ),
                        color=var.C_GREEN
                    )
                )

            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        title="Missing permissions",
                        description=(
                            f"I don't have permissions to update the roles"
                            f" of {member.mention}, either I don't have the"
                            f" permission or the member is above me"
                        ),
                        color=var.C_RED
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description="You need to define both member and role",
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}addrole <member> <role>```"
                ).set_footer(
                    text=(
                        "For both member and role, "
                        "either ping or ID can be used"
                    )
                )
            )

    @commands.command(name="removerole")
    @has_command_permission()
    async def remove_role(
        self, ctx, member: discord.Member = None, role: discord.Role = None
    ):
        if member and role is not None:
            try:
                await member.remove_roles(role)
                await ctx.send(
                    embed=discord.Embed(
                        description=(
                            f"Successfully updated {member.mention} "
                            f"by removing {role.mention} role"
                        ),
                        color=var.C_GREEN
                    )
                )

            except discord.Forbidden:
                await ctx.send(
                    embed=discord.Embed(
                        title="Missing permissions",
                        description=(
                            f"I don't have permissions to update the roles of"
                            f" {member.mention}, either I don't have the"
                            f" permission or the member is above me"
                        ),
                        color=var.C_RED
                    )
                )
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description="You need to define both member and role",
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=(
                        f"```{await get_prefix(ctx)}removerole"
                        f" <member> <role>```"
                    )
                ).set_footer(
                    text=(
                        "For both member and role,"
                        " either ping or ID can be used"
                    )
                )
            )

    @commands.command(name="massrole")
    @has_command_permission()
    async def mass_role(
        self, ctx, role: discord.Role = None, role2: discord.Role = None
    ):
        if role is not None and role2 is not None:
            bot_msg = await ctx.send(
                embed=discord.Embed(
                    title="Confirmation",
                    description=(
                        f"Are you sure you want to update all members"
                        f" with the role {role.mention} with {role2.mention}?"
                    ),
                    color=var.C_BLUE
                ).add_field(
                    name=(
                        "Note that this action is irreversible "
                        "and cannot be stopped once started"
                    ),
                    value=(
                        f"{var.E_ACCEPT} to accept\n"
                        f"{var.E_ENABLE} to accept with live stats\n"
                        f"{var.E_DECLINE} to decline"
                    )
                )
            )

            await bot_msg.add_reaction(var.E_ACCEPT)
            await bot_msg.add_reaction(var.E_ENABLE)
            await bot_msg.add_reaction(var.E_DECLINE)

            def reaction_check(r, u):
                return u == ctx.author and r.message == bot_msg

            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            updates = False

            try:
                await bot_msg.clear_reactions()
            except Exception:
                pass

            if str(reaction.emoji) == var.E_DECLINE:
                return await ctx.send("Cancelled mass role update")

            if str(reaction.emoji) == var.E_ENABLE:
                updates = True

            if (
                str(reaction.emoji) == var.E_ENABLE
                or str(reaction.emoji) == var.E_ACCEPT
            ):

                count = 0

                for member in [
                    member
                    for member in ctx.guild.members
                    if role in member.roles
                ]:
                    try:
                        await member.add_roles(role2)
                        count += 1

                        if updates:
                            await ctx.send(f"{member} updated")

                    except discord.Forbidden:
                        await ctx.send(
                            embed=discord.Embed(
                                description=(
                                    f"Error giving role to {member.mention}"
                                ),
                                color=var.C_ORANGE
                            )
                        )

                    await asyncio.sleep(1)

                await ctx.send(
                    f"Done, updated **{count}** members "
                    f"with the {role2.name} role"
                )

        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both Role 1 and Role 2\n`role1` "
                        "are the members having that role and `role2` is the"
                        " one to be given to them"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}massrole <role1> <role2>```"
                ).set_footer(
                    text="For role, either ping or ID can be used"
                )
            )

    @commands.command(name="massroleremove")
    @has_command_permission()
    async def mass_role_remove(
        self, ctx, role: discord.Role = None, role2: discord.Role = None
    ):
        if role is not None and role2 is not None:
            bot_msg = await ctx.send(
                embed=discord.Embed(
                    title="Confirmation",
                    description=(
                        f"Are you sure you want to update"
                        f" all members with the role {role.mention}"
                        f" by removing {role2.mention}?"
                    ),
                    color=var.C_BLUE
                ).add_field(
                    name=(
                        "Note that this action is irreversable"
                        " and cannot be stopped once started"
                    ),
                    value=(
                        f"{var.E_ACCEPT} to accept\n{var.E_ENABLE}"
                        f" to accept with live stats\n{var.E_DECLINE} to decline"
                    )
                )
            )

            await bot_msg.add_reaction(var.E_ACCEPT)
            await bot_msg.add_reaction(var.E_ENABLE)
            await bot_msg.add_reaction(var.E_DECLINE)

            def reaction_check(r, u):
                return u == ctx.author and r.message == bot_msg

            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=reaction_check
            )

            updates = False

            try:
                await bot_msg.clear_reactions()

            except Exception:
                pass

            if str(reaction.emoji) == var.E_DECLINE:
                return await ctx.send("Cancelled mass role update")

            if str(reaction.emoji) == var.E_ENABLE:
                updates = True

            if str(reaction.emoji) == var.E_ENABLE or str(
                    reaction.emoji) == var.E_ACCEPT:
                count = 0
                for member in [
                    member
                    for member in ctx.guild.members
                    if role in member.roles
                ]:
                    try:
                        await member.remove_roles(role2)
                        count += 1
                        if updates:
                            await ctx.send(f"{member} updated")

                    except discord.Forbidden:
                        await ctx.send(
                            embed=discord.Embed(
                                description=(
                                    f"Error giving role to {member.mention}"
                                ),
                                color=var.C_ORANGE
                            )
                        )
                    await asyncio.sleep(1)

                await ctx.send(
                    f"Done,"
                    f" updated **{count}** members with the {role2.name} role"
                )
        else:

            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both Role 1 and Role 2\n"
                        "`role1` are the members having that role"
                        " and `role2` is the one to be removed from them"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=(
                        f"```{await get_prefix(ctx)}massroleremove"
                        f" <role1> <role2>```"
                    )
                ).set_footer(
                    text="For role, either ping or ID can be used"
                )
            )

    @commands.command()
    @has_command_permission()
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        if member and reason is not None:
            guild_col = db.WARNINGS_DATABASE[str(ctx.guild.id)]
            user_warns = await guild_col.find_one({"_id": member.id})

            if user_warns is None:
                new_warns = [reason]
                await guild_col.insert_one(
                    {"_id": member.id, "warns": new_warns}
                )

            else:
                current_warns = user_warns["warns"]
                new_warns = current_warns.copy()
                new_warns.append(reason)
                new_data = {
                    "$set": {
                        "warns": new_warns
                    }
                }

                await guild_col.update_one(user_warns, new_data)

            await ctx.send(
                content=f"{member.mention} has been warned!",
                embed=discord.Embed(
                    description=(
                        f"Reason: **{reason}**\n"
                        f"Total warns: **{len(new_warns)}**"
                    ),
                    color=var.C_BLUE
                ).set_footer(
                    text=f"Moderator: {ctx.author}"
                )
            )

        elif member is not None and reason is None:
            await ctx.send("Reason is required too!")

        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both the member"
                        " and reason to warn them!"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}warn <member> <reason>```"
                )
            )

    @commands.command(name="removewarn", aliases=["remove-warn", "unwarn"])
    @has_command_permission()
    async def remove_warn(
        self, ctx, member: discord.Member = None, position=None
    ):
        if member and position is not None:
            try:
                position = int(position)

            except ValueError:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"The position should be a number!",
                        color=var.C_RED)
                    )
                return

            guild_col = db.WARNINGS_DATABASE[str(ctx.guild.id)]
            user_doc = await guild_col.find_one({"_id": member.id})

            if user_doc is None:
                await ctx.send(
                    embed=discord.Embed(
                        description=f"{member.mention} does not have any warns",
                        color=var.C_RED
                    ).set_footer(
                        text=(
                            "Note that this warn's position has been taken by"
                            " the warn below it, therefore moving all warns "
                            "below this one position above"
                        )
                    )
                )

            else:
                warns = user_doc["warns"]
                if len(warns) - 1 >= position - 1:
                    reason = warns[position - 1]
                    new_warns = warns.copy()
                    new_warns.pop(position - 1)
                    new_data = {
                        "$set": {
                            "warns": new_warns
                        }
                    }

                    await guild_col.update_one(user_doc, new_data)
                    await ctx.send(
                        embed=discord.Embed(
                            description=(
                                f"{var.E_ACCEPT} Removed {position} warn with "
                                f"the reason **{reason}** from {member.mention}"
                            ),
                            color=var.C_GREEN
                        ).set_footer(
                            text=(
                                "Note that if there are any warns below this "
                                "one then they are moved one position up to "
                                "take the removed warn's place"
                            )
                        )
                    )

                else:
                    await ctx.send(
                        embed=discord.Embed(
                            description=(
                                f"{member.mention} does not have"
                                f" {position} warn(s)"
                            ),
                            color=var.C_RED
                        )
                    )

        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define both the member "
                        "and the warn position to remove the warn"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=(
                        f"```{await get_prefix(ctx)}removewarn "
                        "<member> <position>```"
                    )
                ).set_footer(
                    text="Note that position here is just a number"
                )
            )

    @commands.command()
    @has_command_permission()
    async def warns(self, ctx, member: discord.Member = None):
        if member is not None:
            guild_col = db.WARNINGS_DATABASE[str(ctx.guild.id)]
            userdata = await guild_col.find_one({"_id": member.id})

            if userdata is None:
                await ctx.send(f"{member} does not have any warnings")

            else:
                warns = userdata["warns"]
                embed = discord.Embed(
                    title=f"{member} warns", color=var.C_MAIN
                )
                for i in warns:
                    embed.add_field(
                        name=f"Warn {warns.index(i) + 1}", value=i,
                        inline=False
                    )

                await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=discord.Embed(
                    title=f"🚫 Missing arguments",
                    description=(
                        "You need to define the member to view their warns"
                    ),
                    color=var.C_RED
                ).add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}warns <member>```"
                )
            )


def setup(bot):
    bot.add_cog(Moderation(bot))
