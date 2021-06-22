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
        return ctx.guild.id == 742737352799289375 or 807140294276415510


    @commands.command()
    async def addmsg(self, ctx, *, msg:str=None):
        if msg is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 0})
            if data is None:
                trigger = msg.split("|")[0].remove(" ")
                response = msg.split("|")[1].remove(" ")
                GuildCol.insert_one({
                    "_id": 0,
                   trigger: response
                })
                await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with response **{response}**", color=var.C_BLUE))
            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ')
                response = msg.split("|")[1].lstrip(' ').rstrip(' ')

                print(trigger)
                print(response)

                GuildCol.update({}, {"$set": {trigger: response}})
                await ctx.send(embed=discord.Embed(description=f"Added the message **{trigger}** with response **{response}**", color=var.C_BLUE))
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define both the message and it's response",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addmsg <msg> <response>`"))



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id in [742848285416357970, 742849666256732170, 844657766794788884, 846840113543905383]:
            GuildCol = db.CUSTOMDATABASE[str(message.guild.id)]
            data = GuildCol.find_one({"_id": 0})
            if data is not None:
                print(data.keys())
                if message.content in data.keys():
                    await message.channel.send(data.get(message.content))

    
def setup(bot):
    bot.add_cog(ChemHelp(bot))