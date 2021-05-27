import asyncio
import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix
from utils.greetings import greeting


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def welcome(self, ctx, channel:discord.TextChannel=None):
        guildwelcome = var.WELCOME.find_one({"_id": ctx.guild.id})
        if guildwelcome is None:
            if channel is not None:
                var.WELCOME.insert_one({

                    "_id":ctx.guild.id,
                    "channelid":channel.id,
                    "greeting": "Hope you enjoy your stay here :)",
                    "image": "https://image.freepik.com/free-vector/welcome-sign-neon-light_110464-147.jpg"
                })

                embed = discord.Embed(
                title="Successfully setted up welcome greeting",
                description=f"Now members joining the server will now be greeted in {channel.mention} channel!",
                color=var.CGREEN
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"You need to define the greeting channel too!\n```{getprefix(ctx)}welcome <#channel>```")
        else:
            await ctx.send("Welcome greeting for this server is already enabled")


    @commands.command()
    async def welcomechannel(self, ctx, channel:discord.TextChannel=None):
        guildwelcome = var.WELCOME.find_one({"_id":ctx.guild.id})
        if guildwelcome is not None:
            if channel is not None:
                newdata = {"$set":{
                    "channelid": channel.id
                }}
                var.WELCOME.update_one(guildwelcome, newdata)
                await ctx.send(embed=discord.Embed(
                title="Changed welcome channel",
                description=f"Now users will be greeted in {channel.mention}!",
                color=var.CGREEN)
                )
            else:
                await ctx.send(f"You need to define the greeting channel to change it!\n```{getprefix(ctx)}welcomechannel <#channel>")
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not setup welcome channel",
                        description=f"This server does not have welcome greetings setted up hence I cannot change the channel too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.command()
    async def welcomemessage(self, ctx):
        guildwelcome = var.WELCOME.find_one({"_id": ctx.guild.id})
        if guildwelcome is not None:
            await ctx.send("Send a message to make it the greeting (description) of welcome message embeds!")
            def msgcheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id
            try:
                usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
                newdata = {"$set":{
                    "greeting": usermsg.content
                }}
                var.WELCOME.update_one(guildwelcome, newdata)
                await ctx.send(embed=discord.Embed(
                title="Successfully changed the greeting message!",
                description=f"The new greeting message is:\n{usermsg.content}",
                color=var.CGREEN)
                )
            except asyncio.TimeoutError:
                await ctx.send("You took too long ;-;")
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not setup welcome message",
                        description=f"This server does not have welcome greetings setted up hence I cannot change the message too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.command()
    async def welcomeimage(self, ctx):
        guildwelcome = var.WELCOME.find_one({"_id":ctx.guild.id})
        if guildwelcome is not None:
            await ctx.send("Send an image or image link to make it the greeting image!")

            def msgcheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id
            try:
                usermsg = await self.bot.wait_for("message", check=msgcheck, timeout=30.0)
                if usermsg.attachments:
                    newdata = {"$set":{
                        "image": usermsg.attachments[0].url
                    }}
                    var.WELCOME.update_one(guildwelcome, newdata)
                    await ctx.send(embed=discord.Embed(
                    title="Successfully changed welcome image",
                    description="New welcome image is:",
                    color=var.CGREEN
                    ).set_image(url=usermsg.attachments[0].url)
                    )
                elif usermsg.content.startswith("http"):
                    newdata = {"$set":{
                        "image": usermsg.content
                    }}
                    var.WELCOME.update_one(guildwelcome, newdata)
                    await ctx.send(embed=discord.Embed(
                    title="Successfully changed welcome image",
                    description="New welcome image is:",
                    color=var.CGREEN
                    ).set_image(url=usermsg.content)
                    )
                else:
                    await ctx.send("Invalid image")
            except asyncio.TimeoutError:
                await ctx.send("You too too long ;-;")
                
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not setup welcome image",
                        description=f"This server does not have welcome greetings setted up hence I cannot change the image too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.command()
    async def welcomeremove(self, ctx):
        guildwelcome = var.WELCOME.find_one({"_id":ctx.guild.id})
        if guildwelcome is not None:
            var.WELCOME.delete_one(guildwelcome)
            await ctx.send(embed=discord.Embed(
            title="Successfully deleted welcome greetings",
            description=f"You can enable it again using {getprefix(ctx)}welcome"),
            color=var.CGREEN
            )
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not remove welcome greetings",
                        description=f"This server does not have welcome greetings setted up hence i cannot remove them too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.Cog.listener()
    async def on_member_join(self, member):
        guildverify = var.VERIFY.find_one({"_id": member.guild.id})
        if guildverify is not None:
            roleid = guildverify.get("roleid")
            role = member.guild.get_role(roleid)
            await member.add_roles(role)

        guildwelcome = var.WELCOME.find_one({"_id": member.guild.id})
        if guildwelcome is not None:
            channel = self.bot.get_channel(guildwelcome.get("channelid"))

            embed = discord.Embed(
            title="Welcome to the server!",
            description=guildwelcome.get("greeting"),
            color=discord.Colour.random()
            ).set_image(url=guildwelcome.get("image"))
            await channel.send(content=greeting(member.mention), embed=embed)


def setup(bot):
    bot.add_cog(Welcome(bot))