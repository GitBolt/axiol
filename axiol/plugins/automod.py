
import re
import discord
from discord.ext import commands
import database as db
import variables as var
from functions import get_prefix
from ext.permissions import has_command_permission


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("AutoMod"):
            return True
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Auto-Moderation plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.group(pass_context=True, invoke_without_command=True, aliases=["filter"])
    @has_command_permission()
    async def filters(self ,ctx):
        embed = discord.Embed(title="All Auto-Moderation filters", description="Use the subcommand to configure each filter seperately!", color=var.C_MAIN)
        embed.set_footer(text="The emoji before filter name is their status whether they are enabled or disabled")
        GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0, "Settings": 0})
        for i in GuildDoc:
            status = var.E_ENABLE if GuildDoc[i]["status"] == True else var.E_DISABLE
            embed.add_field(name=status + " " + i , value=f"{await get_prefix(ctx)}filters {i.lower()}", inline=False)
        
        await ctx.send(embed=embed)


    async def manage_filter(self, filtername, embed, GuildDoc, ctx): 
        if GuildDoc[filtername]["status"]:
            embed.description = f"{var.E_ENABLE} This Auto-Moderation filter is currently enabled"
            embed.color = var.C_GREEN
            if filtername == "BadWords":
                embed.add_field(name=f"{await get_prefix(ctx)}addbadword `<word>`", value="Adds a word to bad word list", inline=False)
                embed.add_field(name=f"{await get_prefix(ctx)}removebadword `<word>`", value="Removes a word from bad word list", inline=False)
                embed.add_field(name=f"{await get_prefix(ctx)}allbadwords", value="Shows all bad words", inline=False)
            if filtername == "Mentions":
                embed.add_field(name=f"{await get_prefix(ctx)}mentionamount `<amount>`", value="Change the mention amount to delete, by default it's 5", inline=False)

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
                await db.AUTOMOD.update_one(GuildDoc, newdata)
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
                    await db.AUTOMOD.update_one(GuildDoc, newdata) 
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
            await db.AUTOMOD.update_one(GuildDoc, newdata)

            embed.title=f"{filtername} filter enabled"
            embed.description=f"{var.E_ENABLE} This Auto-Moderation filter has been enabled"
            embed.color=var.C_GREEN
            await botmsg.edit(embed=embed)
            try:
                await botmsg.clear_reactions()
            except discord.Forbidden:
                pass


    @filters.command()
    @has_command_permission()
    async def invites(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Invites filter"
        )
        await self.manage_filter("Invites", embed, GuildDoc, ctx)

    @filters.command()
    @has_command_permission()
    async def links(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Links filter"
        )
        await self.manage_filter("Links", embed, GuildDoc, ctx)

    @filters.command()
    @has_command_permission()
    async def badwords(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="BadWords filter"
        )
        await self.manage_filter("BadWords", embed, GuildDoc, ctx)

    @filters.command()
    @has_command_permission()
    async def mentions(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id}, {"_id":0})
        embed = discord.Embed(
            title="Mentions filter"
        )
        await self.manage_filter("Mentions", embed, GuildDoc, ctx)


    @commands.command()
    @has_command_permission()
    async def addmodrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
            currentlist = GuildDoc["Settings"]["modroles"]
            newlist = currentlist.copy()
            if role.id not in currentlist:
                newlist.append(role.id)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.modroles": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}addmodrole <role>```")
            )

    @commands.command()
    @has_command_permission()
    async def removemodrole(self, ctx, role:discord.Role=None):
        if role is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
            currentlist = GuildDoc["Settings"]["modroles"]
            newlist = currentlist.copy()
            if role.id in currentlist:
                newlist.remove(role.id)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.modroles": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}addmodrole <role>```")
            )


    @commands.command()
    @has_command_permission()
    async def allmodroles(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
        if GuildDoc is not None:
            embed = discord.Embed(title="Moderator roles", description="These roles are immune to auto-moderation by me!", color=var.C_MAIN)
            value = ""
            for i in GuildDoc["Settings"]["modroles"]:
                role = ctx.guild.get_role(i)
                value += f'{role.mention} '
            if value != "":
                embed.add_field(name="Immune roles", value=value)
                await ctx.send(embed=embed)
            else:
                await ctx.send("There are no mod roles yet")
        else:
            await ctx.send("Auto moderation is not setted up yet")


    @commands.command()
    @has_command_permission()
    async def automodblacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None and channel.id not in GuildDoc["Settings"]["blacklists"]:
                currentlist = GuildDoc["Settings"]["blacklists"]
                newlist = currentlist.copy()
                newlist.append(channel.id)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.blacklists": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}automodblacklist <#channel>```")
            )

    @commands.command()
    @has_command_permission()
    async def automodwhitelist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
            if GuildDoc is not None and channel.id in GuildDoc["Settings"]["blacklists"]:
                currentlist = GuildDoc["Settings"]["blacklists"]
                newlist = currentlist.copy()
                newlist.remove(channel.id)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.blacklists": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}automodblacklist <#channel>```")
            )

    @commands.command()
    async def allautomodwhitelists(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
        if GuildDoc is not None:
            embed = discord.Embed(title="All Auto-Moderation whitelists", description="Messages in these channel are immune from automod", color=var.C_MAIN)
            desc = ""
            for i in GuildDoc["Settings"]["blacklists"]:
                desc += f"{i.mention} "

            if desc != "":
                await ctx.send(embed=embed)
            else:
                await ctx.send("There are no blacklisted channels right now")
        else:
            await ctx.send("This server does not have automod setted up right now")

            
    @commands.command()
    @has_command_permission()
    async def ignorebots(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
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
            await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.ignorebots":False}})
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
            await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Settings.ignorebots":True}})
            embed.description = f"{var.E_ENABLE} Bots are now ignored hence immune from Auto-Moderation"
            embed.color = var.C_GREEN
            await botmsg.edit(embed=embed)
            try:
                await botmsg.clear_reactions()
            except discord.Forbidden:
                pass

    @commands.command()
    @has_command_permission()
    async def mentionamount(self, ctx, amount:int=None):
        if amount is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id})
            await db.AUTOMOD.update_one(GuildDoc, {"$set":{"Mentions.amount": amount}})
            await ctx.send(embed=discord.Embed(
                description=f"Successfully changed the amount of mentions to be deleted to **{amount}**",
                color=var.C_GREEN
            ))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to define the amount too!",
                color=var.C_RED
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}mentionamount <amount>```")
            )

    @commands.command()
    @has_command_permission()
    async def addbadword(self, ctx, word:str=None):
        if word is not None:

            GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id})
            currentlist = GuildDoc["BadWords"]["words"]
            newlist = currentlist.copy()
            if word not in newlist:
                newlist.append(word)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"BadWords.words": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}addbadword <word>```")
            )
    
    @commands.command()
    @has_command_permission()
    async def removebadword(self, ctx, word:str=None):
        if word is not None:
            GuildDoc = await db.AUTOMOD.find_one({"_id":ctx.guild.id})
            currentlist = GuildDoc["BadWords"]["words"]
            newlist = currentlist.copy()
            try:
                newlist.remove(word)
                await db.AUTOMOD.update_one(GuildDoc, {"$set":{"BadWords.words": newlist}})
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
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}removebadword <word>```")
            )

    @commands.command()
    @has_command_permission()
    async def allbadwords(self, ctx):
        GuildDoc = await db.AUTOMOD.find_one({"_id": ctx.guild.id})
        if GuildDoc is not None:
            embed = discord.Embed(title="Bad Words", description="All other forms of each bad words are also deleted", color=var.C_TEAL)
            allbannedwords = ""
            for i in GuildDoc["BadWords"]["words"]:
                allbannedwords += f"`{i}` "
            
            if allbannedwords == "":
                await ctx.send("This server does not have any bad word right now.")
            else:
                embed.add_field(name="All bad words", value=allbannedwords)
                await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have automod setted up")


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        PluginDoc = await db.PLUGINS.find_one({"_id": message.guild.id})
        if PluginDoc["AutoMod"]:
            GuildDoc = await db.AUTOMOD.find_one({'_id': message.guild.id})
            if (GuildDoc is not None and message.author != self.bot.user 
            and message.channel.id not in GuildDoc["Settings"]["blacklists"]
            and not any(item in GuildDoc["Settings"]["modroles"] for item in [i.id for i in message.author.roles])):
                if not message.author.bot or message.author.bot and GuildDoc["Settings"]["ignorebots"]:
                    
                    if GuildDoc["Links"]["status"]:
                        regex = re.compile(
                            r"(?:http|ftp)s?://" # http:// or https://
                            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|" #domain...
                            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" # ...or ip
                            r"(?::\d+)?", # optional port
                            #r"([a-zA-Z0-9\-]+)", 
                            flags=re.IGNORECASE)

                        if regex.findall(message.content):
                            await message.delete()
                            res = GuildDoc["Links"]["response"]
                            await message.channel.send(f"{message.author.mention} {res}", delete_after=2)

                    if GuildDoc["Invites"]["status"]:
                        regex = re.compile(
                            r"(?:discord(?:[\.,]|dot)gg|" # Could be discord.gg/
                            r"discord(?:[\.,]|dot)com(?:\/|slash)invite|"# or discord.com/invite/
                            r"discordapp(?:[\.,]|dot)com(?:\/|slash)invite|"# or discordapp.com/invite/
                            r"discord(?:[\.,]|dot)me|" # or discord.me
                            r"discord(?:[\.,]|dot)li|" # or discord.li
                            r"discord(?:[\.,]|dot)io" # or discord.io.
                            r")(?:[\/]|slash)" # / or 'slash'
                            r"([a-zA-Z0-9\-]+)", # the invite code itself
                            flags=re.IGNORECASE
                        )

                        if regex.findall(message.content):
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
