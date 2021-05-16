import os
import discord
import json
from discord.ext import commands
from pymongo import MongoClient

#getting server prefixes
def serverprefixes(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix = serverprefixes)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Get started with #help"))
    print("I'm Ready!")


#simple json file prefixes, soon to be switched to mongodb
@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "#"
    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

@bot.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)


#loading cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#starting bot
bot.run(os.environ.get("TOKEN"))