import discord
from discord.ext import commands, tasks
import string
from discord.guild import Guild
import requests
import variables as var
import database as db

#Custom cog for Global Advertisementdiscord server | 855796269204242432
class GlobalAdvertisement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to make sure this custom cog only runs on this server
    def cog_check(self, ctx):
        return ctx.guild.id == 855796269204242432


    @commands.command()
    async def ga_addrole(self, ctx, imgcount:str=None, role:discord.Role=None):
        if imgcount and role is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            settings = GuildCol.find_one({"_id": 0})
            if settings is None:
                GuildCol.insert_one({
                    "_id": 0,
                    "rewards": {
                        imgcount: role.id
                    },
                    "blacklist": []
                })
                await ctx.send(embed=discord.Embed(description=f"Added {role.mention} for {imgcount} amount of images!", color=var.C_GREEN))
            else:
                current = settings.get("rewards")
                newdict = current.copy()
                newdict.update({imgcount: role.id})
                newdata = {"$set":{
                    "rewards": newdict
                }}

                GuildCol.update_one(settings, newdata)
                await ctx.send(embed=discord.Embed(description=f"Added {role.mention} for {imgcount} amount of images!", color=var.C_GREEN))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to describe both image count and role to reward users!",
                color=var.C_RED
            ).add_field(name="Format", value="`.addrole <image_count> <role>`"
            ).set_footer(text="For role either the role ID or role mention can be used")
            )

    @commands.command()
    async def ga_removerole(self, ctx, imgcount:str=None):
        if imgcount is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            settings = GuildCol.find_one({"_id": 0})
            if settings is None:
                await ctx.send("This server does not have any setting yet")
            else:
                current = settings.get("rewards")
                newdict = current.copy()
                newdict.pop(imgcount)
                newdata = {"$set":{
                    "rewards": newdict
                }}

                GuildCol.update_one(settings, newdata)
                await ctx.send(embed=discord.Embed(description=f"Removed role for {imgcount} images", color=var.C_GREEN))
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to describe both image count and role to reward users!",
                color=var.C_RED
            ).add_field(name="Format", value="`.removerole <image_count> `"
            ).set_footer(text="For role either the role ID or role mention can be used")
            )


    @commands.command()
    async def ga_blacklist(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            settings = GuildCol.find_one({"_id": 0})
            if settings is None:
                GuildCol.insert_one({
                    "_id": 0,
                    "rewards": {},
                    "blacklist": [channel.id]
                })
            else:
                current = settings.get("blacklist")
                newlist = current.copy()
                newlist.append(channel.id)
                newdata = {"$set":{
                    "blacklist": newlist
                }}
                GuildCol.update_one(settings, newdata)
                await ctx.send(f"Blacklisted {channel.mention}")

        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to describe the channel in order to blacklist it!",
                color=var.C_RED
            ).add_field(name="Format", value="`.blacklist <#channel>`")) 


    @commands.command()
    async def ga_top(self, ctx):
        GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
        if GuildCol is not None:
            embed = discord.Embed(title="Top users", color=var.C_MAIN)
            for i in GuildCol.find({"_id": { "$ne": 0 },}).sort("imgcount", -1):
                embed.add_field(name=ctx.guild.get_member(i.get("_id")), value=i.get("imgcount"), inline=False)
        
            await ctx.send(embed=embed)

        else:
            await ctx.send("No one has any messages yet...")


    @commands.command()
    async def ga_settings(self, ctx):
        GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
        if GuildCol is not None:
            rewards = GuildCol.find_one({"_id": 0}).get("rewards")

            embed = discord.Embed(title="Settings", color=var.C_BLUE)
            for i in rewards:
                embed.add_field(name=i, value=ctx.guild.get_role(int(rewards.get(i))).mention)
        
            await ctx.send(embed=embed)


    @commands.command()
    async def ga_remove(self, ctx, user:discord.User=None):
        if user is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            if GuildCol is not None:
                GuildCol.delete_one({"_id":user.id})
                await ctx.send(f"Successfully removed all messages by {user.name}")
        else:
            await ctx.send(embed=discord.Embed(
                title="Not enough arguments",
                description="You need to describe the user in order to remove it!",
                color=var.C_RED
            ).add_field(name="Format", value="`.remove <user>`")) 

    @commands.command()
    async def ga_help(self, ctx):
        embed = discord.Embed(
            title="All help commands for this server",
            color=var.C_MAIN
        )
        embed.add_field(name=".ga_addrole `<image_count>` `<role>`", value="Add a role which users will get for sending certain amount of images")
        embed.add_field(name=".ga_removerole `<image_count>`", value="Remove a role which users will get for sending certain amount of images")
        embed.add_field(name=".ga_blacklist `<#channel>`", value="Blacklist a channel where users won't gain anything")
        embed.add_field(name=".ga_top", value="Shows top users")
        embed.add_field(name=".settings", value="Shows current settings")
        embed.add_field(name=".ga_remove `<user>`", value="Remove all image count from a user")
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        GuildCol = db.CUSTOMDATABASE[str(message.guild.id)]
        settings = GuildCol.find_one({"_id": 0})

        if settings is not None and message.author.bot == False:
            if not message.channel.id in settings.get("blacklist"):
                userdata = GuildCol.find_one({"_id": message.author.id})
                if userdata is None:
                    GuildCol.insert_one({"_id": message.author.id, "imgcount": 0})
                else:
                    existingcount = userdata.get("imgcount")
                    newcount = existingcount
                    newcount += 1
                    newdata = {"$set":{
                        "imgcount": newcount
                    }}
                    GuildCol.update_one(userdata, newdata)
                    if str(userdata.get("imgcount")) in GuildCol.find_one({"_id":0}).get("rewards").keys():
                        rewards = GuildCol.find_one({"_id":0}).get("rewards")
                        roleid = rewards.get(str(userdata.get("imgcount")))
                        role = message.guild.get_role(roleid)
                        
                        prev_key = list(rewards)[list(rewards).index(str(userdata.get("imgcount")))-1]
                        
                        remroleid = rewards.get(prev_key)
                        remrole = message.guild.get_role(int(remroleid))

                        await message.channel.send(content=message.author.mention, embed=discord.Embed(description=f"You just earned {role.mention}!", color=var.C_GREEN))
                        if role not in message.author.roles:
                            await message.author.add_roles(role)   
                            try:
                                if not str(list(rewards.keys())[0]) == str(userdata.get("imgcount")):
                                    await message.author.remove_roles(remrole)
                            except:
                                pass



def setup(bot):
    bot.add_cog(GlobalAdvertisement(bot))