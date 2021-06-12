import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix
import random


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Verification plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.command()
    async def verifysetup(self, ctx):
        embed = discord.Embed(
        title="Send the verify channel",
        description="Since this is the first time this plugin is being enabled, I need to know where I am supposed to verify new members :D",
        color=var.C_BLUE
        ).set_footer(text="The next message which you will send will become the verify channel, make sure that the channel/channelID is valid other wise this won't work")

        botmsg = await ctx.send(embed=embed)

        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        usermsg = await self.bot.wait_for('message', check=messagecheck)
        try:
            chid = int(usermsg.content.strip("<>#"))
        except:
            await ctx.send(embed=discord.Embed(
                    title="Invalid Channel",
                    description=f"{var.E_ERROR} I was not able to find the channel which you entered",
                    color=var.C_RED
            ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
            )

        if discord.utils.get(ctx.guild.roles, name="Not Verified"):
            alertbotmsg = await ctx.send(embed=discord.Embed(
                        title="**Not Verified** role found",
                        description="I have found a role named 'Not Verified' in this guild, do you want me to use this existing one or let me create a new one with proper permissions?",
                        color=var.C_BLUE
            ).add_field(name="Reuse", value=f"{var.E_RECYCLE} Use the existing role without creating any new", inline=False
            ).add_field(name="Create", value=f"{var.E_ACCEPT} Create a new one and use it while keeping the existing one", inline=False
            ).add_field(name="Update", value=f"{var.E_CONTINUE} Replace a new one with the existing one", inline=False
            ))
            await alertbotmsg.add_reaction(var.E_RECYCLE)
            await alertbotmsg.add_reaction(var.E_ACCEPT)
            await alertbotmsg.add_reaction(var.E_CONTINUE)

            def alertreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == alertbotmsg
            reaction, user = await self.bot.wait_for("reaction_add", check=alertreactioncheck)
            await alertbotmsg.clear_reactions()
            ExistingNVerified = discord.utils.get(ctx.guild.roles, name="Not Verified")

            if str(reaction.emoji) == var.E_RECYCLE:
                await botmsg.clear_reactions()
                db.VERIFY.insert_one({
                    
                    "_id":ctx.guild.id,
                    "type": "command",
                    "channel": chid, 
                    "roleid": ExistingNVerified.id,
                    "assignrole": None
                })

            if str(reaction.emoji) == var.E_CONTINUE: 
                await ExistingNVerified.delete()

            if str(reaction.emoji) == var.E_ACCEPT or str(reaction.emoji) == var.E_CONTINUE: #This will run the statement two times for continue, first one to delete it
                NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                embed.title="Processing..."
                embed.description="Setting up everything, just a second"
                embed.set_footer(text="Creating the 'Not Verified' role and setting up proper permissions")
                await botmsg.edit(embed=embed)
                for i in ctx.guild.text_channels:
                    await i.set_permissions(NVerified, view_channel=False)
                await self.bot.get_channel(chid).set_permissions(NVerified, view_channel=True, read_message_history=True)
                await self.bot.get_channel(chid).set_permissions(ctx.guild.default_role, view_channel=False)

                db.VERIFY.insert_one({
                    
                    "_id":ctx.guild.id,
                    "type": "command",
                    "channel": chid, 
                    "roleid": NVerified.id,
                    "assignrole": None
                })
                
        else:
            NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
            embed.title="Processing..."
            embed.description="Setting up everything, just a second"
            embed.set_footer(text="Creating the 'Not Verified' role and setting up proper permissions")
            await botmsg.edit(embed=embed)
            for i in ctx.guild.text_channels:
                await i.set_permissions(NVerified, view_channel=False)
            await self.bot.get_channel(chid).set_permissions(NVerified, view_channel=True, read_message_history=True)
            await self.bot.get_channel(chid).set_permissions(ctx.guild.default_role, view_channel=False)

            db.VERIFY.insert_one({
                
                "_id":ctx.guild.id,
                "type": "command",
                "channel": chid, 
                "roleid": NVerified.id,
                "assignrole": None
            })

        successembed = discord.Embed(
        title="Verification successfully setted up",
        description=f"{var.E_ACCEPT} New members would need to verify in {self.bot.get_channel(chid).mention} to access other channels!",
        color=var.C_GREEN
        ).add_field(name="To configure further", value=f"`{getprefix(ctx)}help verification`"
        ).set_footer(text="Default verification type is command")
        
        await ctx.send(embed=successembed)


    @commands.command()
    async def verifyinfo(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        verifytype = GuildDoc.get("type")
        if verifytype == "command":

            embed = discord.Embed(
            title=f"This server has Command verification",
            description="This is a basic type of verification where users enter a command in the verification channel and they are quickly verified and given access to other channels, this can be used to verify people and low-medium level raid/spam bot.",
            color=var.C_TEAL
            )
        else:
            embed = discord.Embed(
            title="This server has Bot verification",
            description="This is a slightly more advanced bot captcha like verification most suitable to bypass advance bot raids, after users enter the command a captcha image is sent in the channel with distorted text (good enough for a human to read) and if the users enter the code correctly they are verified. The image lasts only for 15 seconds, entering the command again will send another new image.",
            color=var.C_TEAL
            )
        embed.add_field(name="Verification Channel", value=self.bot.get_channel(GuildDoc.get("channel")).mention)
        embed.add_field(name="Not Verified Role", value=ctx.guild.get_role(GuildDoc.get("roleid")).mention)
        
        if GuildDoc.get("assignrole") is None:
            role = None
        else:
            role = ctx.guild.get_role(GuildDoc.get("assignrole")).mention

        embed.add_field(name="Verified Role", value=role)
        await ctx.send(embed=embed)



    @commands.command()
    async def verifychannel(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = db.VERIFY.find_one({"_id": ctx.guild.id})  
            NVerified = ctx.guild.get_role(GuildDoc.get("roleid"))
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(ctx.guild.default_role, view_channel=True) 
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(NVerified, view_channel=False)
            newdata = {"$set":{
                "channel": channel.id
            }}
            db.VERIFY.update_one(GuildDoc, newdata)
            await self.bot.get_channel(channel.id).set_permissions(NVerified, view_channel=True)
            
            embed = discord.Embed(
            title="Successfully changed the verification channel",
            description=f"Members will now be verified in {channel.mention}!",
            color=var.C_BLUE
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the verification channel to change it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}verifychannel <#channel>`"))



    @commands.command()
    async def verifyswitch(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        if GuildDoc.get("type") == "command":
            newdata = {"$set":{
                "type": "bot"
            }}
        else:
            newdata = {"$set":{
                "type": "command"
            }}
        db.VERIFY.update_one(GuildDoc, newdata)
        await ctx.send(embed=discord.Embed(
                    title="Switched to " + newdata.get("$set").get("type") + " verification",
                    description="Use the command again to switch to the other method",
                    color=var.C_GREEN)
        )
    

    @commands.command()
    async def verifyrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = db.VERIFY.find_one({"_id": ctx.guild.id})
            newdata = {'$set':{
                "assignrole": role.id
            }}
            db.VERIFY.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Successfully added {role.mention}",
                    color=var.C_GREEN
            ).set_footer(text="Now users who will successfully verify will get this role")
            )
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the role too!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}verifyrole <role>`"
            ).set_footer(text="For role either role mention or ID can be used (to not disturb anyone having the role)")
            )


    @commands.command()
    async def verifyroleremove(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("assignrole") is not None:
            role = ctx.guild.get_role(GuildDoc.get("assignrole"))

            newdata = {"$set":{
                "assignrole": None
            }}
            db.VERIFY.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Removed {role.mention} from verified role",
                    color=var.C_GREEN
            ).set_footer(text="Now users who verify successfully won't get this role")
            )
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the role too!",
            color=var.C_RED
             ).add_field(name="Format", value=f"`{getprefix(ctx)}verifyroleremove <role>`"
            ).set_footer(text="For role either role mention or ID can be used (to not disturb anyone having the role)")
            )


    @commands.command()
    async def verifyremove(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        db.VERIFY.delete_one(GuildDoc)
        await discord.utils.get(ctx.guild.roles, name="Not Verified").delete()
        GuildPluginDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "Verification": False
        }}
        db.PLUGINS.update_one(GuildPluginDoc, newdata)
        await ctx.send("Successfully removed verification from this server!")



    @commands.command(aliases=["verifyme"])
    async def verify(self, ctx):
        if ctx.channel.id in db.VERIFY.distinct("channel"): #Verify channel IDs
            assignrole = db.VERIFY.find_one({"_id": ctx.guild.id}).get("assignrole")

            await ctx.message.delete()
            if db.VERIFY.find_one({"_id":ctx.guild.id}).get("type") == "command": #Command verification
                roleid = db.VERIFY.find_one({"_id": ctx.guild.id}).get("roleid")
                role = ctx.guild.get_role(roleid)

                await ctx.send(f"Verification successful {var.E_ACCEPT} - **{ctx.author}**", delete_after=1)
                await ctx.author.remove_roles(role)
                if assignrole is not None:
                    await ctx.author.add_roles(ctx.guild.get_role(assignrole))

            else: #Bot verification
                Image = random.choice([
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170831586787398/7h3fpaw1.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170832744415283/bs4hm1gd.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170834484789309/hdmxe425.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170834514018304/kp6d1vs9.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170835957383189/jd3573vq.png',
                        ])    

                embed = discord.Embed(
                    title="Beep Bop,  are you a bot?",
                    description = 'Enter the text given in the image below to verify yourself',
                    colour = var.C_MAIN
                    ).set_image(url=Image
                    ).set_footer(text='You have 15 seconds to enter the text, if you failed to enter it in time then type the command again.'
                    )
                botmsg = await ctx.send(embed=embed, delete_after=15.0)

                def codecheck(message):
                    return message.author == ctx.author and message.channel.id == ctx.channel.id
                
                usermsg = await self.bot.wait_for('message', check=codecheck, timeout=15.0)

                #ayo bots aren't this smart
                code = embed.image.url[77:-4]
                if usermsg.content == code:
                    roleid = db.VERIFY.find_one({"_id": ctx.guild.id}).get("roleid")
                    role = ctx.guild.get_role(roleid)
                    await ctx.send(f"Verification successful {var.E_ACCEPT} - **{ctx.author}**", delete_after=1)
                    await ctx.author.remove_roles(role)
                    if assignrole is not None:
                        await ctx.author.add_roles(ctx.guild.get_role(assignrole))
                    await botmsg.delete()
                    await usermsg.delete()
                else:
                    await ctx.send("Wrong, try again", delete_after=1)
                    await botmsg.delete()
                    await usermsg.delete()



def setup(bot):
    bot.add_cog(Verification(bot))
