import discord
from discord.ext import commands


def LogicalCheck():
    async def predicate(ctx):
        return ctx.guild.id == 751491708465840159
    return commands.check(predicate)

#Custom cog for Logically Answered discord server | 751491708465840159
class LogicallyAnswered(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @LogicalCheck()
    async def poll(self, ctx, *, msg:str=None):
        role = discord.utils.find(lambda r: r.name == 'Level 30+', ctx.message.guild.roles)

        if msg != None and role in ctx.author.roles:
            channel = self.bot.get_channel(789214004950204416) #Polls channel
            embed = discord.Embed(title=f"{ctx.author.name} asks:", description=msg, color=discord.Colour.green())
            msg = await channel.send(content='<@&789216491090346025>', embed=embed)
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            await msg.add_reaction("🤷‍♂️")

        elif msg == None and not role in ctx.author.roles:
            await ctx.send("You neither specified your message nor you are level 30+, sorry you can't use the command right now.")
        
        elif msg == None:    
            await ctx.send("__You need to specify the message to start a poll!__\n Format: ```!poll <yourmessage>```")
        
        elif not role in ctx.author.roles:
            await ctx.send("You don't have level 30+ role yet, you can't use the command right now.")


def setup(bot):
    bot.add_cog(LogicallyAnswered(bot))