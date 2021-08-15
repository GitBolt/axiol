import os
import random
import asyncio
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import database as db
import variables as var
from functions import get_prefix, get_code
from ext.permissions import has_command_permission

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification"):
            return True
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
            ch = self.bot.get_channel(int(usermsg.content.strip("<>#")))
        except:
            await db.PLUGINS.update_one(await db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set":{"Welcome":False}})
            return await ctx.send(embed=discord.Embed(
                    title="Invalid Channel",
                    description="🚫 I was not able to find the channel which you entered",
                    color=var.C_RED
            ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
            )

        async def setup():
            try:    
                NVerified = await ctx.guild.create_role(name="Not Verified", colour=discord.Colour(0xa8a8a8))
                embed.title="Processing..."
                embed.description="Setting up everything, just a second"
                embed.set_footer(text="Creating the 'Not Verified' role and setting up proper permissions")
                await botmsg.edit(embed=embed)
                try:
                    for i in ctx.guild.text_channels:
                        try:
                            await i.set_permissions(NVerified, view_channel=False)
                        except discord.Forbidden:
                            await ctx.send(embed=discord.Embed(
                                        description=f"Skipping {i.mention} since I don't have access to that channel",
                                        color=var.C_ORANGE
                            ))
                    await ch.set_permissions(NVerified, view_channel=True, read_message_history=True)
                    await ch.set_permissions(self.bot.user, view_channel=True)
                    await ch.set_permissions(ctx.guild.default_role, view_channel=False)
                    
                    db.VERIFY.insert_one({
                        
                        "_id":ctx.guild.id,
                        "type": "command",
                        "channel": ch.id, 
                        "roleid": NVerified.id,
                        "assignrole": None
                    })

                    successembed = discord.Embed(
                    title="Verification successfully setted up",
                    description=f"{var.E_ACCEPT} New members would need to verify in {ch.mention} to access other channels!",
                    color=var.C_GREEN
                    ).add_field(name="To configure further", value=f"`{await get_prefix(ctx)}help verification`"
                    ).set_footr(text="Default verification type is command")
                    
                    await ctx.send(embed=successembed)

                except discord.Forbidden:
                    await db.PLUGINS.update_one(await db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set":{"Verification":False}})
                    await ctx.send(embed=discord.Embed(
                                title="Missing access",
                                description=f"I don't have access or change role permissions in {ch.mention} to make it a verification channel",
                                color=var.C_RED
                    ))

            except:
                await db.PLUGINS.update_one(await db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set":{"Verification":False}})
                await ctx.send(embed=discord.Embed(
                            title="Missing Permissions",
                            description="🚫 I don't have permissions to create and set permissions for roles",
                            color=var.C_RED
                ))

        if discord.utils.get(ctx.guild.roles, name="Not Verified"):
            alertbotmsg = await ctx.send(embed=discord.Embed(
                        title="**Not Verified** role found",
                        description="I have found a role named 'Not Verified' in this guild, do you want me to use this existing one or let me create a new one with proper permissions?",
                        color=var.C_BLUE
            ).add_field(name="Reuse", value=f"{var.E_RECYCLE} Use the existing role without creating any new", inline=False
            ).add_field(name="Create", value=f"{var.E_ACCEPT} Create a new one and use it while keeping the existing one", inline=False
            ).add_field(name="Update", value=f"{var.E_CONTINUE} Replace a new one with the existing one (Hence deleting the existing one)", inline=False
            ))
            await alertbotmsg.add_reaction(var.E_RECYCLE)
            await alertbotmsg.add_reaction(var.E_ACCEPT)
            await alertbotmsg.add_reaction(var.E_CONTINUE)

            def alertreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == alertbotmsg

            reaction, user = await self.bot.wait_for("reaction_add", check=alertreactioncheck)
            try:
                await alertbotmsg.clear_reactions()
            except:
                pass
            ExistingNVerified = discord.utils.get(ctx.guild.roles, name="Not Verified")

            if str(reaction.emoji) == var.E_RECYCLE:
                await db.VERIFY.insert_one({
                    
                    "_id":ctx.guild.id,
                    "type": "command",
                    "channel": ch.id, 
                    "roleid": ExistingNVerified.id,
                    "assignrole": None
                })
                successembed = discord.Embed(
                title="Verification successfully setted up",
                description=f"{var.E_ACCEPT} New members would need to verify in {ch.mention} to access other channels!",
                color=var.C_GREEN
                ).add_field(name="To configure further", value=f"`{await get_prefix(ctx)}help verification`"
                ).set_footer(text="Default verification type is command")
                
                await ctx.send(embed=successembed)
                
            if str(reaction.emoji) == var.E_CONTINUE: 
                try:
                    await ExistingNVerified.delete()
                except discord.Forbidden:
                    await db.PLUGINS.update_one(await db.PLUGINS.find_one({"_id": ctx.guild.id}), {"$set":{"Verification":False}})
                    await ctx.send(embed=discord.Embed(
                                title="Missing Permissions",
                                description="🚫 I don't have permissions to delete the existing role, due to this error verification plugin has been disabled again",
                                color=var.C_RED
                    ))
            if str(reaction.emoji) == var.E_CONTINUE or str(reaction.emoji) == var.E_ACCEPT:
                await setup()
        else:
            await setup()





    @commands.command()
    @has_command_permission()
    async def verifyinfo(self, ctx):
        GuildDoc = await db.VERIFY.find_one({"_id":ctx.guild.id})
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
    @has_command_permission()
    async def verifychannel(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = await db.VERIFY.find_one({"_id": ctx.guild.id})  
            NVerified = ctx.guild.get_role(GuildDoc.get("roleid"))
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(ctx.guild.default_role, view_channel=True) 
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(NVerified, view_channel=False)
            newdata = {"$set":{
                "channel": channel.id
            }}
            await db.VERIFY.update_one(GuildDoc, newdata)
            await self.bot.get_channel(channel.id).set_permissions(NVerified, view_channel=True)
            
            embed = discord.Embed(
            title="Successfully changed the verification channel",
            description=f"Members will now be verified in {channel.mention}!",
            color=var.C_BLUE
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the verification channel to change it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{await get_prefix(ctx)}verifychannel <#channel>`"))



    @commands.command()
    @has_command_permission()
    async def verifyswitch(self, ctx):
        GuildDoc = await db.VERIFY.find_one({"_id":ctx.guild.id})
        if GuildDoc.get("type") == "command":
            newdata = {"$set":{
                "type": "bot"
            }}
        else:
            newdata = {"$set":{
                "type": "command"
            }}
        await db.VERIFY.update_one(GuildDoc, newdata)
        await ctx.send(embed=discord.Embed(
                    title="Switched to " + newdata.get("$set").get("type") + " verification",
                    description="Use the command again to switch to the other method",
                    color=var.C_GREEN)
        )
    

    @commands.command()
    @has_command_permission()
    async def verifyrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = await db.VERIFY.find_one({"_id": ctx.guild.id})
            newdata = {'$set':{
                "assignrole": role.id
            }}
            await db.VERIFY.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Successfully added {role.mention}",
                    color=var.C_GREEN
            ).set_footer(text="Now users who will successfully verify will get this role")
            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the role too!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{await get_prefix(ctx)}verifyrole <role>`"
            ).set_footer(text="For role either role mention or ID can be used (to not disturb anyone having the role)")
            )


    @commands.command()
    @has_command_permission()
    async def verifyroleremove(self, ctx):
        GuildDoc = await db.VERIFY.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("assignrole") is not None:
            role = ctx.guild.get_role(GuildDoc.get("assignrole"))

            newdata = {"$set":{
                "assignrole": None
            }}
            await db.VERIFY.update_one(GuildDoc, newdata)
            await ctx.send(embed=discord.Embed(
                    description=f"{var.E_ACCEPT} Removed {role.mention} from verified role",
                    color=var.C_GREEN
            ).set_footer(text="Now users who verify successfully won't get this role")
            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the role too!",
            color=var.C_RED
             ).add_field(name="Format", value=f"`{await get_prefix(ctx)}verifyroleremove <role>`"
            ).set_footer(text="For role either role mention or ID can be used (to not disturb anyone having the role)")
            )


    @commands.command()
    @has_command_permission()
    async def verifyremove(self, ctx):
        GuildDoc = await db.VERIFY.find_one({"_id":ctx.guild.id})
        await db.VERIFY.delete_one(GuildDoc)
        await discord.utils.get(ctx.guild.roles, name="Not Verified").delete()
        GuildPluginDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "Verification": False
        }}
        await db.PLUGINS.update_one(GuildPluginDoc, newdata)
        await ctx.send("Successfully removed verification from this server!")


    @staticmethod
    async def create_board():
        code = await get_code
        image = Image.open(os.path.join(os.getcwd(),("resources/backgrounds/verification_board.png")))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(os.getcwd(),("resources/fonts/Poppins-Medium.ttf")), 80)
        draw.text((810, 55), code ,(184,184,184),font=font)
        return image, code

    @commands.command(aliases=["verifyme"])
    async def verify(self, ctx):
        if ctx.channel.id in await db.VERIFY.distinct("channel"): #Verify channel IDs
            VerifyDoc = await db.VERIFY.find_one({"_id":ctx.guild.id})

            if VerifyDoc["type"] == "command": #Command based verification
                role_id = VerifyDoc["roleid"]
                role = ctx.guild.get_role(role_id)

                await ctx.send(f"{var.E_ACCEPT}  Verification successful **```{ctx.author}```**", delete_after=1)
                await ctx.author.remove_roles(role)
                if VerifyDoc["assignrole"] is not None:
                    await ctx.author.add_roles(ctx.guild.get_role(VerifyDoc["assignrole"]))

            else: #Bot verification

                #Lookin epic innit bruv?
                Images = {
                        'https://cdn.discordapp.com/attachments/865444983762452520/876497365891178546/axiol_verification.png': "7h3fpaw1",
                        'https://cdn.discordapp.com/attachments/865444983762452520/876497364779692072/axiol_verification.png.png': "bs4hm1gd",
                        'https://cdn.discordapp.com/attachments/865444983762452520/876497363387187240/axiol_verification.png.png.png': "kp6d1vs9",
                        'https://cdn.discordapp.com/attachments/865444983762452520/876497360224669796/axiol_verification.png.png.png.png': "hmxe425",
                        'https://cdn.discordapp.com/attachments/865444983762452520/876497358681149470/axiol_verification.png.png.png.png.png': "jd3573vq",
                    }       

                choice = random.choice(list(Images))
                code = Images[choice]

                embed = discord.Embed(
                    title="Beep Bop,  are you a bot?",
                    description = 'Enter the text given in the image below to verify yourself',
                    colour = var.C_MAIN
                    ).set_image(url=choice
                    ).set_footer(text='You have 20 seconds to enter the text, if you failed to enter it in time then type the command again.'
                    )
                botmsg = await ctx.send(embed=embed, delete_after=20.0)

                def codecheck(message):
                    return message.author == ctx.author and message.channel.id == ctx.channel.id
                
                try:
                    usermsg = await self.bot.wait_for('message', check=codecheck, timeout=20.0)

                    if usermsg.content == code:
                        role_id = VerifyDoc["roleid"]
                        role = ctx.guild.get_role(role_id)
                        await ctx.send(f"{var.E_ACCEPT}  Verification successful **```{ctx.author}```**", delete_after=1)
                        await ctx.author.remove_roles(role)
                        if VerifyDoc["assignrole"] is not None:
                            await ctx.author.add_roles(ctx.guild.get_role(VerifyDoc["assignrole"]))
                        await botmsg.delete()
                    else:
                        await ctx.send("Wrong, try again", delete_after=1)
                        await botmsg.delete()
                except asyncio.TimeoutError:
                    pass


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        PluginDoc = await db.PLUGINS.find_one({"_id":message.guild.id})
        if PluginDoc["Verification"]:
            GuildVerifyDoc = await db.VERIFY.find_one({"_id": message.guild.id})
            if GuildVerifyDoc is None:
                print(f"First time verification being enabled {message.guild.name}")
            else:
                if (message.channel.id == GuildVerifyDoc["channel"] and 
                    message.author != self.bot.user):
                    
                    await message.delete()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        VerifyDoc = await db.VERIFY.find_one({"_id": member.guild.id})
        PluginDoc = await db.PLUGINS.find_one({"_id": member.guild.id})

        if PluginDoc["Verification"]:
            roleid = VerifyDoc["roleid"]
            unverifiedrole = member.guild.get_role(roleid)

            await member.add_roles(unverifiedrole)
            
def setup(bot):
    bot.add_cog(Verification(bot))