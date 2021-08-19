import sys
import traceback
import discord
import asyncio
from discord.ext import commands
from variables import C_RED


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Invalid Channel
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Invalid Channel",
                    description=(
                        "🚫 Are you sure the channel ID "
                        "or channel mention was correct?"
                    ),
                    color=C_RED
                ).set_footer(
                    text=(
                        "You can either mention the channel (example: #general)"
                        " or use the channel's id (example: 843516084266729515)"
                    )
                )
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=discord.Embed(
                    title="Missing Permissions",
                    description=(
                        "🚫 You don't have permissions to do that "
                        f"{ctx.author.name} "
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Member not found",
                    description=(
                        f"🚫 You sure the mention/ID is correct? "
                        f"Or maybe they left? "
                        f"Maybe they don't even exist? "
                        f"[SpongoBob?](https://youtu.be/wjXBqelv4GM)"
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.UserNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="User not found",
                    description=(
                        "🚫 Make sure the User ID is correct,"
                        " if you are sure it's correct then perhaps the "
                        "User deleted their account?"
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.MessageNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Message not found",
                    description=(
                        "🚫 Are you sure that the message ID belongs "
                        "to this server and is valid?"
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.GuildNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Guild not found",
                    description=(
                        "🚫 Looks like I'm not in the guild or the ID is"
                        " incorrect, maybe invite me there :eyes:"
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Role not found",
                    description=(
                        "🚫 Make sure that the ID or mention is correct. "
                        "Maybe you pinged any member instead of the role?"
                        " Maybe you copied the wrong ID?"
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.EmojiNotFound):
            await ctx.send(
                embed=discord.Embed(
                    title="Emoji not found",
                    description=(
                        "🚫 Either the emoji is invalid or "
                        "I'm not in the server where this emoji "
                        "is from to be able to use it."
                    ),
                    color=C_RED
                )
            )

        elif isinstance(error, commands.CommandNotFound):
            if not ctx.message.content.endswith("."):
                print(f"Command: {ctx.message.content} from {ctx.guild.name}")

        elif isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, asyncio.TimeoutError):
                await ctx.send(
                    "Time is up! You failed to respond under time "
                    "therefore the process has been cancelled."
                )

            else:
                traceback.print_exception(
                    type(error), error, error.__traceback__, file=sys.stderr
                )

        elif not isinstance(error, commands.CheckFailure):
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot):
    bot.add_cog(Errors(bot))
