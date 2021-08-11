import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import check, Context
import variables as var
import database as db
from ext.buttons import Disable, Plugins, Enable
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
        description="Click on the respective button to enable/disable the plugin",
        color=var.C_MAIN
        ).set_footer(text=f"{enabled_amount}/{total_amount} plugins are enabled in this server"
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")
        
        for i in GuildDoc:
            status = "Enabled" if GuildDoc.get(i) else "Disabled"
            embed.add_field(name=i, value=f"{var.DICT_PLUGINEMOJIS.get(i)} {status}", inline=False)

        view = Plugins(self.bot, ctx, embed)
        view.message = await ctx.send(embed=embed, view=view)
        await view.wait()

        toggle_view = Disable(ctx) if GuildDoc[view.plugin] else Enable(ctx)
        do_this = "Enable" if toggle_view.type else "Disable"
        embed = discord.Embed(title=view.plugin + " plugin", 
                        description=f"{do_this} the plugin by clicking on the button", 
                    color=var.C_BLUE
                )
        toggle_view.message = await ctx.send(embed=embed, view=toggle_view)
        await toggle_view.wait()

        if toggle_view.value and toggle_view.type:
            newdata = {"$set":{
                view.plugin: True
            }}
            db.PLUGINS.update_one(GuildDoc, newdata)

            embed.description=f"{var.E_ENABLE} {view.plugin} plugin has been enabled"
            embed.color=var.C_GREEN
            await toggle_view.message.edit(embed=embed)
        if toggle_view.value and not toggle_view.type:
            newdata = {"$set":{
                view.plugin: False
            }}
            db.PLUGINS.update_one(GuildDoc, newdata)
            
            embed.description=f"{var.E_DISABLE} {view.plugin} plugin has been disabled"
            embed.color=var.C_RED
            await toggle_view.message.edit(embed=embed, view=None)

            #Since welcome and verification are not enabled by default
            #The time plugin is enabled, there is no information available in the db
            #Hence we ask for the channel and insert the data
            #With autmod and leveling we just insert the default configs
            if view.plugin == "Welcome" and db.WELCOME.find_one({"_id": ctx.guild.id}) is None:
                await ctx.invoke(self.bot.get_command('welcomesetup'))
        
            if view.plugin == "Verification" and db.VERIFY.find_one({"_id": ctx.guild.id}) is None:
                await ctx.invoke(self.bot.get_command('verifysetup'))

            if view.plugin == "Karma" and str(ctx.guild.id) not in db.KARMADATBASE.list_collection_names():
                GuildDoc = db.KARMADATBASE.create_collection(str(ctx.guild.id))
                GuildDoc.insert_one({
                    "_id": 0,
                    "blacklists": [],
                    })   

            if view.plugin == "Leveling" and str(ctx.guild.id) not in db.LEVELDATABASE.list_collection_names():
                GuildDoc = db.LEVELDATABASE.create_collection(str(ctx.guild.id))
                GuildDoc.insert_one({

                    "_id": 0,
                    "xprange": [15, 25],
                    "alertchannel": None,
                    "blacklistedchannels": [],
                    "alerts": True,
                    "rewards": {}
                    })  

            if view.plugin == "AutoMod" and db.AUTOMOD.find_one({"_id":ctx.guild.id}) is None:
                db.AUTOMOD.insert_one({
                    "_id": ctx.guild.id,
                    "BadWords":{
                        "status": True,
                        "words": ["fuck", "bitch", "porn", "slut", "asshole"],
                        "response": "You aren't allowed to say that!"
                    },
                    "Invites": {
                        "status": True,
                        "response": "You can't send invites here!"
                    },
                    "Links": {
                        "status": True,
                        "response": "You can't send links here!"
                    },
                    "Mentions": {
                        "status": False,
                        "response": "You can't mention so many people!",
                        "amount": 5
                    },
                    "Settings": {
                        "ignorebots": False,
                        "blacklists": [],
                        "modroles": []
                    }
                })         


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
        try:
            await botmsg.clear_reactions()
        except discord.Forbidden:
            pass

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