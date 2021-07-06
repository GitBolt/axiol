import re
import discord
from discord.ext import commands
import database as db
import variables as var
from functions import getprefix


async def manage_filter(self, filtername, embed, GuildDoc, ctx): 
    if GuildDoc[filtername]["status"]:
        embed.description = f"{var.E_ENABLE} This Auto-Moderation filter is currently enabled"
        embed.color = var.C_GREEN
        if filtername == "BadWords":
            embed.add_field(name=f"{getprefix(ctx)}addbadword `<word>`", value="Adds a word to ban word list", inline=False)
        if filtername == "Mentions":
            embed.add_field(name=f"{getprefix(ctx)}mentionamount `<amount>`", value="Change the mention amount to delete, by default it's 5", inline=False)

        embed.add_field(name="Response", value=f"React to {var.E_SETTINGS}")
        embed.add_field(name="Disable", value=f"React to {var.E_DISABLE}")
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_SETTINGS)
        await botmsg.add_reaction(var.E_DISABLE)

        def reactioncheck(reaction, user):
            if str(reaction.emoji) in [var.E_DISABLE, var.E_SETTINGS]:
                return user == ctx.author and reaction.message == botmsg
        
        reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
        if str(reaction.emoji) == var.E_DISABLE:
            currentdata = GuildDoc[filtername]
            newdict = currentdata.copy()
            newdict["status"] = False

            newdata = {"$set":{
                filtername : newdict
            }}
            db.AUTOMODERATION.update_one(GuildDoc, newdata)
            embed.title=f"{filtername} filter disabled"
            embed.description=f"{var.E_DISABLE} This Auto-Moderation filter has been disabled"
            embed.color=var.C_RED
            embed.clear_fields()
            await botmsg.edit(embed=embed)
            try:
                await botmsg.clear_reactions()
            except discord.Forbidden:
                pass
        else:
            await ctx.send(f"The next message which you will send will become the **{filtername}** Auto-Moderation response!\nType `cancel` to stop this proccess")
            def messagecheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id            
            usermsg = await self.bot.wait_for("message", check=messagecheck)
            if usermsg.content in ["cancel", "`cancel`", "```cancel```"]:
                await ctx.send(f"Cancelled {filtername} response change")   
            else: 
                currentdata = GuildDoc[filtername]
                newdict = currentdata.copy()
                newdict["response"] = usermsg.content

                newdata = {"$set":{
                filtername: newdict
                }}
                db.AUTOMODERATION.update_one(GuildDoc, newdata) 
                await ctx.send(embed=discord.Embed(description=f"Successfully changed Auto-Moderation {filtername} response to \n**{usermsg.content}**", color=var.C_GREEN))  
    else:
        embed.description = f"{var.E_DISABLE} This Auto-Moderation filter is currently disabled"
        embed.color = var.C_RED
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_ENABLE)

        def enablecheck(reaction, user):
            if str(reaction.emoji) == var.E_ENABLE:
                return user == ctx.author and reaction.message == botmsg
                
        reaction, user = await self.bot.wait_for("reaction_add", check=enablecheck)

        currentdata = GuildDoc[filtername]
        newdict = currentdata.copy()
        newdict["status"] = True

        newdata = {"$set":{
            filtername: newdict
        }}
        db.AUTOMODERATION.update_one(GuildDoc, newdata)

        embed.title=f"{filtername} filter enabled"
        embed.description=f"{var.E_ENABLE} This Auto-Moderation filter has been enabled"
        embed.color=var.C_GREEN
        await botmsg.edit(embed=embed)
        try:
            await botmsg.clear_reactions()
        except discord.Forbidden:
            pass


class AutoModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("AutoModeration") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Auto-Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["filter"])
    async def filters(self ,ctx):
        embed = discord.Embed(title="All Auto-Moderation filters", description="Use the subcommand to configure each filter seperately!", color=var.C_MAIN)
        embed.set_footer(text="The emoji after filter name is their status whether they are enabled or disabled")
        GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id}, {"_id":0, "IgnoreBots": 0})
        for i in GuildDoc:
            status = var.E_ENABLE if GuildDoc[i]["status"] == True else var.E_DISABLE
            embed.add_field(name=status + " " + i , value=f"{getprefix(ctx)}filters {i.lower()}", inline=False)
        
        await ctx.send(embed=embed)

            
    @filters.command()
    async def invites(self, ctx):
        GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Invites filter"
        )
        await manage_filter(self, "Invites", embed, GuildDoc, ctx)

    @filters.command()
    async def links(self, ctx):
        GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Links filter"
        )
        await manage_filter(self, "Links", embed, GuildDoc, ctx)

    @filters.command()
    async def badwords(self, ctx):
        GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="BadWords filter"
        )
        await manage_filter(self, "BadWords", embed, GuildDoc, ctx)

    @filters.command()
    async def mentions(self, ctx):
        GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Mentions filter"
        )
        await manage_filter(self, "Mentions", embed, GuildDoc, ctx)


    @commands.command()
    async def ignorebots(self, ctx):
        GuildDoc = db.AUTOMODERATION.find_one({"_id": ctx.guild.id})
        botstatus = True if GuildDoc["IgnoreBots"] else False
        if botstatus:
            db.AUTOMODERATION.update_one(GuildDoc, {"$set":{"IgnoreBots":False}})
            await ctx.send(embed=discord.Embed(
                description="Bots won't be ignored hence are immune to Auto-Moderation",
                color=var.C_GREEN
            ))
        else:
            db.AUTOMODERATION.update_one(GuildDoc, {"$set":{"IgnoreBots":True}})
            await ctx.send(embed=discord.Embed(
                description="Bots are now ignored hence will be affected by Auto-Moderation",
                color=var.C_GREEN
            ))

    @commands.command()
    async def mentionamount(self, ctx, amount:int=None):
        if amount is not None:
            GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id})
            db.AUTOMODERATION.update_one(GuildDoc, {"$set":{"Mentions.amount": amount}})
            await ctx.send(embed=discord.Embed(
                description=f"Successfully changed the amount of mentions to be deleted to **{amount}**",
                color=var.C_GREEN
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the amount too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}mentionamount <amount>```")
            )

    @commands.command()
    async def addbadword(self, ctx, word:str=None):
        if word is not None:
            GuildDoc = db.AUTOMODERATION.find_one({"_id":ctx.guild.id})
            currentlist = GuildDoc["BadWords"]["words"]
            newlist = currentlist.copy()
            newlist.append(word)
            db.AUTOMODERATION.update_one(GuildDoc, {"$set":{"BadWords.words": newlist}})
            await ctx.send(embed=discord.Embed(
                description=f"Successfully added the word **{word}** in badwords list",
                color=var.C_GREEN
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the word too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}addbadword <word>```")
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        GuildDoc = db.AUTOMODERATION.find_one({'_id': message.guild.id})
        if GuildDoc is not None and not message.author.bot and not GuildDoc["IgnoreBots"]:

            if GuildDoc["Links"]["status"]:
                regex = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if re.match(regex, message.content) is not None:
                    await message.delete()
                    res = GuildDoc["Links"]["response"]
                    await message.channel.send(f"{message.author.mention} {res}", delete_after=2)

            if GuildDoc["Invites"]["status"]:
                if "discord.gg/" in message.content:
                    await message.delete()
                    res = GuildDoc["Invites"]["response"]
                    await message.channel.send(f"{message.author.mention} {res}", delete_after=2)
            
            if GuildDoc["Mentions"]["status"]:
                amount = GuildDoc["Mentions"]["amount"]
                if len(message.mentions) >= amount:
                    await message.delete()
                    res = GuildDoc["Mentions"]["response"]
                    await message.channel.send(f"{message.author.mention} {res}", delete_after=2)
            
            if GuildDoc["BadWords"]["status"]:
                badwords = GuildDoc["BadWords"]["words"]
                if any(item in badwords for item in message.content.split(" ")):
                    await message.delete()
                    res = GuildDoc["BadWords"]["response"]
                    await message.channel.send(f"{message.author.mention} {res}", delete_after=2)            



def setup(bot):
    bot.add_cog(AutoModeration(bot))
