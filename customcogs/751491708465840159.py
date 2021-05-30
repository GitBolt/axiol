import discord
import asyncio
from discord.ext import commands


#Custom cog for Logically Answered discord server | 751491708465840159
class LogicallyAnswered(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to make sure this custom cog only runs on this server
    def cog_check(self, ctx):
        return ctx.guild.id == 751491708465840159

    @commands.command()
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


    #Soon gonna add auto reactions too
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 751491708465840159:

            if str(message.channel) == '💡〢suggestions':
                await message.add_reaction('<:upvote:776831295946620948>')
                await message.add_reaction('<:downvote:776831143453786164>')

            if str(message.channel) == '✋〢video-requests':
                await message.add_reaction('👍')
                await message.add_reaction('👎')

            if str(message.channel) == '👋〢welcome':
                await message.add_reaction('<:elonwave:806962782330552340>')

            if str(message.channel) == '🗳〢vote':
                await message.add_reaction('✅')
                await message.add_reaction('❌')

            if str(message.channel) == '📝〢one-word-story' and message.author.bot == False:
                for i in message.content:

                    if ' ' in i:
                        await message.delete()
                    elif '-' in i:
                        await message.delete()
                    elif '_' in i:
                        await message.delete()


def setup(bot):
    bot.add_cog(LogicallyAnswered(bot))