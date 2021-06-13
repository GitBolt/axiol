import json
import torch
import random
import discord
from discord.ext import commands
import database as db
import variables as var
from greetings import greeting
from functions import getprefix, getxprange
from chatbot.model import NeuralNet
from chatbot.utils import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def sendresponse(ctx, tag, responselist):
    choice = random.choice(responselist)
    if tag == "prefix":
        choice = choice.replace("~", getprefix(ctx))

    return choice


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        GuildVerifyDoc = db.VERIFY.find_one({"_id": member.guild.id})
        GuildWelcomeDoc = db.WELCOME.find_one({"_id": member.guild.id})

        #Verification Stuff
        if db.PLUGINS.find_one({"_id": member.guild.id}).get("Verification") == True:
            roleid = GuildVerifyDoc.get("roleid")
            unverifiedrole = member.guild.get_role(roleid)

            await member.add_roles(unverifiedrole)

        #Welcome stuff
        servers = []
        for i in db.PLUGINS.find({"Welcome": True}):
            servers.append(i.get("_id"))

        if member.guild.id in servers:
            channel = self.bot.get_channel(GuildWelcomeDoc.get("channelid"))

            embed = discord.Embed(
            title="Welcome to the server!",
            description=GuildWelcomeDoc.get("greeting"),
            color=discord.Colour.random()
            ).set_image(url=GuildWelcomeDoc.get("image"))

            await channel.send(content=greeting(member.mention), embed=embed)

            autoroles = GuildWelcomeDoc.get("assignroles")
            if autoroles != []:
                for i in autoroles:
                    autorole = member.guild.get_role(i)
                    await member.add_roles(autorole)



    @commands.Cog.listener()
    async def on_message(self, message):
        GuildPluginLevelingDoc = db.PLUGINS.find_one({"_id": message.guild.id})

        if GuildPluginLevelingDoc.get("Leveling") == True and message.author.bot == False:
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
                        if ch is not None:
                            await ch.send(f"{message.author.mention} you leveled up to level {levelnow}!")
                        else:
                            embed = discord.Embed(
                            title="You leveled up!",
                            description=f"{var.E_ACCEPT} You are now level {levelnow}!",
                            color=var.C_MAIN
                            )
                            await message.channel.send(content=message.author.mention, embed=embed)

        
        GuildChatbotDoc = db.CHATBOT.find_one({"_id": message.guild.id})

        def channels():
            if GuildChatbotDoc is not None and GuildChatbotDoc.get("channels") != []:
                channels = GuildChatbotDoc.get("channels")
            else:
                channels = []
            return channels

        if (f'<@!{843484459113775114}>' in message.content and message.author.bot == False
        or message.channel.id in channels() and message.author.bot == False):

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

            sentence = message.content.strip(f"<@!{843484459113775114}>") #Removing the bot ping
            sentence = tokenize(sentence)
            X = bag_of_words(sentence, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted = torch.max(output, dim=1)

            tag = tags[predicted.item()]
            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            if prob.item() > 0.85:
                for intent in intents['intents']:
                    if tag == intent["tag"]:
                        await message.channel.send(sendresponse(message, tag, intent["responses"]))

            else:
                await self.bot.get_channel(843516136540864512).send(embed=discord.Embed(description={message.content},color=var.C_MAIN))    
                await message.channel.send(random.choice([
                    "What?",
                    "Sorry what?",
                    "?",
                    "Didn't understand",
                    "Huh",
                    ":face_with_raised_eyebrow:",
                    "what",
                    "Can you say that differently?"
                ]))


def setup(bot):
    bot.add_cog(Events(bot))