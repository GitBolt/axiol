import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verifysetup(self, ctx, channel:discord.TextChannel=None):
        guildverif = var.VERIFY.find_one({"_id":ctx.guild.id})
        if guildverif is None:
            if channel is not None:
                embed = discord.Embed(
                title="Setup verification",
                description="React to the respective emojis below to choose the verification type",
                color=var.CMAIN
                ).add_field(name="Command verification", value=f"{var.ACCEPT} Simple command", inline=False
                ).add_field(name="Bot verification", value="🤖 Captcha like image", inline=False)
                botmsg = await ctx.send(embed=embed)
                await botmsg.add_reaction(var.ACCEPT)
                await botmsg.add_reaction("🤖")

                def check(reaction, user):
                    return user == ctx.author and reaction.message == botmsg

                reaction, user = await self.bot.wait_for('reaction_add', check=check)
                if str(reaction.emoji) == var.ACCEPT:
                    await ctx.send(embed=discord.Embed(
                        title="Command verification",
                        description=f"Successfully setted up verification, now new joined members will be able to access other channels only after they verify in {channel.mention}",
                        color=var.CGREEN
                    ).set_footer(text="You can change the permissions of channels and settings of the role (name, color, order etc), just don't delete the role")
                    )
                    NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                    for i in ctx.guild.text_channels:
                        await i.set_permissions(NVerified, view_channel=False)
                    await channel.set_permissions(NVerified, view_channel=True)
                    var.VERIFY.insert_one({"_id":ctx.guild.id, "type": "Command", "channel": channel.id, "roleid": NVerified.id})

                if str(reaction.emoji) == "🤖":
                    await ctx.send(embed=discord.Embed(
                        title="Bot verification",
                        description=f"Successfully setted up verification, now new joined members will be able to access other channels only after they verify in {channel.mention}",
                        color=var.CGREEN
                    ).set_footer(text="You can change the permissions of channels and settings of the role (name, color, order etc), just don't delete the role")
                    )
                    NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                    for i in ctx.guild.text_channels:
                        await i.set_permissions(NVerified, view_channel=False)
                    await channel.set_permissions(NVerified, view_channel=True)
                    var.VERIFY.insert_one({"_id":ctx.guild.id, "type": "bot", "channel": channel.id, "roleid": NVerified.id})

            else:
                await ctx.send(f"Looks like you forgot to mention the verification channel, if you don't have one already then create it!\n```{getprefix(ctx)}verifysetup <#channel>```")

        else:
            await ctx.send("Verification for this server is already enabled.")

def setup(bot):
    bot.add_cog(Verification(bot))