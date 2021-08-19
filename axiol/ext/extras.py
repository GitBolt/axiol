import discord
from discord.ext import commands
import axiol.variables as var
from axiol.functions import get_prefix
import axiol.database as db


class Extras(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            f"Pong 🏓! Response time: {round(self.bot.latency * 1000)}ms"
        )

    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(
            title="My Github Source Code Woohoo",
            description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)",
            color=var.C_TEAL
        ).set_thumbnail(
            url=(
                "https://cdn0.iconfinder.com/data/"
                "icons/shift-logotypes/32/Github-512.png"
            )
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="My invite link!",
            description=(
                "[Invite me from here](https://discord.com/oauth2/authorize"
                "?client_id=843484459113775114&permissions=473295959&scope=bot)"
            ),
            color=var.C_BLUE
        ).set_thumbnail(
            url=(
                "https://cdn.discordapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, desc=None):
        if desc is not None:
            # Support server suggestion channel
            channel = self.bot.get_channel(843548616505294848)

            embed = discord.Embed(
                title=f"{ctx.author}'s idea",
                description=(
                    f"This idea came from a server named **{ctx.guild.name}**!"
                ),
                color=var.C_BLUE
            ).add_field(
                name="Suggestion", value=desc
            )

            msg = await channel.send(embed=embed)
            await msg.add_reaction(var.E_ACCEPT)
            await msg.add_reaction(var.E_DECLINE)
            await ctx.send("Suggestion sent to the support server!")

        else:
            await ctx.send(
                f"You need to describe your idea too! This is the format\n"
                f"```{await get_prefix(ctx)} <description of your idea>```\n"
                f"Don't forget the space after prefix :D"
            )

    @commands.command(aliases=["bot", "info"])
    async def about(self, ctx):
        guild_count = 0
        member_count = 0
        ping = f"{round(self.bot.latency * 1000)}ms"

        for guild in self.bot.guilds:
            guild_count += 1
            member_count += guild.member_count

        embed = discord.Embed(
            title="Some information about me :flushed:",
            description=(
                f"[Donation](https://paypal.me/palbolt) "
                f"[Vote](https://top.gg/bot/843484459113775114/vote) "
                f"[Support](https://discord.gg/hxc73psNsB)"
            ),
            color=var.C_MAIN
        ).add_field(
            name="Server Count",
            value=str(guild_count),
            inline=False
        ).add_field(
            name="Members",
            value=member_count,
            inline=False
        ).add_field(
            name="Made by",
            value="Bolt#8905",
            inline=False
        ).add_field(
            name="Creation date",
            value="16 May, 2021",
            inline=False
        ).set_footer(
            text=f"Ping: {ping}"
        ).set_thumbnail(
            url=(
                "https://cdn.discordapp.com/attachments/843519647055609856/"
                "845662999686414336/Logo1.png"
            )
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        embed = discord.Embed(
            title=f"{ctx.guild.name}",
            color=var.C_TEAL
        )

        embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(
            name="All Members", value=ctx.guild.member_count, inline=False
        )

        embed.add_field(
            name="Channels", value=str(len(ctx.guild.channels)), inline=False
        )

        embed.add_field(
            name="Voice Channels",
            value=str(len(ctx.guild.voice_channels)),
            inline=False
        )

        embed.add_field(
            name="Roles", value=str(len(ctx.guild.roles)), inline=False
        )

        embed.add_field(
            name="Boost Level", value=ctx.guild.premium_tier, inline=False
        )

        embed.add_field(
            name="Created at",
            value=str(ctx.guild.created_at.strftime("%Y - %m - %d")),
            inline=False
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        guild_verify_doc = await db.VERIFY.find_one({"_id": ctx.guild.id})
        if guild_verify_doc is not None:
            role = ctx.guild.get_role(guild_verify_doc.get("roleid"))

            count = sum(role in member.roles for member in ctx.guild.members)
            embed.add_field(name="Non Verified Members", value=str(count))

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Extras(bot))
