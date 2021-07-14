import asyncio
import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix
from greetings import greeting
from ext.permissions import has_command_permission

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    #This command isn't really used, just putted this here to invoke on first welcome plugin enable
    @commands.command()
    @has_command_permission()
    async def welcomesetup(self, ctx):
        embed = discord.Embed(
        title="Send the welcome channel where I can greet members!",
        description="Since this is the first time this plugin is being enabled, I need to know where I am supposed to greet new members :D",
        color=var.C_BLUE
        ).set_footer(text="The next message which you will send will become the welcome channel, make sure that the Channel/ChannelID is valid other wise this won't work"
        )
        await ctx.send(embed=embed)
        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id
        usermsg = await self.bot.wait_for('message', check=messagecheck)
        try:
            chid = int(usermsg.content.strip("<>#"))
        except:
            await ctx.send(embed=discord.Embed(
                        title="Invalid Channel",
                        description="🚫 I was not able to find the channel which you entered",
                        color=var.C_RED
                    ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
                    )

        db.WELCOME.insert_one({

            "_id":ctx.guild.id,
            "channelid":chid,
            "message": None,
            "welcomegreeting": "Hope you enjoy your stay here ✨",
            "image": "https://cdn.discordapp.com/attachments/843519647055609856/864924991597314078/Frame_1.png📷",
            "assignroles": []
        })
        successembed = discord.Embed(
        title="Welcome greeting successfully setted up",
        description=f"{var.E_ACCEPT} New members will now be greeted in {self.bot.get_channel(chid).mention}!",
        color=var.C_GREEN
        ).add_field(name="To configure further", value=f"`{getprefix(ctx)}help welcome`")
        
        await ctx.send(embed=successembed)        


    @commands.command()
    @has_command_permission()
    async def welcomecard(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})
        
        def getcontent():
            if GuildDoc.get("message") is None:
                content = greeting(ctx.author.mention)
            else:
                content = GuildDoc.get("message")
            return content
            
        embed = discord.Embed(
        title="Welcome to the server!",
        description=GuildDoc.get("greeting"),
        color=discord.Colour.random()
        ).set_image(url=GuildDoc.get("image")
        )
        await ctx.send(content=getcontent(), embed=embed)


    @commands.command()
    @has_command_permission()
    async def welcomechannel(self, ctx, channel:discord.TextChannel=None):
        GuildDoc = db.WELCOME.find_one({"_id":ctx.guild.id})

        if channel is not None:
            newdata = {"$set":{
                "channelid": channel.id
            }}
            db.WELCOME.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
            title="Changed welcome channel",
            description=f"{var.E_ACCEPT} Now users will be greeted in {channel.mention}",
            color=var.C_GREEN)
            )

        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the greeting channel to change it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}welcomechannel <#channel>`"))


    @commands.command()
    @has_command_permission()
    async def welcomemessage(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(embed=discord.Embed(
                    tite="Send a message to make it the welcome message",
                    description="The next message which you will send will become the embed message!",
                    color=var.C_BLUE
        ).add_field(name="Cancel", value=f"Type `cancel` to stop this process"
        ).set_footer(text="Don't confuse this with welcome greeting, that's different! This is the text message which pings the member and is outside the embed card itself, the greeting is the description of the embed")
        )

        def msgcheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=300.0)

            if usermsg.content == "cancel" or usermsg.content == "`cancel`":
                await ctx.send("Cancelled welcome message change :ok_hand:")
            else:
                newdata = {"$set":{
                    "message": usermsg.content
                }}
                db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed the welcome message!",
                description=f"The new welcome message is:\n**{usermsg.content}**",
                color=var.C_GREEN)
                )
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}** you took too long to enter your message, try again maybe?")


    @commands.command()
    @has_command_permission()
    async def welcomegreeting(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(embed=discord.Embed(
                    tite="Send a message to make it the welcome greeting!",
                    description="The next message which you will send will become the embed description!",
                    color=var.C_BLUE
        ).add_field(name="Cancel", value=f"Type `cancel` to cancel this"
        ).set_footer(text="Don't confuse this with embed message, that's different! This is the embed description which is inside the embed itself however welcome message is the content outside where members are pinged!")
        )

        def msgcheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
            if usermsg.content == "cancel" or usermsg.content == "`cancel`":
                await ctx.send("Cancelled welcome message change :ok_hand:")
            else:
                newdata = {"$set":{
                    "welcomegreeting": usermsg.content
                }}
                db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed the greeting message!",
                description=f"The new greeting message is:\n**{usermsg.content}**",
                color=var.C_GREEN)
                )
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}** you took too long to enter your message, try again maybe?")


    @commands.command()
    @has_command_permission()
    async def welcomeimage(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(embed=discord.Embed(
                    tite="Send a message to make it the image",
                    description="Either send the image as a file or use a link!",
                    color=var.C_BLUE
        ).add_field(name="Cancel", value=f"Type `cancel` to cancel this")
        )
        def msgcheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id
        try:
            usermsg = await self.bot.wait_for("message", check=msgcheck, timeout=60.0)

            if usermsg.content == "cancel" or usermsg.content == "`cancel`":
                await ctx.send("Cancelled image change :ok_hand:")
            if usermsg.attachments:
                newdata = {"$set":{
                    "image": usermsg.attachments[0].url
                }}
                db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed welcome image",
                description="New welcome image is:",
                color=var.C_GREEN
                ).set_image(url=usermsg.attachments[0].url)
                )
            elif usermsg.content.startswith("http"):
                newdata = {"$set":{
                    "image": usermsg.content
                }}
                db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed welcome image",
                description="New welcome image is:",
                color=var.C_GREEN
                ).set_image(url=usermsg.content)
                )
            else:
                await ctx.send("Invalid image, try again")
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}** you took too long to enter your welcome image, try again maybe?")
                

    @commands.command()
    @has_command_permission()
    async def welcomerole(self, ctx, role:discord.Role=None):
        GuildDoc = db.WELCOME.find_one({"_id":ctx.guild.id})
        if role is not None:
            rolelist = GuildDoc.get("assignroles")
            updatedlist = rolelist.copy()
            updatedlist.append(role.id)

            newdata = {"$set":{
                "assignroles":updatedlist
            }}
            db.WELCOME.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    title="Successfully added auto assign role",
                    description=f"{var.E_ACCEPT} Users will be automatically given {role.mention} when they join",
                    color=var.C_GREEN)
            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the role",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}welcomerole <role>`"
            ).set_footer(text="For role either role ID or role mention can be used")
            )


    @commands.command()
    @has_command_permission()
    async def welcomereset(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "message": None,
            "welcomegreeting": "Hope you enjoy your stay here ✨",
            "image": "https://image.freepik.com/free-vector/welcome-sign-neon-light_110464-147.jpg",
            "assignroles": []
        }}
        db.WELCOME.update_one(GuildDoc, newdata)
        await ctx.send(embed=discord.Embed(
        description=f"{var.E_ACCEPT} Successfully changed the welcome embed back to the default one",
        color=var.C_GREEN)
        )


    @commands.Cog.listener()
    async def on_member_join(self, member):
        GuildVerifyDoc = db.VERIFY.find_one({"_id": member.guild.id})
        GuildWelcomeDoc = db.WELCOME.find_one({"_id": member.guild.id})

        #Verification Stuff
        if db.PLUGINS.find_one({"_id": member.guild.id}).get("Verification") == True:
            roleid = GuildVerifyDoc.get("roleid")
            unverifiedrole = member.guild.get_role(roleid)

            await member.add_roles(unverifiedrole)

        #Main Welcome stuff
        servers = []
        for i in db.PLUGINS.find({"Welcome": True}):
            servers.append(i.get("_id"))

        if member.guild.id in servers:
            channel = self.bot.get_channel(GuildWelcomeDoc.get("channelid"))

            def getcontent():
                if GuildWelcomeDoc.get("message") is None:
                    content = greeting(member.mention)
                else:
                    content = GuildWelcomeDoc.get("message")
                return content

            embed = discord.Embed(
            title="Welcome to the server!",
            description=GuildWelcomeDoc.get("greeting"),
            color=discord.Colour.random()
            ).set_image(url=GuildWelcomeDoc.get("image"))

            await channel.send(content=getcontent(), embed=embed)

            autoroles = GuildWelcomeDoc.get("assignroles")
            if autoroles != []:
                for i in autoroles:
                    autorole = member.guild.get_role(i)
                    await member.add_roles(autorole)


def setup(bot):
    bot.add_cog(Welcome(bot))
