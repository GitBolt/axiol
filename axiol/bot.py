import os
from dotenv import load_dotenv
import disnake


from disnake.ext import commands
import database as db
import constants as var

load_dotenv()


async def guild_prefix(_bot, message):
    """Return current guild prefix"""
    if not message.guild:
        return var.DEFAULT_PREFIX

    prefix_doc = await db.PREFIXES.find_one({"_id": message.guild.id})
    if prefix_doc is None:
        return var.DEFAULT_PREFIX
    return prefix_doc["prefix"]


intents = disnake.Intents().all()
bot = commands.Bot(command_prefix=guild_prefix, help_command=None, intents=intents)


@bot.event
async def on_ready():

    await bot.change_presence(
        activity=disnake.Activity(
            type=disnake.ActivityType.streaming, name=f".help"
        )
    )
    print("gm 🌥️")


# Loading pogs
for filename in os.listdir("./custom"):
    if filename.endswith(".py"):
        bot.load_extension(f"custom.{filename[:-3]}")

for filename in os.listdir("./ext"):
    if filename.endswith(".py"):
        bot.load_extension(f"ext.{filename[:-3]}")

for filename in os.listdir("./plugins"):
    if filename.endswith(".py"):
        bot.load_extension(f"plugins.{filename[:-3]}")

for filename in os.listdir("./visuals"):
    if filename.endswith(".py"):
        bot.load_extension(f"visuals.{filename[:-3]}")

bot.run(var.TOKEN)
