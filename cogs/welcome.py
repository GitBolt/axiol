import asyncio
import discord
from discord.ext import commands
import utils.variables as var
import utils.database as db
from utils.functions import getprefix
from utils.greetings import greeting


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


    @commands.command()
    async def welcomecard(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})
        
        embed = discord.Embed(
        title="Welcome to the server!",
        description=GuildDoc.get("greeting"),
        color=discord.Colour.random()
        ).set_image(url=GuildDoc.get("image")
        )
        await ctx.send(content=greeting(ctx.author.mention), embed=embed)



    @commands.command()
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
            description=f"{var.E_ERROR} You need to define the greeting channel to change it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}welcomechannel #channel`"))



    @commands.command()
    async def welcomemessage(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})

        await ctx.send(embed=discord.Embed(
                    tite="Send a message to make it the message",
                    description="The next message which you will send will become the embed description!",
                    color=var.C_BLUE
        ).add_field(name="Cancel", value=f"Type `cancel` to cancel this")
        )

        def msgcheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
            if usermsg.content == "cancel" or "`cancel`":
                await ctx.send("Cancelled welcome message change :ok_hand:")
            else:
                newdata = {"$set":{
                    "greeting": usermsg.content
                }}
                db.WELCOME.update_one(GuildDoc, newdata)

                await ctx.send(embed=discord.Embed(
                title=f"{var.E_ACCEPT} Successfully changed the greeting message!",
                description=f"The new greeting message is:\n**{usermsg.content}**",
                color=var.C_GREEN)
                )
        except asyncio.TimeoutError:
            await ctx.send("You took too long to enter your message ;-;")



    @commands.command()
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
            if usermsg.content == "cancel" or "`cancel`":
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
                await ctx.send("Invalid image")
        except asyncio.TimeoutError:
            await ctx.send("You took too long to send the new image ;-;")
                
                

    @commands.command()
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
            description=f"{var.E_ERROR} You need to define the role",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}welcomerole <role>`"
            ).set_footer(text="For role either role ID or role mention can be used")
            )



    @commands.command()
    async def welcomereset(self, ctx):
        GuildDoc = db.WELCOME.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "greeting": "Hope you enjoy your stay here :)",
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
        if GuildVerifyDoc is not None:
            roleid = GuildVerifyDoc.get("roleid")
            role = member.guild.get_role(roleid)
            await member.add_roles(role)


        #Welcome stuff
        servers = []
        for i in db.PLUGINS.find({"Welcome": True}):
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