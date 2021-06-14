import discord
import asyncio
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Moderation") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user:discord.User=None, *, reason="No reason given"):
        if user is not None and user != ctx.author:

            await ctx.guild.ban(user, reason=reason)
            await ctx.send(f"Applied ban to `{user}` :ok_hand:")

            try:
                await user.send(embed=discord.Embed(
                    title=f"You have been banned from {ctx.guild.name}",
                    description="Sorry I'm just a bot and I follow orders :(", 
                    color=var.C_RED).add_field(name="Reason", value=reason
                    ).add_field(name="Banned by", value=ctx.author)
                    )
            except discord.Forbidden:
                pass

        elif user == ctx.author:
            await ctx.send("You can't ban yourself :eyes:")

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the user to ban them, reason is optional",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}ban <user> <reason>`"
            ).set_footer(text="For user either User mention or User ID can be used")
            )
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
                await ctx.send(embed=discord.Embed(
                    title="Permission error",
                    description=f"{var.E_ERROR} I don't have permissions to ban the user, make sure that my I have ban members permission and role is placed above the highest role which the user has",
                    color=var.C_RED
                )
                )



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user:discord.User=None):
        if user is not None and user != ctx.author:

            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned `{user}` :ok_hand:')

            try:
                await user.send(embed=discord.Embed(
                                title=f"You have been unbanned from {ctx.guild.name}!",
                                description="Yay I would be happy to see you back!", 
                                color=var.C_GREEN
                                ).add_field(name="Unbanned by", value=ctx.author)
                                )
            except discord.Forbidden:
                pass

        elif user == ctx.author:
            await ctx.send("You are not even banned why you trying to unban yourself :face_with_raised_eyebrow:")

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the user to unban them",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}unban <user>`"
            ).set_footer(text="For user either User mention or User ID can be used")
            )         
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to unban the user, make sure that I have ban members permission and my role is placed above the highest role which the user has",
                color=var.C_RED
            )
            )



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member=None):
        if member is not None:

            if not discord.utils.get(ctx.guild.roles, name='Muted'):
                mutedrole = await ctx.guild.create_role(name="Muted", colour=discord.Colour(0xa8a8a8))
                for i in ctx.guild.text_channels:
                    await i.set_permissions(mutedrole, send_messages=False)
            else:
                mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(mutedrole)
                await ctx.send(f"Applied chat mute to `{member}` :mute:")

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define member in order to mute them",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}mute <member>`"
            ).set_footer(text="For user either Member mention or Member ID can be used")
            )
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to mute the member, make sure that I have manage roles permission and my role is placed above the highest role which the member has",
                color=var.C_RED
            )
            )



    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member:discord.Member=None):
        if member is not None:

            if not discord.utils.get(ctx.guild.roles, name='Muted'): 
                await ctx.send("There is no muted role yet hence I cannot unmute, Muting someone automatically makes one.")
            else:
                mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
                await member.remove_roles(mutedrole)
                await ctx.send(f"Unmuted `{member}` :sound:")

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the member to unmute them",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}unmute <member>`"
            ).set_footer(text="For user either Member mention or Member ID can be used")
            )
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to unmute the user, make sure that I have manage roles permission and my role is placed above the highest role which the user has",
                color=var.C_RED
            )
            )



    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member=None, *, reason="No reason provided"):
        if member is not None and member != ctx.author:  

            await member.kick(reason=reason)
            await ctx.send(f"`{member}` have been kicked from the server")
            try:
                await member.send(embed=discord.Embed(
                                title=f"You have been kicked from {ctx.guild.name}",
                                color=var.C_RED
                                ).add_field(name="Reason", value=reason
                                ).add_field(name="Kicked by", value=ctx.author)
                                )
            except discord.Forbidden:
                pass

        elif member == ctx.author:
            await ctx.send("You can't kick yourself :eyes:")

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the member to kick them",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}kick <member>`"
            ).set_footer(text="For user either Member mention or Member ID can be used")
            )
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to kick the member, make sure that I have kick members permission and my role is placed above the highest role which the member has",
                color=var.C_RED
            )
            )


    @commands.command(aliases=["nickname", "changenick"])
    @commands.has_permissions(change_nickname=True)
    async def nick(self, ctx, member: discord.Member=None, *,nick=None):
        if member and nick is not None:
            await member.edit(nick=nick)
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_ACCEPT} Nickname changed for `{member}` to {nick}",
                color=var.C_GREEN
            ))

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define both the member and their new nick",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}nick <member> <new nick>`"
            ).set_footer(text="For Member either mention or Member ID can be used")
            )
    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to change the nickname of the member, make sure that I have change nickname permission and my role is placed above the highest role which the member has",
                color=var.C_RED
            )
            )




    @commands.command(aliases=["clean", "clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit:int=None):
        if limit is not None:
            await ctx.channel.purge(limit=limit+1)

            info = await ctx.send(embed=discord.Embed(
                                description=f"Deleted {limit} messages",
                                color=var.C_ORANGE)
                                )
            await asyncio.sleep(1)
            await info.delete()
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the amount to delete messages too!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}purge <amount>`"
            )
            )
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, discord.Forbidden):
            await ctx.send(embed=discord.Embed(
                title="Permission error",
                description=f"{var.E_ERROR} I don't have permissions to delete messages",
                color=var.C_RED
            )
            )   



def setup(bot):
    bot.add_cog(Moderation(bot))
