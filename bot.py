import os
import discord
import asyncio
from discord.ext import commands
import utils.vars as var


def serverprefix(bot, message):
    if var.PREFIXES.find_one({"serverid": message.guild.id}) is None:
        return var.DEFAULT_PREFIX
    return var.PREFIXES.find_one({"serverid": message.guild.id}).get("prefix")
    
bot = commands.Bot(command_prefix = serverprefix)
bot.remove_command('help')


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


@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx):
    try:
        current_prefix = var.PREFIXES.find_one({"serverid": ctx.guild.id}).get("prefix")
    except AttributeError:
        current_prefix = var.DEFAULT_PREFIX

    embed = discord.Embed(title="Prefix :D that's the way you control me aye!",
                        description=f"The prefix for this server is\n```{current_prefix}```\nWanna change it? React to the {var.SETTINGS} emoji below!",
                        color=var.MAGENTA)
    message = await ctx.send(embed=embed)
    await message.add_reaction(var.SETTINGS)

    def reactioncheck(reaction, user):
        return str(reaction.emoji) == var.SETTINGS and reaction.message == message and user.id == ctx.author.id

    await bot.wait_for('reaction_add', check=reactioncheck)
    await ctx.send(embed=discord.Embed(description="Next message which you will send will become the prefix :eyes:\n"+
                                    f"To cancel it enter\n```{current_prefix}cancel```",
                                    color=var.ORANGE))
    await message.clear_reactions()

    def prefixmsgcheck(message):
        return message.author.id == ctx.author.id and message.guild.id == ctx.guild.id

    try:
        message = await bot.wait_for('message', check=prefixmsgcheck, timeout=60.0)

        if message.content == current_prefix+"cancel":
            await ctx.send("Cancelled prefix change.")
            
        elif message.content == var.DEFAULT_PREFIX:
            var.PREFIXES.delete_one({"serverid": ctx.guild.id})
            await ctx.send(f"Changed your prefix to the default one\n```{var.DEFAULT_PREFIX}```")

        elif current_prefix == var.DEFAULT_PREFIX:
            var.PREFIXES.insert_one({"_id": var.PREFIXES.estimated_document_count()+1, "serverid": ctx.guild.id, "prefix": message.content})
            await ctx.send(f"Updated your new prefix, it's\n```{message.content}```")

        else:
            oldprefix = var.PREFIXES.find_one({"serverid": message.guild.id})
            newprefix = {"$set": {"serverid": message.guild.id, "prefix": message.content}}
            
            var.PREFIXES.update_one(oldprefix, newprefix)
            await ctx.send(f"Updated your new prefix, it's\n```{message.content}```")

    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to enter your new prefix {ctx.author.mention} ;-;")
            


bot.run(var.TOKEN)