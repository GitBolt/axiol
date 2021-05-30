import asyncio
import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix
from utils.greetings import greeting


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    def cog_check(self, ctx):
        GuildDoc = var.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome") == True:
            return ctx.guild.id


    @commands.command()
    async def welcomecard(self, ctx):
        GuildDoc = var.WELCOME.find_one({"_id": ctx.guild.id})
        embed = discord.Embed(
        title="Welcome to the server!",
        description=GuildDoc.get("greeting"),
        color=discord.Colour.random()
        ).set_image(url=GuildDoc.get("image")
        )
        await ctx.send(content=greeting(ctx.author.mention), embed=embed)


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
                await ctx.send(f"You need to define the greeting channel to change it!\n```{getprefix(ctx)}welcomechannel <#channel>```")
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
                description=f"The new greeting message is:\n\n**{usermsg.content}**",
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
    async def welcomerole(self, ctx, role:discord.Role=None):
        guildwelcome = var.WELCOME.find_one({"_id":ctx.guild.id})
        if guildwelcome is not None:
            if role is not None:
                rolelist = guildwelcome.get("assignroles")
                updatedlist = rolelist.copy()
                updatedlist.append(role.id)

                newdata = {"$set":{
                    "assignroles":updatedlist
                }}
                var.WELCOME.update_one(guildwelcome, newdata)
                await ctx.send(embed=discord.Embed(
                        title="Successfully added auto assign role",
                        description=f"Users will be automatically given {role.mention} when they join",
                        color=var.CGREEN)
                )
            else:
                await ctx.send(f"You need to define the role too!\n```{getprefix(ctx)}welcomerole <role>```\nFor role either role mention or ID can be used")
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not setup auto assign role",
                        description=f"This server does not have welcome greetings setted up hence i cannot give users auto role too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.command()
    async def welcomeremove(self, ctx):
        guildwelcome = var.WELCOME.find_one({"_id":ctx.guild.id})
        if guildwelcome is not None:
            var.WELCOME.delete_one(guildwelcome)
            await ctx.send(embed=discord.Embed(
            title="Successfully deleted welcome greetings",
            description=f"You can enable it again using {getprefix(ctx)}welcome",
            color=var.CGREEN)
            )
        else:
            await ctx.send(embed=discord.Embed(
                        title="Can not remove welcome greetings",
                        description=f"This server does not have welcome greetings setted up hence i cannot remove them too, use the command {getprefix(ctx)}welcome to enble it ",
                        color=var.CRED
            ))


    @commands.Cog.listener()
    async def on_member_join(self, member):
        GuildVerifyDoc = var.VERIFY.find_one({"_id": member.guild.id})
        GuildWelcomeDoc = var.WELCOME.find_one({"_id": member.guild.id})

        #Verification Stuff
        if GuildVerifyDoc is not None:
            roleid = GuildVerifyDoc.get("roleid")
            role = member.guild.get_role(roleid)
            await member.add_roles(role)


        #Welcome stuff
        servers = []
        for i in var.PLUGINS.find({"Welcome": True}):
            servers.append(i.get("_id"))

        if member.guild.id in servers and GuildWelcomeDoc is not None:
            channel = self.bot.get_channel(GuildWelcomeDoc.get("channelid"))

            embed = discord.Embed(
            title="Welcome to the server!",
            description=GuildWelcomeDoc.get("greeting"),
            color=discord.Colour.random()
            ).set_image(url=GuildWelcomeDoc.get("image"))
            await channel.send(content=greeting(member.mention), embed=embed)
            autoroles = GuildWelcomeDoc.get("assignroles")
            if autoroles != []:
                for i in autoroles:
                    await member.add_roles(member.guild.get_role(i))


def setup(bot):
    bot.add_cog(Welcome(bot))