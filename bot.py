import os
import discord
import asyncio
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix

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


@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx):
    embed = discord.Embed(
    title="Prefix :D that's the way you control me aye!",
    description=f"The prefix for this server is\n```{getprefix(ctx)}```\nWanna change it? React to the {var.SETTINGS} emoji below!",
    color=var.CMAIN
    )
    botmsg = await ctx.send(embed=embed)
    await botmsg.add_reaction(var.SETTINGS)

    def reactioncheck(reaction, user):
        return user == ctx.author and reaction.message == botmsg

    await bot.wait_for('reaction_add', check=reactioncheck)
    await ctx.send(embed=discord.Embed(
                description="Next message which you will send will become the prefix :eyes:\n"+
                f"To cancel it enter\n```{getprefix(ctx)}cancel```",
                color=var.CORANGE
                ).set_footer(text="Automatic cancel after 1 minute")
                )
    await botmsg.clear_reactions()

    def prefixmsgcheck(message):
        return message.author == ctx.author and message.channel.id == ctx.channel.id

    try:
        usermsg = await bot.wait_for('message', check=prefixmsgcheck, timeout=60.0)

        if usermsg.content == getprefix(ctx)+"cancel":
            await ctx.send("Cancelled prefix change.")
            
        elif usermsg.content == var.DEFAULT_PREFIX:
            var.PREFIXES.delete_one({"serverid": ctx.guild.id})
            await ctx.send(f"Changed your prefix to the default one\n```{var.DEFAULT_PREFIX}```")

        elif getprefix(ctx) == var.DEFAULT_PREFIX: #New prefix change if our current prefix is default one
            var.PREFIXES.insert_one({"_id": var.PREFIXES.estimated_document_count()+1, "serverid": ctx.guild.id, "prefix": usermsg.content})
            await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

        else:
            oldprefix = var.PREFIXES.find_one({"serverid": usermsg.guild.id})
            newprefix = {"$set": {"serverid": usermsg.guild.id, "prefix": usermsg.content}}
            
            var.PREFIXES.update_one(oldprefix, newprefix)
            await ctx.send(f"Updated your new prefix, it's\n```{usermsg.content}```")

    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to enter your new prefix {ctx.author.mention} ;-;")
            

bot.run(var.TOKEN)