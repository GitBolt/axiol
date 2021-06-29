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
for filename in os.listdir('./custom'):
    if filename.endswith('.py'):
        bot.load_extension(f'custom.{filename[:-3]}')

for filename in os.listdir('./ext'):
    if filename.endswith('.py'):
        bot.load_extension(f'ext.{filename[:-3]}')

for filename in os.listdir('./plugins'):
    if filename.endswith('.py'):
        bot.load_extension(f'plugins.{filename[:-3]}')

for filename in os.listdir('./visuals'):
    if filename.endswith('.py'):
        bot.load_extension(f'visuals.{filename[:-3]}')



@bot.event
async def on_guild_join(guild):
    #Inserting plugin configs if it does not exist (incase of re-inviting)
    if not db.PLUGINS.count_documents({"_id": guild.id}, limit=1):
        db.PLUGINS.insert_one({

            "_id": guild.id,
            "Leveling": False,
            "Moderation": True,
            "Reaction Roles": True,
            "Welcome": False,
            "Verification": False,
            "Chatbot": True,
            "Music": True,
        })

    #Support server Log
    embed = discord.Embed(
    title="I just joined a new server!",
    description=f"Thanks to this kind person for inviting me to `{guild.name}` :D",
    color=var.C_GREEN
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)           


#Support server Log
@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
    title="I just got removed from a server",
    description=f"Someone removed me from `{guild.name}` :(",
    color=var.C_RED
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)    


bot.run(var.TOKEN)
