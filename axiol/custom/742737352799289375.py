import json
import torch
import discord
from discord.ext import commands
import database as db
import variables as var
from functions import getprefix
from discord.ext.commands import check, Context
from chatbot.model import NeuralNet
from chatbot.utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')




#Custom cog for Chemistry Help discord server | 742737352799289375
class ChemHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to make sure this custom cog only runs on this server
    def cog_check(self, ctx):
        return ctx.guild.id == 742737352799289375 or 807140294276415510


    @commands.command()
    async def addmsg(self, ctx, *, msg:str=None):
        if ctx.author.id in [565059698399641600, 791950104680071188] and msg is not None:

            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 0})
            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()
                GuildCol.insert_one({
                    "_id": 0,
                   trigger: response
                })
                await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with response **{response}**", color=var.C_BLUE))
            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()

                GuildCol.update(data, {"$set": {trigger: response}})
                await ctx.send(embed=discord.Embed(description=f"Added the message **{trigger}** with response **{response}**", color=var.C_BLUE))
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define both the message and it's response",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addmsg <msg> | <response>`"))



    @commands.command()
    async def addreaction(self, ctx, *, msg:str=None):
        if ctx.author.id in [565059698399641600, 791950104680071188] and msg is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 1})
            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with reaction **{emoji}**", color=var.C_BLUE))
                except :
                    await ctx.send("Sorry but it seems like either the emoji is invalid or it's a custom emoji from a server where I am not in hence can't use this emoji either :(")
                
                GuildCol.insert_one({
                    "_id": 1,
                   trigger: emoji
                })
            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with reaction **{emoji}**", color=var.C_BLUE))
                except :
                    await ctx.send("Sorry but it seems like either the emoji is invalid or it's a custom emoji from a server where I am not in hence can't use this emoji either :(")

                GuildCol.update(data, {"$set": {trigger: emoji}})
                
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define both the message and it's reaction",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addreaction <msg> <emoji>`"))




    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id in [742848285416357970, 742849666256732170, 844657766794788884, 846840113543905383]:

            GuildCol = db.CUSTOMDATABASE[str(message.guild.id)]
            msgdata = GuildCol.find_one({"_id": 0})
            reactiondata = GuildCol.find_one({"_id": 1})
            if msgdata is not None:
                for trigger in msgdata.keys():
                    if trigger in message.content.lower():
                        await message.channel.send(msgdata.get(trigger))

            if reactiondata is not None:
                for trigger in reactiondata.keys():
                    if trigger in message.content.lower():
                        await message.add_reaction(reactiondata.get(trigger))      

    
def setup(bot):
    bot.add_cog(ChemHelp(bot))