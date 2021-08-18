import asyncio
import discord
from discord.ext import commands
import variables as var
import database as db
from functions import get_prefix
from greetings import greeting
from ext.permissions import has_command_permission

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Welcome"):
            return True
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    #This command isn't really used, just putted this here to invoke on first welcome plugin enable
    @commands.command()
    @has_command_permission()
    async def welcomesetup(self, ctx):
        await ctx.send("Now send the channel where you want me to send welcome message.")

        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id
        usermsg = await self.bot.wait_for('message', check=messagecheck)

        try:
            chid = int(usermsg.content.strip("<>#"))
        except:
            await db.PLUGINS.update_one(db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set":{"Welcome":False}})
            return await ctx.send(embed=discord.Embed(
                        title="Invalid Channel",
                        description="🚫 I was not able to find the channel which you entered. The plugin has been disabled, try again",
                        color=var.C_RED
                    ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
                    )
            
        await db.WELCOME.insert_one({

            "_id":ctx.guild.id,
            "channelid":chid,
            "message": None,
            "greeting": "Hope you enjoy your stay here ✨",
            "image": "https://cdn.discordapp.com/attachments/843519647055609856/864924991597314078/Frame_1.png",
            "assignroles": []
        })
        successembed = discord.Embed(
        title="Welcome greeting successfully setted up",
        description=f"{var.E_ACCEPT} New members will now be greeted in {self.bot.get_channel(chid).mention}!",
        color=var.C_GREEN
        ).add_field(name="To configure further", value=f"`{await get_prefix(ctx)}help welcome`")
        
        await ctx.send(embed=successembed)        


    @commands.command()
    @has_command_permission()
    async def wcard(self, ctx):
        GuildDoc = await db.WELCOME.find_one({"_id": ctx.guild.id})
        
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
    async def wchannel(self, ctx, channel:discord.TextChannel=None):
        GuildDoc = await db.WELCOME.find_one({"_id":ctx.guild.id})

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
            ).add_field(name="Format", value=f"`{await get_prefix(ctx)}wchannel <#channel>`"))


    @commands.command()
    @has_command_permission()
    async def wmessage(self, ctx):
        GuildDoc = await db.WELCOME.find_one({"_id": ctx.guild.id})

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
                await db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed the welcome message!",
                description=f"The new welcome message is:\n**{usermsg.content}**",
                color=var.C_GREEN)
                )
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}** you took too long to enter your message, try again maybe?")


    @commands.command()
    @has_command_permission()
    async def wgreeting(self, ctx):
        GuildDoc = await db.WELCOME.find_one({"_id": ctx.guild.id})

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
                await db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed the greeting message!",
                description=f"The new greeting message is:\n**{usermsg.content}**",
                color=var.C_GREEN)
                )
        except asyncio.TimeoutError:
            await ctx.send(f"**{ctx.author.name}** you took too long to enter your message, try again maybe?")


    @commands.command()
    @has_command_permission()
    async def wimage(self, ctx):
        GuildDoc = await db.WELCOME.find_one({"_id": ctx.guild.id})

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
                await db.WELCOME.update_one(GuildDoc, newdata)

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
                await db.WELCOME.update_one(GuildDoc, newdata)

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
    async def wrole(self, ctx, role:discord.Role=None):
        GuildDoc = await db.WELCOME.find_one({"_id":ctx.guild.id})
        if role is not None:
            rolelist = GuildDoc.get("assignroles")
            updatedlist = rolelist.copy()
            updatedlist.append(role.id)

            newdata = {"$set":{
                "assignroles":updatedlist
            }}
            await db.WELCOME.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    title="Successfully added auto assign role",
                    description=f"{var.E_ACCEPT} Users will be automatically given {role.mention} when they join",
                    color=var.C_GREEN)
            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the role",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{await get_prefix(ctx)}wrole <role>`"
            ).set_footer(text="For role either role ID or role mention can be used")
            )

    @commands.command()
    @has_command_permission()
    async def wbots(self, ctx):
        data = await db.WELCOME.find_one({"_id": ctx.guild.id})
        embed = discord.Embed(title="Greet bots")
        if data["greet_bots"]:
            embed.description=f"Currently, bots are greeted by me when they join.\nReact to the {var.E_DISABLE} emoji to disable me greeting them."
            embed.color=var.C_GREEN
        else:
            embed.description=f"Currently, bots are not greeted by me when they join.\n React to  the {var.E_ENABLE} emoji to enable me greeting them."
            embed.color=var.C_RED
        
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_DISABLE if data["greet_bots"] else var.E_ENABLE)

        def check(reaction, user):
            if str(reaction.emoji) in [var.E_DISABLE, var.E_ENABLE]:
                return user == ctx.author and reaction.message == botmsg

        await self.bot.wait_for("reaction_add", check=check, timeout=60)
        newdata = {"$set":{
            "greet_bots":False if data["greet_bots"] else True    
        
            }}
        await db.WELCOME.update_one(data, newdata)
        try:
            await botmsg.clear_reactions()
        except discord.Forbidden:
            pass
        embed.description= "Bots won't be greeted from now by me." if data["greet_bots"] else "Bots would be greeted from now by me."
        embed.color = var.C_RED if data["greet_bots"] else var.C_GREEN
        await botmsg.edit(embed=embed)


    @commands.command()
    @has_command_permission()
    async def wreset(self, ctx):
        GuildDoc = await db.WELCOME.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "message": None,
            "welcomegreeting": "Hope you enjoy your stay here ✨",
            "image": "https://cdn.discordapp.com/attachments/843519647055609856/864924991597314078/Frame_1.png",
            "assignroles": [],
            "greet_bots": True,
        }}
        await db.WELCOME.update_one(GuildDoc, newdata)
        await ctx.send(embed=discord.Embed(
        description=f"{var.E_ACCEPT} Successfully changed the welcome embed back to the default one",
        color=var.C_GREEN)
        )


    @commands.Cog.listener()
    async def on_member_join(self, member):

        welcome_guild_ids = [doc["_id"] async for doc in db.PLUGINS.find({"Welcome": True})]
        
        if member.guild.id in welcome_guild_ids:
            WelcomeDoc = await db.WELCOME.find_one({"_id": member.guild.id})
            if not WelcomeDoc["greet_bots"]:
                return
            channel = self.bot.get_channel(WelcomeDoc.get("channelid"))

            def getcontent():
                if WelcomeDoc.get("message") == None:
                    content = greeting(member.mention)
                else:
                    content = f"{member.mention} {WelcomeDoc.get('message')}"
                return content

            embed = discord.Embed(
            title="Welcome to the server!",
            description=WelcomeDoc.get("greeting"),
            color=discord.Colour.random()
            ).set_image(url=WelcomeDoc.get("image"))

            await channel.send(content=getcontent(), embed=embed)

            autoroles = WelcomeDoc["assignroles"]
            if autoroles != []:
                for i in autoroles:
                    autorole = member.guild.get_role(i)
                    await member.add_roles(autorole)


def setup(bot):
    bot.add_cog(Welcome(bot))
