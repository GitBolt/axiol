import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import check, Context
import variables as var
import database as db
from functions import getprefix


def user_or_admin(myid):
    async def predicate(ctx: Context):
        return ctx.author.id == myid or ctx.author.guild_permissions.administrator 
    return check(predicate)


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["plugin", "extensions", "extentions", "addons"])
    @user_or_admin(791950104680071188) #This me
    async def plugins(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id}, {"_id":False}) #Getting guild's plugin document and removing the ID
        enabled_amount = len([keys for keys, values in GuildDoc.items() if values == True])
        total_amount = len(GuildDoc)

        embed = discord.Embed(
        title="All available plugins",
        description="React to the respective emojis below to enable/disable them!",
        color=var.C_MAIN
        ).set_footer(text=f"{enabled_amount}/{total_amount} plugins are enabled in this server"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
        
        for i in GuildDoc:
            status = "Enabled" if GuildDoc.get(i) == True else "Disabled"
            embed.add_field(name=i, value=f"{var.DICT_PLUGINEMOJIS.get(i)} {status}", inline=False)

        botmsg = await ctx.send(embed=embed)
        for i in GuildDoc:
            await botmsg.add_reaction(var.DICT_PLUGINEMOJIS.get(i))
        
        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg

        def enablecheck(reaction, user):
            if str(reaction.emoji) == var.E_ENABLE:
                return user == ctx.author and reaction.message == enabledbotmsg

        def disablecheck(reaction, user):
            if str(reaction.emoji) == var.E_DISABLE:
                return user == ctx.author and reaction.message == enabledbotmsg

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=reactioncheck, timeout=60.0)
                GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
                if str(reaction.emoji) in var.DICT_PLUGINEMOJIS.values():
                    await botmsg.clear_reactions()
                    plugin_type = list(var.DICT_PLUGINEMOJIS.keys())[list(var.DICT_PLUGINEMOJIS.values()).index(str(reaction.emoji))]

                    embed = discord.Embed(
                    title=f"{plugin_type} Plugin",
                    )
                    if GuildDoc.get(plugin_type) == True:
                        embed.description=f"{var.E_ENABLE} {plugin_type} is currently enabled"
                        embed.color=var.C_GREEN
                        enabledbotmsg = await ctx.send(embed=embed)
                        await enabledbotmsg.add_reaction(var.E_DISABLE)

                        await self.bot.wait_for('reaction_add', check=disablecheck)
                        newdata = {"$set":{
                            plugin_type: False
                        }}
                        db.PLUGINS.update_one(GuildDoc, newdata)

                        embed.title=f"{plugin_type} disabled"
                        embed.description=f"{var.E_DISABLE} {plugin_type} extension has been disabled"
                        embed.color=var.C_RED
                        await enabledbotmsg.edit(embed=embed)
                        await enabledbotmsg.clear_reactions()

                    else:
                        embed.description=f"{var.E_DISABLE} {plugin_type} is currently disabled"
                        embed.color = var.C_RED
                        enabledbotmsg = await ctx.send(embed=embed)
                        await enabledbotmsg.add_reaction(var.E_ENABLE)

                        await self.bot.wait_for('reaction_add', check=enablecheck)
                        newdata = {"$set":{
                            plugin_type: True
                        }}
                        db.PLUGINS.update_one(GuildDoc, newdata)

                        embed.title=f"{plugin_type} enabled"
                        embed.description=f"{var.E_ENABLE} {plugin_type} extension has been enabled"
                        embed.color=var.C_GREEN
                        await enabledbotmsg.edit(embed=embed)
                        await enabledbotmsg.clear_reactions()

                        #Since welcome is not enabled by default ->
                        #The time plugin is enabled, there is no information avaialable in the db ->
                        #Hence we ask for the welcome channel and insert the data
                        if str(reaction.emoji) == "👋" and db.WELCOME.find_one({"_id": ctx.guild.id}) is None:

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
                                        description=f"{var.E_ERROR} I was not able to find the channel which you entered",
                                        color=var.C_RED
                                ).set_footer(text="You can either mention the channel (example: #general) or use the channel's id (example: 843516084266729515)")
                                )

                            db.WELCOME.insert_one({

                                "_id":ctx.guild.id,
                                "channelid":chid,
                                "greeting": "Hope you enjoy your stay here :)",
                                "image": "https://image.freepik.com/free-vector/welcome-sign-neon-light_110464-147.jpg",
                                "assignroles": []
                            })
                            successembed = discord.Embed(
                            title="Welcome greeting successfully setted up",
                            description=f"{var.E_ACCEPT} New members will now be greeted in {self.bot.get_channel(chid).mention}!",
                            color=var.C_GREEN
                            ).add_field(name="To configure further", value=f"`{getprefix(ctx)}help welcome`")
                            
                            await ctx.send(embed=successembed)
                    
                        #Same with verification
                        if str(reaction.emoji) =="✅" and db.VERIFY.find_one({"_id": ctx.guild.id}) is None:

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
                                ).add_field(name="Use existing", value=f"React to {var.E_ACCEPT}"
                                ).add_field(name="Create new", value=f"{var.E_CONTINUE}"
                                ).set_footer(text="Using the second option, I will create a new 'Not Verified' role however the existing 'Not Verified' role would still be there (in case you have some settings in it) don't get confused between two!")
                                )
                                await alertbotmsg.add_reaction(var.E_ACCEPT)
                                await alertbotmsg.add_reaction(var.E_CONTINUE)

                                def alertreactioncheck(reaction, user):
                                    return user == ctx.author and reaction.message == alertbotmsg
                                reaction, user = await self.bot.wait_for("reaction_add", check=alertreactioncheck)

                                if str(reaction.emoji == var.E_ACCEPT):
                                    NVerified = discord.utils.get(ctx.guild.roles, name="Not Verified")
                                    await botmsg.clear_reactions()
                                    db.VERIFY.insert_one({
                                        
                                        "_id":ctx.guild.id,
                                        "type": "command",
                                        "channel": chid, 
                                        "roleid": NVerified.id,
                                        "assignrole": None
                                    })

                                elif str(reaction.emoji) == var.E_CONTINUE:
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

            except asyncio.TimeoutError:
                await botmsg.clear_reactions()
                


    @commands.command()
    @user_or_admin(791950104680071188) #This me
    async def prefix(self, ctx):
        embed = discord.Embed(
        title="Prefix :D that's the way you control me aye!",
        description=f"The prefix for this server is\n```{getprefix(ctx)}```\nWanna change it? React to the {var.E_SETTINGS} emoji below!",
        color=var.C_MAIN
        )
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_SETTINGS)

        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg

        await self.bot.wait_for('reaction_add', check=reactioncheck)
        await ctx.send(embed=discord.Embed(
                    description="Next message which you will send will become the prefix :eyes:\n"+
                    f"To cancel it enter\n```{getprefix(ctx)}cancel```",
                    color=var.C_ORANGE
                    ).set_footer(text="Automatic cancellation after 1 minute")
                    )
        await botmsg.clear_reactions()

        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        try:
            usermsg = await self.bot.wait_for('message', check=messagecheck, timeout=60.0)

            if usermsg.content == getprefix(ctx)+"cancel": #Cancel
                await ctx.send("Cancelled prefix change :ok_hand:")
                
            elif usermsg.content == var.DEFAULT_PREFIX: #Same prefixes so deleting the doc
                db.PREFIXES.delete_one({"_id": ctx.guild.id})
                await ctx.send(f"Changed your prefix to the default one\n```{var.DEFAULT_PREFIX}```")

            elif getprefix(ctx) == var.DEFAULT_PREFIX: #If current prefix is default then insert new
                db.PREFIXES.insert_one({
                    "_id": ctx.guild.id, 
                    "prefix": usermsg.content
                    })
                await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

            else: #Exists so just update it
                GuildDoc = db.PREFIXES.find_one({"_id": usermsg.guild.id})
                newdata = {"$set": {
                    "prefix": usermsg.content
                    }}
                
                db.PREFIXES.update_one(GuildDoc, newdata)
                await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to enter your new prefix {ctx.author.mention} ;-;")


def setup(bot):
    bot.add_cog(Settings(bot))