import random
import json
import discord
import torch
from discord.ext import commands
from utils.functions import getprefix
import utils.database as db
import utils.variables as var
from chatbot.model import NeuralNet
from chatbot.utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot") == True:
            return ctx.guild.id


    @commands.command()
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
            await ctx.send(f"Successfully added {channel.mention}")
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the channel in order to make it bot chat",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}setchatbot <#channel>`"
            )
            )

    
    @commands.command()
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
                await ctx.send(f"removed {channel.mention}")
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

    @commands.Cog.listener()
    async def on_message(self, message):
        GuildChatbotDoc = db.CHATBOT.find_one({"_id": message.guild.id})
        try:
            if f'<@!{self.bot.user.id}>' in message.content or message.channel.id in GuildChatbotDoc.get("channels") and message.author.bot == False:

                with open('chatbot/intents.json', 'r') as json_data:
                    intents = json.load(json_data)

                FILE = "chatbot/data.pth"
                data = torch.load(FILE, map_location='cpu')

                input_size = data["input_size"]
                hidden_size = data["hidden_size"]
                output_size = data["output_size"]
                all_words = data['all_words']
                tags = data['tags']
                model_state = data["model_state"]

                model = NeuralNet(input_size, hidden_size, output_size).to(device)
                model.load_state_dict(model_state)
                model.eval()

                sentence = message.content.strip(f"<@!{self.bot.user.id}>")
                sentence = tokenize(sentence)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)

                tag = tags[predicted.item()]
                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]
                print(prob.item())
                if prob.item() > 0.9:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            await message.channel.send(random.choice(intent['responses']))


                elif prob.item() > 0.4:
                    await message.channel.send(random.choice([
                        "Okay so I gotta agree, I'm dumb and I wasn't able to understand what you said ;-;",
                        "Can you word this a bit differently, I couldn't understand",
                        "Hmmm?",
                    ]))

                else:
                    await message.channel.send(random.choice([
                        "What?",
                        "Sorry what?",
                        "?",
                        "Didn't understand",
                        "Huh",
                    ]))
                            
        except AttributeError:
            pass


def setup(bot):
    bot.add_cog(Chatbot(bot))

