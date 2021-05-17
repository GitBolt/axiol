import os
import discord
import asyncio
from discord.ext import commands
import utils.emojis as emoji
from utils.vars import DEFAULT_PREFIX, MONGOCLIENT, TOKEN

#Database Fetching
DATABASE = MONGOCLIENT['Axiol']
PREFIXES = DATABASE["Prefixes"] #Prefixes Collection


#Getting Server Prefix
def serverprefix(bot, message):
    if PREFIXES.find_one({"serverid": message.guild.id}) is None:
        return DEFAULT_PREFIX
    return PREFIXES.find_one({"serverid": message.guild.id}).get("prefix")
    
bot = commands.Bot(command_prefix = serverprefix)
bot.remove_command('help')

#Changing presence and alerting on ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Get started with .help or whatever your server prefix is if changed"))
    print("I'm Ready!")

#Loading Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


#Prefix change command
@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx):
    try:
        current_prefix = PREFIXES.find_one({"serverid": ctx.author.guild.id}).get("prefix")
    except AttributeError:
        current_prefix = DEFAULT_PREFIX

    embed = discord.Embed(title="Prefix :D that's the way you control me aye!",
                        description=f"The prefix for this server is ```{current_prefix}```\nWanna change it? React to the {emoji.SETTINGS} emoji below!",
                        color=discord.Color.teal())
    message = await ctx.send(embed=embed)
    await message.add_reaction(emoji.SETTINGS)


    def reactioncheck(reaction, user):
        return str(reaction.emoji) == emoji.SETTINGS and reaction.message == message and user.id == ctx.author.id

    await bot.wait_for('reaction_add', check=reactioncheck)
    await ctx.send(embed=discord.Embed(description="Next message which you will send will become the prefix :eyes:" +
                                    f"To cancel it enter `{current_prefix}cancel`",
                                    color=discord.Color.magenta()))
    await message.clear_reaction(emoji.SETTINGS)

    def prefixmsgcheck(message):
        return message.author.id == ctx.author.id and message.author.guild.id == ctx.author.guild.id

    try:
        message = await bot.wait_for('message', check=prefixmsgcheck, timeout=60.0)

        if message.content == current_prefix+"cancel":
            await ctx.send("Cancelled prefix change.")
        else:
            if current_prefix == DEFAULT_PREFIX:
                PREFIXES.insert_one({"_id": PREFIXES.estimated_document_count()+1, "serverid": ctx.author.guild.id, "prefix": message.content})
            else:
                oldprefix = PREFIXES.find_one({"serverid": message.guild.id})
                newprefix = {"$set": {"serverid": message.author.guild.id, "prefix": message.content}}
                
                PREFIXES.update_one(oldprefix, newprefix)
                await ctx.send(f"Updated your new prefix, it's ```{message.content}```")

    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to enter your new prefix ⏲ {ctx.author.mention}")
            

#Starting Bot
bot.run(TOKEN)