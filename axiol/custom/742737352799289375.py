import json
import torch
import discord
from discord.ext import commands
import database as db
import variables as var
from functions import getprefix
from chatbot.model import NeuralNet
from chatbot.utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#Custom cog for Chemistry Help discord server | 742737352799289375
class ChemHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to make sure this custom cog only runs on this server
    def cog_check(self, ctx):
        return ctx.guild.id == 742737352799289375


    @commands.command()
    async def addmsg(self, ctx, msg:str=None, response:str=None):
        if msg and response is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 0})
            if data is None:
                GuildCol.insert_one({
                    "_id": 0,
                    msg: response
                })
                await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with response **{response}**"))
            else:
                GuildCol.update({}, {"$set": {msg: response}})
                await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with response **{response}**"))
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define both the message and it's response",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addmsg <msg> <response>`"))



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id in [742849666256732170, 742849666256732170]:
            GuildCol = db.CUSTOMDATABASE[str(message.guild.id)]
            data = GuildCol.find_one({"_id": 0})
            if data is not None:
                if message.content in data.keys():
                    await message.channel.send(data.get(message.content))

    
def setup(bot):
    bot.add_cog(ChemHelp(bot))