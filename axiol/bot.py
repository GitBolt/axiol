import os
import discord
from discord.ext import commands
import database as db
import variables as var


#Function to get current server prefix
def serverprefix(bot, message):
    if db.PREFIXES.find_one({"_id": message.guild.id}) is None:
        return var.DEFAULT_PREFIX
    return db.PREFIXES.find_one({"_id": message.guild.id}).get("prefix")

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = serverprefix, help_command=None, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
                            type=discord.ActivityType.streaming,
                            name=f"Get started with {var.DEFAULT_PREFIX}help"
                            ))
    print("I woke up 🌥️")


#Loading pogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
#Loading visual pogs
for filename in os.listdir('./visuals'):
    if filename.endswith('.py'):
        bot.load_extension(f'visuals.{filename[:-3]}')
#Loading custom pogs
for filename in os.listdir('./customcogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'customcogs.{filename[:-3]}')


@bot.event
async def on_guild_join(guild):
    #Inserting plugin configs if it does not exist (incase of re-inviting)
    if not db.PLUGINS.count_documents({"_id": guild.id}, limit=1):
        db.PLUGINS.insert_one({

            "_id":guild.id,
            "Leveling":True,
            "Moderation": True,
            "Reaction Roles": True,
            "Welcome": False,
            "Verification": False,
            "Chatbot": False,
            "Music": True
        })

    #Inserting leveling data because this is enabled by default 
    if not str(guild.id) in db.LEVELDATABASE.list_collection_names():
        GuildDoc = db.LEVELDATABASE.create_collection(str(guild.id))
        GuildDoc.insert_one({

            "_id": 0,
            "xprange": [15, 25],
            "alertchannel": None,
            "blacklistedchannels": [],
            "alerts": True
            })    

    #Support server Log
    embed = discord.Embed(
    title="I just joined a new server!",
    description=f"Thanks to this kind person for inviting me to **{guild.name}** :D",
    color=var.C_GREEN
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)           

#Support server Log
@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
    title="I just got removed from a server",
    description=f"Someone removed me from **{guild.name}** :(",
    color=var.C_RED
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)    


bot.run(var.TOKEN)
