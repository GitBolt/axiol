import re
import discord
from discord.ext import commands
from discord.guild import Guild
import database as db
import variables as var
from functions import getprefix



async def manage_filter(self, filtername, embed, GuildDoc, ctx): 
    if GuildDoc[filtername]["status"]:
        embed.description = f"{var.E_ENABLE} This Auto-Moderation filter is currently enabled"
        embed.color = var.C_GREEN
        if filtername == "BadWords":
            embed.add_field(name=f"{getprefix(ctx)}addbadword `<word>`", value="Adds a word to bad word list", inline=False)
            embed.add_field(name=f"{getprefix(ctx)}removebadword `<word>`", value="Removes a word from bad word list", inline=False)
            embed.add_field(name=f"{getprefix(ctx)}allbadwords", value="Shows all bad words", inline=False)
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
            db.AUTOMOD.update_one(GuildDoc, newdata)
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
                db.AUTOMOD.update_one(GuildDoc, newdata) 
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
        db.AUTOMOD.update_one(GuildDoc, newdata)

        embed.title=f"{filtername} filter enabled"
        embed.description=f"{var.E_ENABLE} This Auto-Moderation filter has been enabled"
        embed.color=var.C_GREEN
        await botmsg.edit(embed=embed)
        try:
            await botmsg.clear_reactions()
        except discord.Forbidden:
            pass


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("AutoMod") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Auto-Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["filter"])
    async def filters(self ,ctx):
        embed = discord.Embed(title="All Auto-Moderation filters", description="Use the subcommand to configure each filter seperately!", color=var.C_MAIN)
        embed.set_footer(text="The emoji before filter name is their status whether they are enabled or disabled")
        GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0, "Settings": 0})
        for i in GuildDoc:
            status = var.E_ENABLE if GuildDoc[i]["status"] == True else var.E_DISABLE
            embed.add_field(name=status + " " + i , value=f"{getprefix(ctx)}filters {i.lower()}", inline=False)
        
        await ctx.send(embed=embed)

            
    @filters.command()
    async def invites(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Invites filter"
        )
        await manage_filter(self, "Invites", embed, GuildDoc, ctx)

    @filters.command()
    async def links(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Links filter"
        )
        await manage_filter(self, "Links", embed, GuildDoc, ctx)

    @filters.command()
    async def badwords(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="BadWords filter"
        )
        await manage_filter(self, "BadWords", embed, GuildDoc, ctx)

    @filters.command()
    async def mentions(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Mentions filter"
        )
        await manage_filter(self, "Mentions", embed, GuildDoc, ctx)


    @commands.command()
    async def addmodrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
            currentlist = GuildDoc["Settings"]["modroles"]
            newlist = currentlist.copy()
            if role.id not in currentlist:
                newlist.append(role.id)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.modroles": newlist}})
                await ctx.send(embed=discord.Embed(
                    title="Successfully added mod role",
                    description=f"{role.mention} is immune from auto moderation now!",
                    color=var.C_GREEN
                ))
            else:
                await ctx.send("This role is already a mod role")
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the role too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}addmodrole <role>```")
            )

    @commands.command()
    async def removemodrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
            currentlist = GuildDoc["Settings"]["modroles"]
            newlist = currentlist.copy()
            if role.id in currentlist:
                newlist.remove(role.id)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.modroles": newlist}})
                await ctx.send(embed=discord.Embed(
                    title="Successfully removed mod role",
                    description=f"{role.mention} is not immune from auto moderation now!",
                    color=var.C_GREEN
                ))
            else:
                await ctx.send("This role is not a mod role")
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the role too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}addmodrole <role>```")
            )


    @commands.command()
    async def allmodroles(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
        if GuildDoc is not None:
            embed = discord.Embed(title="Moderator roles", description="These roles are immune to auto-moderation by me!", color=var.C_MAIN)
            value = ""
            for i in GuildDoc["Settings"]["modroles"]:
                role = ctx.guild.get_role(i)
                value += f'{role.mention} '

            embed.add_field(name="Immune roles", value=value)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Auto moderation is not setted up yet")


    @commands.command()
    async def automodblacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None and channel.id not in GuildDoc["Settings"]["blacklists"]:
                currentlist = GuildDoc["Settings"]["blacklists"]
                newlist = currentlist.copy()
                newlist.append(channel.id)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.blacklists": newlist}})
                await ctx.send(embed=discord.Embed(
                    title="Successfully blacklisted",
                    description=f"{channel.mention} is immune from auto moderation now!",
                    color=var.C_GREEN
                ))
            else:
                await ctx.send("This channel is already blacklisted")
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the channel too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}automodblacklist <#channel>```")
            )

    @commands.command()
    async def automodwhitelist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None and channel.id in GuildDoc["Settings"]["blacklists"]:
                currentlist = GuildDoc["Settings"]["blacklists"]
                newlist = currentlist.copy()
                newlist.remove(channel.id)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.blacklists": newlist}})
                await ctx.send(embed=discord.Embed(
                    title="Successfully whitelisted",
                    description=f"{channel.mention} is whitelisted hence affected with auto moderation now!",
                    color=var.C_GREEN
                ))
            else:
                await ctx.send("This channel is not blacklisted hence can't whitelist either")
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the channel too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}automodblacklist <#channel>```")
            )

    @commands.command()
    async def ignorebots(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
        ignored = GuildDoc["Settings"]["ignorebots"]
        embed = discord.Embed(title="Ignore auto-moderation on bots")
        if ignored:
            embed.description = f"{var.E_ENABLE} Bots are currently ignored hence immune from Auto-Moderation"
            embed.color = var.C_GREEN
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction(var.E_DISABLE)

            def disablecheck(reaction, user):
                if str(reaction.emoji) == var.E_DISABLE:
                    return user == ctx.author and reaction.message == botmsg

            await self.bot.wait_for("reaction_add", check=disablecheck)
            db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.ignorebots":False}})
            embed.description = f"{var.E_DISABLE} Bots are now not ignored hence affected by Auto-Moderation"
            embed.color = var.C_RED
            await botmsg.edit(embed=embed)
            try:
                await botmsg.clear_reactions()
            except discord.Forbidden:
                pass

        else:
            embed.description = f"{var.E_DISABLE} Bots are currently not ignored hence affected by Auto-Moderation"
            embed.color = var.C_RED
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction(var.E_ENABLE)

            def enablecheck(reaction, user):
                if str(reaction.emoji) == var.E_ENABLE:
                    return user == ctx.author and reaction.message == botmsg

            await self.bot.wait_for("reaction_add", check=enablecheck)
            db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.ignorebots":True}})
            embed.description = f"{var.E_ENABLE} Bots are now ignored hence immune from Auto-Moderation"
            embed.color = var.C_GREEN
            await botmsg.edit(embed=embed)
            try:
                await botmsg.clear_reactions()
            except discord.Forbidden:
                pass

    @commands.command()
    async def mentionamount(self, ctx, amount:int=None):
        if amount is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id})
            db.AUTOMOD.update_one(GuildDoc, {"$set":{"Mentions.amount": amount}})
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

            GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id})
            currentlist = GuildDoc["BadWords"]["words"]
            newlist = currentlist.copy()
            if word not in newlist:
                newlist.append(word)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"BadWords.words": newlist}})
                await ctx.send(embed=discord.Embed(
                    description=f"Successfully added the word **{word}** in badwords list",
                    color=var.C_GREEN
                ))
            else:
                await ctx.send(embed=discord.Embed(
                    description="This word already exists in the bad word list",
                    color=var.C_RED
                ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the word too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}addbadword <word>```")
            )
    
    @commands.command()
    async def removebadword(self, ctx, word:str=None):
        if word is not None:
            GuildDoc = db.AUTOMOD.find_one({"_id":ctx.guild.id})
            currentlist = GuildDoc["BadWords"]["words"]
            newlist = currentlist.copy()
            try:
                newlist.remove(word)
                db.AUTOMOD.update_one(GuildDoc, {"$set":{"BadWords.words": newlist}})
                await ctx.send(embed=discord.Embed(
                    description=f"Successfully added the word **{word}** in badwords list",
                    color=var.C_GREEN
                ))
            except ValueError:
                await ctx.send(embed=discord.Embed(
                    description=f"The word **{word}** does not exist in the bad word list hence can't remove it either",
                    color=var.C_RED
                ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the word too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}removebadword <word>```")
            )

    @commands.command()
    async def allbadwords(self, ctx):
        GuildDoc = db.AUTOMOD.find_one({"_id": ctx.guild.id})
        if GuildDoc is not None:
            embed = discord.Embed(title="Bad Words", description="All other forms of each bad words are also deleted", color=var.C_TEAL)
            allbannedwords = ""
            for i in GuildDoc["BadWords"]["words"]:
                allbannedwords += f"`{i}` "

            embed.add_field(name="All bad words", value=allbannedwords)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have any bad word right now.")


    @commands.Cog.listener()
    async def on_message(self, message):
        GuildDoc = db.AUTOMOD.find_one({'_id': message.guild.id})

        if (GuildDoc is not None and message.author != self.bot.user 
        and message.channel.id not in GuildDoc["Settings"]["blacklists"]
        and not any(item in GuildDoc["Settings"]["modroles"] for item in [i.id for i in message.author.roles])):
            if not message.author.bot or message.author.bot and GuildDoc["Settings"]["ignorebots"]:

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
                    if len([i for i in badwords if i in message.content]) > 0:
                        await message.delete()
                        res = GuildDoc["BadWords"]["response"]
                        await message.channel.send(f"{message.author.mention} {res}", delete_after=2)            



def setup(bot):
    bot.add_cog(AutoMod(bot))
