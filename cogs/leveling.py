import random
import discord
from discord.ext import commands
import utils.vars as var


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["setuplevel", "setuplevels", "addlevel", "addleveling", "startleveling"])
    @commands.has_permissions(administrator=True)
    async def levelsetup(self, ctx):

        if str(ctx.guild.id) in var.LEVELDATABASE.list_collection_names():
            if var.LEVELDATABASE[str(ctx.guild.id)].find_one({"_id":0}).get("status") == True:
                em = discord.Embed(title="Configure Leveling for your server", 
                    description=f"Leveling is already enabled in this server", color=var.CTEAL)

                em.add_field(name="Configure", value=f"React to {var.SETTINGS}")
                em.add_field(name="Disable", value=f"React to {var.DISABLE}")
                em.add_field(name="Remove", value=f"React to {var.CANCEL}")
                em.set_footer(text="Removing leveling for the server deletes all the existing data ⚠️")
                msg = await ctx.send(embed=em)
                await msg.add_reaction(var.SETTINGS)
                await msg.add_reaction(var.DISABLE)
                await msg.add_reaction(var.CANCEL)
            else:
                dismsg = await ctx.send(embed=discord.Embed(title="Leveling disabled", description="Leveling for this server is currently disabled").add_field(name="Enable", value=f"React to {var.ENABLE}"))
                dismsg.add_reaction(var.ENABLE)
        else:
            msg = await ctx.send(embed=discord.Embed(title="Add leveling to you server",
                                description=f"React to the {var.CONFIRM} emoji to enable leveling on this server", color=var.CMAIN))
            await msg.add_reaction(var.CONFIRM)

        def check(reaction, user):
            if user == ctx.author and reaction.message == msg:
                return str(reaction.emoji) == var.CONFIRM or var.SETTINGS or var.DISABLE or var.CANCEL or var.ENABLE

        reaction, user = await self.bot.wait_for('reaction_add', check=check)
        if str(reaction.emoji) == var.CONFIRM:
            var.LEVELDATABASE.create_collection(str(ctx.guild.id))
            var.LEVELDATABASE[str(ctx.guild.id)].insert_one({
                "_id": 0,
                "status": True,
                "alertchannel": ctx.channel.id,
                "blacklistedchannels": []
            })    
            await ctx.send("Successfully setted up leveling for this server")

        if str(reaction.emoji) == var.SETTINGS:
            await ctx.send("set")

        if str(reaction.emoji) == var.DISABLE:
            col = var.LEVELDATABASE[str(ctx.guild.id)]
            data = col.find_one({"_id": 0})

            newdata = {"$set":{
                        "status": False
                    }}
            var.LEVELDATABASE[str(ctx.guild.id)].update_one(data, newdata)
            try:
                pref = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
            except AttributeError:
                pref = var.DEFAULT_PREFIX
            await ctx.send(embed=discord.Embed(title="Leveling disabled", description="Leveling for this server has been disabled, this means that the rank data is still there but users won't gain xp until enabled again", color=var.CBLUE).add_field(name=pref+"levelsetup", value=f"Use the command and react to the {var.ENABLE} to enable leveling again"))
        
        if str(reaction.emoji) == var.CANCEL:
            var.LEVELDATABASE[str(ctx.guild.id)].drop()
            await ctx.send(embed=discord.Embed(title="Leveling removed", description="Leveling have been removed from this server, that means all the rank data has been deleted"), color=var.CORANGE)
        
        if str(reaction.emoji) == var.ENABLE:
            await ctx.send("en")
    
        

    @commands.Cog.listener()
    async def on_message(self, message):

        if str(message.guild.id) in var.LEVELDATABASE.list_collection_names():
            guildlevels = var.LEVELDATABASE[str(message.guild.id)]
            userdata = guildlevels.find_one({"_id": message.author.id})

            if userdata is None:
                guildlevels.insert_one({"_id": message.author.id, "xp": 0})
            else:
                xp = userdata["xp"] + random.randint(10, 30)
                guildlevels.update_one(userdata, {"$set": {"xp": xp}})
                level = 0
                while True:
                    if xp < ((50*(level**2))+(50*level)):
                        break
                    level += 1
                xp -= ((50*((level-1)**2))+(50*(level-1)))
                if xp == 0:
                    if message.channel.id not in guildlevels.find_one({"_id":1}).get("noupdate_channels"):
                        await message.channel.send(f"{message.author.mention} you leveled up to level {level}!")

    

    @commands.command()
    async def rank(self, ctx, rankuser:discord.Member=None):
        if rankuser is None:
            user = ctx.author
        else:
            user = rankuser

        guildlevels = var.LEVELDATABASE[str(ctx.guild.id)]
        if guildlevels is not None:
            userdata = guildlevels.find_one({"_id": user.id})
            if userdata is None:
                await ctx.send("The user does not have any rank yet :(")
            else:
                xp = userdata["xp"]
                level = 0
                rank = 0
                while True:
                    if xp < ((50*(level**2))+(50*(level-1))):
                        break
                    level += 1

                xp -= ((50*((level-1)**2))+(50*(level-1)))
                boxes = int((xp/(200*((1/2)* level)))*20)
                rankings = guildlevels.find().sort("xp", -1)
                for i in rankings:
                    rank += 1
                    if userdata["_id"] == i["_id"]:
                        break
                embed = discord.Embed(title=f"Level stats for {user.name}",
                                    description=boxes * "<:blue:808242875933786112>" + (20-boxes) * "<:white:808242875728789525>", 
                                    color=discord.Colour.gold())
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*level))}", inline=True)
                embed.add_field(name="Level", value=level, inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                msg = await ctx.channel.send(embed=embed)
        else:
            await ctx.send("No one in this server has any rank yet :O")


    @commands.command()
    async def leaderboard(self, ctx):
        guildlevels = var.LEVELDATABASE[str(ctx.guild.id)]
        if guildlevels is not None:
            rankings = guildlevels.find().sort("xp", -1)
            embed = discord.Embed(title=f"Leaderboard for {ctx.guild.name}", color=var.CBLUE)
            rankcount = 0
            for i in rankings:
                rankcount += 1
                user = await ctx.guild.fetch_member(i.get("_id"))
                xp = i.get("xp")
                embed.add_field(name=f"{rankcount}: {user.name}", value=f"Total XP: {xp}", inline=False)
            print("hi")
            await ctx.send(embed=embed)
        else:
            await ctx.send("No one in this server has any rank yet :OOOOOOOO") 

def setup(bot):
    bot.add_cog(Leveling(bot))