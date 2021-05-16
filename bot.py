import os
import discord
import asyncio
from discord.ext import commands
from pymongo import MongoClient
import emojis

#Database Fetching
MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL"))
DATABASE = MONGOCLIENT['Axiol']
PREFIXES = DATABASE["Prefixes"] #Prefixes Collection


#Getting Server Prefix
def serverprefix(bot, message):
    if PREFIXES.find_one({"serverid": message.guild.id}) is None:
        return "#"
    return PREFIXES.find_one({"serverid": message.guild.id}).get("prefix")
    
bot = commands.Bot(command_prefix = serverprefix)
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name="Get started with #help"))
    print("I'm Ready!")


@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx):
    embed = discord.Embed(title="Prefix for this server",
                        description=f"Hey, the prefix for this server is `#`\n Wanna change it? React to the {emojis.SETTINGS} emoji below!",
                        color=discord.Color.teal())
    message = await ctx.send(embed=embed)
    await message.add_reaction(emojis.SETTINGS)
    await asyncio.sleep(1)

    def reactioncheck(reaction, user):
        return str(reaction.emoji) == emojis.SETTINGS and reaction.message == message and reaction.me == True
    react = await bot.wait_for('reaction_add', check=reactioncheck)
    if react:  
        await ctx.send(embed=discord.Embed(description="Send the prefix and I will change it, don't send anything, *just your prefix*", color=discord.Color.purple()))

    def prefixmsgcheck(message):
        return message.author == ctx.author
    try:
        userprefix = await bot.wait_for('message', check=prefixmsgcheck, timeout=60.0)
        if PREFIXES.find_one({"serverid": message.guild.id}) is None:
            PREFIXES.insert_one({"_id": PREFIXES.estimated_document_count()+1, "serverid": ctx.author.guild.id, "prefix": userprefix.content})
        oldprefix = PREFIXES.find_one({"serverid": message.guild.id})
        newprefix = {"$set": {"serverid": message.guild.id, "prefix": userprefix.content}}
        PREFIXES.update_one(oldprefix, newprefix)
        await ctx.send(f"Updated your new prefix, it's `{userprefix.content}` if I am not wrong :eyes:")
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to enter your prefix ⏲")


#Loading Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#Starting Bot
bot.run(os.environ.get("TOKEN"))