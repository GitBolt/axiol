import os
import discord
from discord.ext import commands
import utils.vars as var


#Function to get current server prefix
def serverprefix(bot, message):
    if var.PREFIXES.find_one({"serverid": message.guild.id}) is None:
        return var.DEFAULT_PREFIX
    return var.PREFIXES.find_one({"serverid": message.guild.id}).get("prefix")

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = serverprefix, help_command=None, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(
                            type=discord.ActivityType.streaming,
                            name=f"Get started with {var.DEFAULT_PREFIX}help"
                            ))
    print("I'm Ready!")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

for filename in os.listdir('./customcogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'customcogs.{filename[:-3]}')


@bot.event
async def on_guild_join(guild):
    #Inserting plugin configs if it does not exist (incase of re inviting)
    if not var.PLUGINS.count_documents({"_id":guild.id}, limit=1):
        var.PLUGINS.insert_one({

            "_id":guild.id,

            "Leveling":True,
            "Moderation": True,
            "Reaction Roles": True,
            "Verification": False,
            "Welcome": False,
        })
    #Inserting leveling data if it does not exist (incase of re inviting) 
    if not str(guild.id) in var.LEVELDATABASE.list_collection_names():
        GuildDoc = var.LEVELDATABASE.create_collection(str(guild.id))
        GuildDoc.insert_one({

            "_id": 0,
            "xprange": [15, 25],
            "alertchannel": None,
            "blacklistedchannels": [],
            })    

    #Support server Log channel ID
    embed = discord.Embed(
    title="I just joined a new server!",
    description=f"Thanks to this pog person for inviting me to **{guild.name}** :D",
    color=var.CGREEN
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)           


@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
    title="I just got removed from a server",
    description=f"Someone removed me from **{guild.name}** :(",
    color=var.CRED
    ).add_field(name="Member count", value=guild.member_count
    )
    await bot.get_channel(848207106821980213).send(embed=embed)    


# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CheckFailure):
#         pass


bot.run(var.TOKEN)