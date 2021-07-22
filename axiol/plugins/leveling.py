import random
import discord
from discord.ext import commands
import variables as var
import database as db
from functions import getprefix, getxprange
from ext.permissions import has_command_permission


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Leveling") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Leveling plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.command()
    @has_command_permission()
    async def rank(self, ctx, rankuser:discord.User=None):
        if rankuser is None:
            user = ctx.author
        else:
            user = rankuser

        GuildCol = db.LEVELDATABASE[str(ctx.guild.id)]
        userdata = GuildCol.find_one({"_id": user.id})
        if userdata is None:
                await ctx.send("This user does not have any rank yet...")
        else:
            xp = userdata["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50*(lvl**2))+(50*lvl)):
                    break
                lvl += 1
            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
            try:
                boxes = int((xp/(200*((1/2) * lvl)))*20)
            except:
                boxes = 0
            ranking = GuildCol.find().sort("xp", -1)
            for x in ranking:
                rank += 1
                if userdata["_id"] == x["_id"]:
                    break

            embed = discord.Embed(
            title=f"Level stats for {user.name}",
            color=var.C_TEAL
            ).add_field(name="Rank", value=f"{rank}/{GuildCol.estimated_document_count()-1}", inline=True
            ).add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True
            ).add_field(name="Level", value=lvl, inline=True
            ).add_field(name="Progress", value=boxes * "<:current:850041599139905586>" +(20-boxes) * "<:left:850041599127584776>", inline=False
            ).set_thumbnail(url=user.avatar_url
            )
            await ctx.channel.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def leaderboard(self, ctx):
        GuildCol = db.LEVELDATABASE[str(ctx.guild.id)]
        rankings = GuildCol.find({

                "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
                
            }).sort("xp", -1)

        if rankings.count() < 10:
            exactpages = 1
        else:
            exactpages = rankings.count() / 10
        if type(exactpages) != int:
            all_pages = round(exactpages) + 1
        else:
            all_pages = exactpages

        embed = discord.Embed(
        title=f"Leaderboard", 
        description="◀️ First page\n⬅️ Previous page\n<:RankChart:854068306285428767> Bar graph of top 10 users\n➡️ Next page\n▶️ Last page\n",
        color=var.C_BLUE
        ).set_thumbnail(url=ctx.guild.icon_url
        )

        rankcount = 0
        for i in rankings:
            rankcount += 1
            try:
                user = ctx.guild.get_member(i.get("_id"))
                xp = i.get("xp")
                embed.add_field(name=f"{rankcount}: {user}", value=f"Total XP: {xp}", inline=False)
            except:
                print(f"Not found {i}")

            if rankcount == 10:
                break
            
        embed.set_footer(text=f"Page 1/{all_pages}")
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction("◀️")
        await botmsg.add_reaction("⬅️")
        await botmsg.add_reaction("<:RankChart:854068306285428767>")
        await botmsg.add_reaction("➡️")
        await botmsg.add_reaction("▶️")

        async def leaderboardpagination(current_page, embed, all_pages):
            pagern = current_page + 1
            embed.set_footer(text=f"Page {pagern}/{all_pages}")
            embed.clear_fields()

            rankings = GuildCol.find({

                    "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
                    
                }).sort("xp", -1)

            rankcount = (current_page)*10
            user_amount = current_page*10
            for i in rankings[user_amount:]:
                rankcount += 1
                user = self.bot.get_user(i.get("_id"))
                xp = i.get("xp")
                embed.add_field(name=f"{rankcount}: {user}", value=f"Total XP: {xp}", inline=False)
                if rankcount == (current_page)*10 + 10:
                    break

        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg
        
        current_page = 0
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
            if str(reaction.emoji) == "◀️":
                try:
                    await botmsg.remove_reaction("◀️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page = 0
                await leaderboardpagination(current_page, embed, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "➡️":
                try:
                    await botmsg.remove_reaction("➡️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page += 1
                if current_page > all_pages:
                    current_page -= 1
                await leaderboardpagination(current_page, embed, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "<:RankChart:854068306285428767>":
                try:
                    await botmsg.clear_reactions()
                except discord.Forbidden:
                    pass
                await ctx.invoke(self.bot.get_command('barchart'))

            if str(reaction.emoji) == "⬅️":
                try:
                    await botmsg.remove_reaction("⬅️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page -= 1
                if current_page < 0:
                    current_page += 1
                await leaderboardpagination(current_page, embed, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "▶️":
                try:
                    await botmsg.remove_reaction("▶️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page = all_pages-1
                await leaderboardpagination(current_page, embed, all_pages)
                await botmsg.edit(embed=embed)


    @commands.command()
    @has_command_permission()
    async def levelinfo(self, ctx):
        GuildDoc = db.LEVELDATABASE.get_collection(str(ctx.guild.id)).find_one({"_id": 0})
        xprange = GuildDoc.get("xprange")
        bl = []

        for i in GuildDoc.get("blacklistedchannels"):
            bl.append(self.bot.get_channel(i).mention)

        blacklistedchannels = ', '.join(bl) if not bl == [] else None
        maxrank = db.LEVELDATABASE.get_collection(str(ctx.guild.id)).find().sort("xp", -1).limit(1)
        maxrank_user = self.bot.get_user(list(maxrank)[0].get("_id"))
        def getalertchannel():
            if GuildDoc.get("alertchannel") is not None:
                alertchannel = self.bot.get_channel(GuildDoc.get("alertchannel")).mention
            else:
                alertchannel = None
            return alertchannel
        status = "Enabled" if GuildDoc.get("alerts") == True else "Disabled" 
        rewards = GuildDoc.get("rewards")
        
        embed = discord.Embed(
        title="Server leveling information",
        color=var.C_BLUE
        ).set_thumbnail(url=ctx.guild.icon_url
        ).add_field(name="Highest XP Member", value=maxrank_user, inline=False
        ).add_field(name="Leveling XP Range", value=xprange, inline=False
        ).add_field(name="Blacklisted channels", value=blacklistedchannels, inline=False
        ).add_field(name="Alert Status", value=status, inline=False
        ).add_field(name="Alert channel", value=getalertchannel(), inline=False
        ).add_field(name="Level rewards", value=f"React to {var.E_CONTINUE}" if GuildDoc["rewards"] else "There are no level rewards right now", inline=False
        )
        botmsg = await ctx.send(embed=embed)
        if GuildDoc["rewards"]: 
            await botmsg.add_reaction(var.E_CONTINUE)

            def reactioncheck(reaction, user):
                if str(reaction.emoji) == var.E_CONTINUE:
                    return user == ctx.author and reaction.message == botmsg

            await self.bot.wait_for("reaction_add", check=reactioncheck)
            try:
                await botmsg.clear_reactions()
            except:
                pass
            rewards = GuildDoc.get("rewards")
            embed.title = "Level rewards"
            embed.clear_fields()
            for i in rewards:
                role = ctx.guild.get_role(rewards.get(i))
                embed.add_field(name=f"Level {i}", value=role.mention, inline=False)
            await botmsg.edit(embed=embed)


    @commands.command()
    @has_command_permission()
    async def givexp(self, ctx, user:discord.Member=None, amount:int=None):

        if user and amount is not None:

            if amount > 10000000 :
                await ctx.send(embed=discord.Embed(
                    description="🚫 Ayo that's too much",
                    color=var.C_RED
                ))
            else:
                GuildCol = db.LEVELDATABASE[str(ctx.guild.id)]
                data = GuildCol.find_one({"_id": user.id})
                if data is None:
                    GuildCol.insert_one({"_id": user.id, "xp": amount})
                    await ctx.send(f"Successfully awarded {user} with {amount} xp!")
                    
                elif data.get("xp") > 10000000:
                    await ctx.send(embed=discord.Embed(
                        description="🚫 Cannot give more xp to the user, they are too rich already",
                        color=var.C_RED
                    ))
                else:
                    newdata = {"$set":{
                                "xp": data.get("xp") + amount
                            }}
                    GuildCol.update_one(data, newdata)
                    await ctx.send(f"Successfully awarded {user} with {amount} xp!")
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the member and the amount to give them xp",
            color=var.C_RED
            ).add_field(name="Format", value=f"```{getprefix(ctx)}givexp <user> <amount>```"
            ).set_footer(text="For user either user mention or user ID can be used")
            )


    @commands.command()
    @has_command_permission()
    async def removexp(self, ctx, user:discord.Member=None, amount:int=None):
        if user and amount is not None:
            if amount > 10000000 :
                await ctx.send(embed=discord.Embed(
                    description="🚫 Ayo that's too much",
                    color=var.C_RED
                ))
            else:
                GuildCol = db.LEVELDATABASE[str(ctx.guild.id)]
                data = GuildCol.find_one({"_id": user.id})

                newdata = {"$set":{
                            "xp": data.get("xp") - amount
                        }}
                GuildCol.update_one(data, newdata)
                await ctx.send(f"Successfully removed {amount} xp from {user}!")
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the member and the amount to remove their xp",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}removexp <user> <amount>`"
            ).set_footer(text="For user either user mention or user ID can be used")
            )


    @commands.command()
    @has_command_permission()
    async def xprange(self, ctx, minval:int=None, maxval:int=None):
        if minval and maxval is not None:
            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newdata = {"$set":{
                "xprange": [minval, maxval]
            }}
            GuildCol.update_one(settings, newdata)
            await ctx.send(embed=discord.Embed(
                        description=f"New xp range is now {minval} - {maxval}!",
                        color=var.C_GREEN)
            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the xp range",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}xprange <min_xp> <max_xp>`"
            )
            )


    @commands.command()
    @has_command_permission()
    async def blacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklistedchannels").copy()
            newsettings.append(channel.id)
            newdata = {"$set":{
                "blacklistedchannels": newsettings
                }}
            GuildCol.update_one(settings, newdata)

            await ctx.send(embed=discord.Embed(
                        description=f"{channel.mention} has been blacklisted, hence users won't gain any xp in that channel.",
                        color=var.C_GREEN)
                        )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the channel to blacklist it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}blacklist <#channel>`"
            )
            )


    @commands.command()
    @has_command_permission()
    async def whitelist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklistedchannels").copy()
            if channel.id in newsettings:

                newsettings.remove(channel.id)
                newdata = {"$set":{
                    "blacklistedchannels": newsettings
                    }}
                GuildCol.update_one(settings, newdata)
                await ctx.send(embed=discord.Embed(
                            description=f"{channel.mention} has been removed from blacklist, hence users will be able to gain xp again in that channel.",
                            color=var.C_GREEN)
                            )
            else:
                await ctx.send(f"{channel.mention} was not blacklisted")

        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the channel to whitelist it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}whitelist <#channel>`"
            )
            )


    @commands.command(aliases=["removealerts"])
    @has_command_permission()
    async def togglealerts(self, ctx):
        GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
        GuildConfig = GuildCol.find_one({"_id": 0})
        if GuildConfig.get("alerts") == True:
            newdata = {"$set":{
                "alerts": False
            }}
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_ACCEPT} Successfully disabled alerts!",
                color=var.C_GREEN
            ))
        else:
            newdata = {"$set":{
                "alerts": True
            }}
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_ACCEPT} Successfully enabled alerts!",
                color=var.C_GREEN
            ))
        GuildCol.update_one(GuildConfig, newdata)


    @commands.command()
    @has_command_permission()
    async def alertchannel(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newdata = {"$set":{
                "alertchannel": channel.id
                }}
            GuildCol.update_one(settings, newdata)
            await ctx.send(embed=discord.Embed(
                        description=f"{channel.mention} has been marked as the alert channel, hence users who will level up will get mentioned here!",
                        color=var.C_GREEN)
                        )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the channel to make it the alert channel",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}alertchannel <#channel>`"
            )
            )


    @commands.command(aliases=["addreward"])
    @has_command_permission()
    async def reward(self, ctx, level:str=None, role:discord.Role=None):
        if level and role is not None and level.isnumeric():

            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            existingdata = settings.get("rewards")

            newdict = existingdata.copy()

            newdict.update({level: role.id})
            newdata = {"$set":{
                "rewards":newdict
            }}

            GuildCol.update_one(settings, newdata)
            await ctx.send(embed=discord.Embed(
                        description=f"Successfully added {role.mention} as the reward to Level {level}!",
                        color=var.C_GREEN)
                        )

        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the level and role both to add a reward!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}reward <level> <role>`"
            ).set_footer(text=f"Make sure that for level you only the enter level number, example: {getprefix(ctx)}reward 2 @somerole\nNot {getprefix(ctx)}reward level2 @somerole")
            )

    @commands.command()
    @has_command_permission()
    async def removereward(self, ctx, level:str=None):
        if level is not None:

            GuildCol = db.LEVELDATABASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            existingdata = settings.get("rewards")
            if not level in existingdata.keys():
                await ctx.send("This role does not have any rewards setted up")
            else:
                newdict = existingdata.copy()
                role = ctx.guild.get_role(newdict.get(level))
                newdict.pop(level)
                
                newdata = {"$set":{
                    "rewards":newdict
                }}

                GuildCol.update_one(settings, newdata)
                await ctx.send(embed=discord.Embed(
                            description=f"Successfully removed {role.mention} as the reward from Level {level}!",
                            color=var.C_GREEN)
                            )

        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the level to remove it's reward!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}removereward <level>`"
            ).set_footer(text=f"Make sure that for level you only the enter level number, example: {getprefix(ctx)}removereward 2 \nNot {getprefix(ctx)}removereward level2 ")
            )



    @commands.Cog.listener()
    async def on_message(self, message):
        
        GuildPluginLevelingDoc = db.PLUGINS.find_one({"_id": message.guild.id})

        if GuildPluginLevelingDoc.get("Leveling") and message.author.bot == False:
            if not message.channel.id in db.LEVELDATABASE[str(message.guild.id)].find_one({"_id":0}).get("blacklistedchannels"):

                GuildLevelDoc = db.LEVELDATABASE[str(message.guild.id)]
                userdata = GuildLevelDoc.find_one({"_id": message.author.id})

                if userdata is None:
                    GuildLevelDoc.insert_one({"_id": message.author.id, "xp": 0})
                else:
                    xp = userdata["xp"]

                    initlvl = 0
                    while True:
                        if xp < ((50*(initlvl**2))+(50*initlvl)):
                            break
                        initlvl += 1

                    xp = userdata["xp"] + random.randint(getxprange(message)[0], getxprange(message)[1])
                    GuildLevelDoc.update_one(userdata, {"$set": {"xp": xp}})

                    levelnow = 0
                    while True:
                        if xp < ((50*(levelnow**2))+(50*levelnow)):
                            break
                        levelnow += 1

                    if levelnow > initlvl and GuildLevelDoc.find_one({"_id":0}).get("alerts") == True:
                        ch = self.bot.get_channel(GuildLevelDoc.find_one({"_id":0}).get("alertchannel"))
                        embed = discord.Embed(
                        title="You leveled up!",
                        description=f"{var.E_ACCEPT} You are now level {levelnow}!",
                        color=var.C_MAIN
                        )
                        try:
                            if ch is not None:
                                await ch.send(content=message.author.mention, embed=embed)
                            else:
                                await message.channel.send(content=message.author.mention, embed=embed)
                        except discord.Forbidden:
                            pass

                    rewards = GuildLevelDoc.find_one({"_id":0}).get("rewards")
                    if str(levelnow) in rewards.keys():
                        roleid = rewards.get(str(levelnow))
                        role = message.guild.get_role(roleid)
                        if role is not None and role not in message.author.roles:
                            try:
                                await message.author.add_roles(role)
                            except:
                                print(f"ERROR! {role} - {roleid} in server {message.guild.id} with name {message.guild.name}")
def setup(bot):
    bot.add_cog(Leveling(bot))
