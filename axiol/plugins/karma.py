import nltk
import discord
from discord.ext import commands
from nltk.sentiment import SentimentIntensityAnalyzer
import database as db
import variables as var
from functions import get_prefix
from ext.permissions import has_command_permission


nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()


class Karma(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Karma"):
            return True
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Karma plugin is disabled in this server",
                color=var.C_ORANGE
            ))



    @commands.command()
    @has_command_permission()
    async def karma(self, ctx, karmauser:discord.User=None):
        if karmauser is None:
            user = ctx.author
        else:
            user = karmauser

        GuildCol = await db.KARMADATBASE[str(ctx.guild.id)]
        userdata = GuildCol.find_one({"_id": user.id})

        karmas = list(GuildCol.find({

                "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
                
            }).sort("karma", -1))

        if userdata is None:
                await ctx.send("This user does not have any karma yet...")
        else:
            position = karmas.index(userdata) + 1 #Index starts with one
            embed = discord.Embed(
            title=f"Karma for {user.name}",
            color=var.C_MAIN
            ).add_field(name="Karma", value=userdata["karma"], inline=True
            ).add_field(name="Position", value=f"{position}/{len(karmas)}", inline=False
            ).set_thumbnail(url=user.avatar_url
            )
            totalkarma = 0
            for i in karmas:
                totalkarma += i["karma"]
            average = totalkarma/len(karmas)
            if userdata["karma"] > average:
                embed.description=f"Your karma is better than the average {user.name}! :)"
            if userdata["karma"] < average:
                embed.description = f"Your karma is lower than the average {user.name}, is it because you don't talk much or you are not nice enough? :eyes:"
            if position == 1:
                embed.description = f"Woohoo {user.name}, you are the nicest person in the server!"
            await ctx.channel.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def karmaboard(self, ctx):
        GuildCol = await db.KARMADATBASE[str(ctx.guild.id)]
        karmas = list(GuildCol.find({

                "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
                
            }).sort("karma", -1))

        print(karmas)
        if len(karmas) < 10:
            exactpages = 1
        else:
            exactpages = len(karmas) / 10
        if type(exactpages) != int:
            all_pages = round(exactpages) + 1
        else:
            all_pages = exactpages

        totalkarma = 0
        for i in karmas:
            totalkarma += i["karma"]
        average = totalkarma/len(karmas)

        embed = discord.Embed(
        title=f"Karma Board", 
        description=f"The average karma in this server is **{average}**",
        color=var.C_BLUE
        ).set_thumbnail(url=ctx.guild.icon_url
        )

        count = 0
        for i in karmas:
            count += 1
            try:
                user = self.bot.get_user(i.get("_id"))
                karma = i.get("karma")
                embed.add_field(name=f"{count}: {user}", value=f"Total Karma: {karma}", inline=False)
            except:
                print(f"Not found {i}")
            if count == 10:
                break
            
        embed.set_footer(text=f"Page 1/{all_pages}")
        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction("◀️")
        await botmsg.add_reaction("⬅️")
        await botmsg.add_reaction("➡️")
        await botmsg.add_reaction("▶️")

        def reactioncheck(reaction, user):
            return user == ctx.author and reaction.message == botmsg

        async def pagination(ctx, current_page, embed, GuildCol, all_pages):
            pagern = current_page + 1
            embed.set_footer(text=f"Page {pagern}/{all_pages}")
            embed.clear_fields()

            karmas = list(GuildCol.find({

                    "_id": { "$ne": 0 }, #Removing ID 0 (Config doc, unrelated to user xp) 
                    
                }).sort("karma", -1))

            rankcount = (current_page)*10
            user_amount = current_page*10
            for i in karmas[user_amount:]:
                rankcount += 1
                user = self.bot.get_user(i.get("_id"))
                karma = i.get("karma")
                embed.add_field(name=f"{rankcount}: {user}", value=f"Total Karma: {karma}", inline=False)
                if rankcount == (current_page)*10 + 10:
                    break

        current_page = 0
        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
            if str(reaction.emoji) == "◀️":
                try:
                    await botmsg.remove_reaction("◀️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page = 0
                await pagination(ctx, current_page, embed, GuildCol, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "➡️":
                try:
                    await botmsg.remove_reaction("➡️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page += 1
                if current_page > all_pages:
                    current_page -= 1
                await pagination(ctx, current_page, embed, GuildCol, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "⬅️":
                try:
                    await botmsg.remove_reaction("⬅️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page -= 1
                if current_page < 0:
                    current_page += 1
                await pagination(ctx, current_page, embed, GuildCol, all_pages)
                await botmsg.edit(embed=embed)

            if str(reaction.emoji) == "▶️":
                try:
                    await botmsg.remove_reaction("▶️", ctx.author)
                except discord.Forbidden:
                    pass
                current_page = all_pages-1
                await pagination(ctx, current_page, embed, GuildCol, all_pages)
                await botmsg.edit(embed=embed)


    @commands.command()
    @has_command_permission()
    async def kblacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = await db.KARMADATBASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklists").copy()
            if channel.id in newsettings:
                await ctx.send("This channel is already blacklisted")
            else:
                newsettings.append(channel.id)
                newdata = {"$set":{
                    "blacklists": newsettings
                    }}
                GuildCol.update_one(settings, newdata)

                await ctx.send(embed=discord.Embed(
                            description=f"{channel.mention} has been blacklisted, hence users won't gain any karma in that channel.",
                            color=var.C_GREEN)
                            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the channel to blacklist it!",
            color=var.C_RED
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}kblacklist <#channel>```"
            )
            )

    @commands.command()
    @has_command_permission()
    async def kwhitelist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = await db.KARMADATBASE.get_collection(str(ctx.guild.id))
            settings = GuildCol.find_one({"_id": 0})

            newsettings = settings.get("blacklists").copy()
            if not channel.id in newsettings:
                await ctx.send("This channel is not blacklisted")
            else:
                newsettings.remove(channel.id)
                newdata = {"$set":{
                    "blacklists": newsettings
                    }}
                GuildCol.update_one(settings, newdata)

                await ctx.send(embed=discord.Embed(
                            description=f"{channel.mention} has been whitelisted, hence users would be able to gain karma again in that channel.",
                            color=var.C_GREEN)
                            )
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define the channel to whitelist it!",
            color=var.C_RED
            ).add_field(name="Format", value=f"```{await get_prefix(ctx)}kwhitelist <#channel>```"
            )
            )


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        PluginDoc = await db.PLUGINS.find_one({"_id": message.guild.id})
        if PluginDoc["Karma"] and not message.author.bot:
            if not message.channel.id in await db.KARMADATBASE[str(message.guild.id)].find_one({"_id":0})["blacklists"]:

                GuildKarmaDoc = await db.KARMADATBASE[str(message.guild.id)]
                userdata = GuildKarmaDoc.find_one({"_id": message.author.id})
                polarity = sia.polarity_scores(message.content)
                result = max(polarity, key=polarity.get)
                def getkarma():
                    if result == "neg":
                        return -polarity[result]
                    elif result == "pos":
                        return polarity[result]
                    else:
                        return 0

                if userdata is None:
                    GuildKarmaDoc.insert_one({"_id": message.author.id, "karma": getkarma()})
                else:
                    newkarma = getkarma()
                    newkarma += userdata["karma"]
                    GuildKarmaDoc.update_one(userdata, {"$set": {"karma": newkarma}})

def setup(bot):
    bot.add_cog(Karma(bot))