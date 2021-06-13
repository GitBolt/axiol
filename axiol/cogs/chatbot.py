import discord
from discord.ext import commands
from functions import getprefix
import database as db
import variables as var


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Chatbot plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @commands.command(aliases=["enablechatbot"])
    async def setchatbot(self, ctx, channel:discord.TextChannel=None):

        if db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            db.CHATBOT.insert_one({
                "_id": ctx.guild.id,
                "channels": []                                    
                })

        if channel is not None:
            GuildDoc = db.CHATBOT.find_one({"_id": ctx.guild.id})
            channelist = GuildDoc.get("channels")
            newlist = channelist.copy()
            newlist.append(channel.id)
            print(newlist)
            newdata = {"$set":{
                "channels": newlist
            }}

            db.CHATBOT.update_one(GuildDoc, newdata)
            await ctx.send(f"Enabled Chatbot for {channel.mention}")
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the channel in order to make it bot chat",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}setchatbot <#channel>`"
            )
            )

    
    @commands.command(aliases=["disablechatbot"])
    async def removechatbot(self, ctx, channel:discord.TextChannel=None):

        if db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            db.CHATBOT.insert_one({
                "_id": ctx.guild.id,
                "channels": []                                    
                })
        if channel is not None:
            GuildDoc = db.CHATBOT.find_one({"_id": ctx.guild.id})
            if channel.id in GuildDoc.get("channels"):
                channelist = GuildDoc.get("channels")
                newlist = channelist.copy()
                newlist.remove(channel.id)
                newdata = {"$set":{
                    "channels": newlist
                }}
                db.CHATBOT.update_one(GuildDoc, newdata)
                await ctx.send(f"Disabled Chatbot from {channel.mention}")
            else:
                await ctx.send("This channel is not a bot chatting channel")
        else:   
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the channel in order to remove bot chat",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}removechatbot <#channel>`"
            )
            )


    @commands.command()
    async def chatbotchannels(self, ctx):
        GuildDoc = db.CHATBOT.find_one({"_id": ctx.guild.id})
        embed = discord.Embed(
            title="All chatbot channels in this server",
            color=var.C_TEAL
        )
        if GuildDoc.get("channels") != []:
            for i in GuildDoc.get("channels"):
                embed.add_field(name="** **", value=self.bot.get_channel(i).mention)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have any chat bot channel")



def setup(bot):
    bot.add_cog(Chatbot(bot))

