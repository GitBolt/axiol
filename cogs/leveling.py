import random
import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import prefix

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["level", "setuplevels", "setuplevel"])
    @commands.has_permissions(administrator=True)
    async def levels(self, ctx):
        if str(ctx.guild.id) in var.LEVELDATABASE.list_collection_names(): #Check if leveling exists 
            if var.LEVELDATABASE[str(ctx.guild.id)].find_one({"_id":0}).get("status") == True: #If leveling exists and enabled

                embed = discord.Embed(
                title="Configure Leveling for this server", 
                description=f"Leveling is enabled in this server", 
                color=var.CMAIN
                ).add_field(name="Configure", value=f"React to {var.SETTINGS}"
                ).add_field(name="Disable", value=f"React to {var.DISABLE}"
                ).add_field(name="Remove", value=f"React to {var.DECLINE}"
                ).set_footer(text="Removing will delete all rank data ⚠️"
                )
                botmsg = await ctx.send(embed=embed)
                await botmsg.add_reaction(var.SETTINGS)
                await botmsg.add_reaction(var.DISABLE)
                await botmsg.add_reaction(var.DECLINE)

            else: #If leveling exists but disabled
                embed = discord.Embed(
                title="Leveling disabled", 
                description="Leveling for this server is currently disabled", 
                color=var.CORANGE
                ).add_field(name="Enable", value=f"React to {var.ENABLE}"
                )
                botmsg = await ctx.send(embed=embed)
                await botmsg.add_reaction(var.ENABLE)

        else: #If leveling does not exist
            embed = discord.Embed(
            title="Add leveling to you server",
            description=f"React to the {var.ACCEPT} emoji to enable leveling on this server!", 
            color=var.CMAIN
            )
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction(var.ACCEPT)

        #Reaction checks
        def check(reaction, user):
            if user == ctx.author and reaction.message == botmsg:
                return str(reaction.emoji) == var.ACCEPT or var.DECLINE or var.DISABLE or var.ENABLE or var.SETTINGS 

        reaction, user = await self.bot.wait_for('reaction_add', check=check)

        if str(reaction.emoji) == var.ACCEPT: #Add leveling
            await botmsg.clear_reactions()

            var.LEVELDATABASE.create_collection(str(ctx.guild.id))
            var.LEVELDATABASE[str(ctx.guild.id)].insert_one({
                "_id": 0,
                "status": True,
                "alertchannel": ctx.channel.id,
                "blacklistedchannels": []
            })    

            embed = discord.Embed(
            title="Successfully setted up leveling for this server",
            description=f"To further configure, disable or remove leveling use the same command (`{prefix(ctx)}levels`)",
            color=var.CGREEN
            )
            await ctx.send(embed=embed)

        if str(reaction.emoji) == var.DECLINE:
            await botmsg.clear_reactions()

            var.LEVELDATABASE[str(ctx.guild.id)].drop()

            embed = discord.Embed(
            title="Leveling removed", 
            description="Leveling have been removed from this server, that means all the rank data has been deleted", 
            color=var.CGREEN
            )
            await ctx.send(embed=embed)

        if str(reaction.emoji) == var.ENABLE: #Enable
            await botmsg.clear_reactions()

            col = var.LEVELDATABASE[str(ctx.guild.id)]
            data = col.find_one({"_id": 0})

            newdata = {"$set":{
                        "status": True
                    }}
            var.LEVELDATABASE[str(ctx.guild.id)].update_one(data, newdata)
            await ctx.send("Successfully enabled leveling again on this server!")

        if str(reaction.emoji) == var.DISABLE: #Disable
            await botmsg.clear_reactions()

            col = var.LEVELDATABASE[str(ctx.guild.id)]
            data = col.find_one({"_id": 0})

            newdata = {"$set":{
                        "status": False
                    }}
            var.LEVELDATABASE[str(ctx.guild.id)].update_one(data, newdata)

            embed = discord.Embed(
            title="Leveling for this server has been disabled", 
            description="This means that the rank data is still there but users won't gain xp until enabled again", 
            color=var.CORANGE
            ).add_field(name=prefix(ctx)+"levels", value=f"Use the command and react to the {var.ENABLE} to enable leveling again"
            )
            await ctx.send(embed=embed)
        
        if str(reaction.emoji) == var.SETTINGS: #Configure
            await botmsg.clear_reactions()
            await ctx.invoke(self.bot.get_command('settings'))


    @commands.command()
    async def givexp(self, ctx, user:discord.Member=None, amount:int=None):
        if user and amount is not None:
            if str(ctx.guild.id) in var.LEVELDATABASE.list_collection_names():
                col = var.LEVELDATABASE[str(ctx.guild.id)]
                data = col.find_one({"_id": user.id})

                newdata = {"$set":{
                            "xp": data.get("xp") + amount
                        }}
                var.LEVELDATABASE[str(ctx.guild.id)].update_one(data, newdata)
                await ctx.send(f"Successfully awarded {user} with {amount} xp!")
            else:
                embed = discord.Embed(
                title="Can't give XP to the user",
                description=f"Leveling for this server is not setted up, use the command `{prefix(ctx)} levels to enable leveling",
                color=var.CRED
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"You need to define the user and amount both, follow this format\n```{prefix(ctx)}givexp <user> <amount>```\nFor user either user can be mentioned or ID can be used.")


    @commands.command()
    async def removexp(self, ctx, user:discord.Member=None, amount:int=None):
        if user and amount is not None:
            if str(ctx.guild.id) in var.LEVELDATABASE.list_collection_names():
                col = var.LEVELDATABASE[str(ctx.guild.id)]
                data = col.find_one({"_id": user.id})

                newdata = {"$set":{
                            "xp": data.get("xp") - amount
                        }}
                var.LEVELDATABASE[str(ctx.guild.id)].update_one(data, newdata)
                await ctx.send(f"Successfully removed {amount} xp from {user}!")
            else:
                embed = discord.Embed(
                title="Can't remove XP from the user",
                description=f"Leveling for this server is not setted up, use the command `{prefix(ctx)} levels to enable leveling",
                color=var.CRED
                )
                await ctx.send(embed=embed)
        else:
            await ctx.send(f"You need to define the user and amount both, follow this format\n```{prefix(ctx)}removexp <user> <amount>```\nFor user either user can be mentioned or ID can be used.")


    @commands.command()
    async def award(self, ctx):
        await ctx.send("Coming soon...")


    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.guild.id) in var.LEVELDATABASE.list_collection_names():
            if var.LEVELDATABASE[str(message.guild.id)].find_one({"_id":0}).get("status") == True:

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
                        ch = self.bot.get_channel(guildlevels.find_one({"_id":0}).get("alertchannel"))
                        await ch.send(f"{message.author.mention} you leveled up to level {level}!")


    @commands.command()
    async def rank(self, ctx, rankuser:discord.Member=None):
        if rankuser is None:
            user = ctx.author
        else:
            user = rankuser

        if str(ctx.guild.id) in var.LEVELDATABASE.list_collection_names():
            guildlevels = var.LEVELDATABASE[str(ctx.guild.id)]
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

                embed = discord.Embed(
                title=f"Level stats for {user.name}",
                description=boxes * "<:blue:808242875933786112>" + (20-boxes) * "<:white:808242875728789525>", 
                color=var.CTEAL
                ).add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True
                ).add_field(name="XP", value=f"{xp}/{int(200*((1/2)*level))}", inline=True
                ).add_field(name="Level", value=level, inline=True
                ).set_thumbnail(url=user.avatar_url
                )
                if var.LEVELDATABASE[str(ctx.guild.id)].find_one({"_id":0}).get("status") == False:
                    embed.set_footer(text="Leveling for this server is disabled this means the xp is still there but members won't gain any new xp")
                await ctx.channel.send(embed=embed)
        else:
            await ctx.send("Leveling is not enabled on this server :(")


    @commands.command()
    async def leaderboard(self, ctx):
        guildlevels = var.LEVELDATABASE[str(ctx.guild.id)]
        if guildlevels is not None:
            rankings = guildlevels.find().sort("xp", -1)
            embed = discord.Embed(
            title=f"Leaderboard for {ctx.guild.name}", 
            color=var.CBLUE
            )
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