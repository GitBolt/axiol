import discord
from discord.ext import commands, tasks
import string
import requests
import variables as var

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

        
    @commands.command()
    async def storystart(self, ctx):
        onewordstory.start(self, ctx)
    await ctx.send(f"{var.E_ENABLE} Started the background proccess for one word story")

    @commands.command()
    async def storystop(self, ctx):
        onewordstory.stop(self, ctx)
        await ctx.send(f"{var.E_DISABLE} Stopped the background proccess for one word story")


    #Soon gonna add auto reactions too
    @commands.Cog.listener()
    async def on_message(self, message):
        
        def messagecheck(msg):
            allowed = list(string.ascii_lowercase + string.digits)
            return msg <= allowed
            
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

            if (str(message.channel) == '📝〢one-word-story' and 
                message.author.bot == False and message.author.id != 791950104680071188):
                last_message = await message.channel.history(limit=2).flatten()
                last_message_author = last_message[1].author

                if last_message_author == message.author:
                    await message.channel.send(f"{message.author.mention} You can't send two messages in a row! Wait for someone else to send a message first", delete_after=5)
                if (not list(message.content) <= list(string.ascii_lowercase + string.digits)or
                    last_message_author == message.author):
                    try:
                        await message.delete()
                    except:
                        pass



@tasks.loop(hours=12)
async def onewordstory(self, ctx):
    channel = self.bot.get_channel(803308171577393172)
    botmsg = await channel.history().find(lambda m: m.author == self.bot.user)

    storymessages = await channel.history(after=botmsg).flatten()
    wholestory = ""
    for msg in storymessages:
        wholestory += msg.content + ' '

    word = requests.get("https://random-word-api.herokuapp.com/word?number=1")

    embed = discord.Embed(
            title=f"New word: {word.json()[0]}",
            description=f"Previous story: `{wholestory}`",
            color=var.C_MAIN
    ).set_footer(text='After 12 hours I will combine all the words and form a story and then send a new word to start a new story!')

    await channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(LogicallyAnswered(bot))