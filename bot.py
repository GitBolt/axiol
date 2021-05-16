import os
import discord
import asyncio
import emojis
from discord.ext import commands
from pymongo import MongoClient

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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Get started with #help"))
    print("I'm Ready!")


@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx):
    embed = discord.Embed(title="Prefix for this server",
                        description=f"Hey, the prefix for this server is `#`\n Wanna change it? React to the {emojis.SETTINGS} emoji below!",
                        color=discord.Color.teal())
    message = await ctx.send(embed=embed)
    await message.add_reaction(emojis.SETTINGS)
    await message.add_reaction(emojis.DELETE)
    await asyncio.sleep(1)


    def reactioncheck(reaction, user):
        return str(reaction.emoji) == emojis.SETTINGS or emojis.DELETE and reaction.message == message

    def prefixmsgcheck(message):
        return message.author == ctx.author

    react, user = await bot.wait_for('reaction_add', check=reactioncheck)
    if user == ctx.author:
        if str(react.emoji) != emojis.DELETE:
            try:
                currentprefix = PREFIXES.find_one({"serverid": ctx.author.guild.id}).get("prefix")
            except AttributeError:
                currentprefix = "#"
            await ctx.send(embed=discord.Embed(description="Next message which you will send will become the prefix :eyes:" +
                                            f"To cancel it enter `{currentprefix}cancel`",
                                            color=discord.Color.purple()))
            try:
                userprefix = await bot.wait_for('message', check=prefixmsgcheck, timeout=60.0)
                if userprefix.content == currentprefix+"cancel":
                    await ctx.send("Cancelled prefix change, imagine if this would have been the prefix lol")
                elif userprefix.content != currentprefix+"cancel":
                    if PREFIXES.find_one({"serverid": message.author.guild.id}) is None:
                        PREFIXES.insert_one({"_id": PREFIXES.estimated_document_count()+1, "serverid": ctx.author.guild.id, "prefix": userprefix.content})
                    oldprefix = PREFIXES.find_one({"serverid": message.guild.id})
                    newprefix = {"$set": {"serverid": message.author.guild.id, "prefix": userprefix.content}}
                    PREFIXES.update_one(oldprefix, newprefix)
                    await ctx.send(f"Updated your new prefix, it's `{userprefix.content}` if I am not wrong :eyes:")
            except asyncio.TimeoutError:
                await ctx.send(f"You took too long to enter your new prefix ⏲ {ctx.author.mention}")

        else:
            await message.delete()
            d = await ctx.send("Message deleted :O")
            await asyncio.sleep(1)
            await d.delete()


#Loading Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

#Starting Bot
bot.run(os.environ.get("TOKEN"))