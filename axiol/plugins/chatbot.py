import discord
from aiohttp import request
from discord.ext import commands
import database as db
import variables as var
from functions import get_prefix
from ext.permissions import has_command_permission


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = await db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Chatbot"):
            return True
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Chatbot plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @commands.command(aliases=["enablechatbot"])
    @has_command_permission()
    async def setchatbot(self, ctx, channel:discord.TextChannel=None):
    
        if await db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            await db.CHATBOT.insert_one({
                "_id": ctx.guild.id,
                "channels": [ctx.channel.id]                                    
                })
        if channel is None:
            channel = ctx.channel
            
         GuildDoc = await db.CHATBOT.find_one({"_id": ctx.guild.id})
         channelist = GuildDoc.get("channels")
         newlist = channelist.copy()
         newlist.append(channel.id)
         newdata = {"$set":{
             "channels": newlist
         }}

         await db.CHATBOT.update_one(GuildDoc, newdata)
         await ctx.send(f"{var.E_ACCEPT} Enabled Chatbot for {channel.mention}")
    

    @commands.command(aliases=["disablechatbot"])
    @has_command_permission()
    async def removechatbot(self, ctx, channel:discord.TextChannel=None):

        if await db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            await db.CHATBOT.insert_one({
                "_id": ctx.guild.id,
                "channels": []                                    
                })
        if channel is None:
            channel = ctx.channel

        GuildDoc = await db.CHATBOT.find_one({"_id": ctx.guild.id})
        if channel.id in GuildDoc.get("channels"):
            channelist = GuildDoc.get("channels")
            newlist = channelist.copy()
            newlist.remove(channel.id)
            newdata = {"$set":{
                "channels": newlist
            }}
            await db.CHATBOT.update_one(GuildDoc, newdata)
            await ctx.send(f"Disabled Chatbot from {channel.mention}")
        else:
            await ctx.send("This channel is not a bot chatting channel")


    @commands.command()
    @has_command_permission()
    async def chatbotchannels(self, ctx):
        GuildDoc = await db.CHATBOT.find_one({"_id": ctx.guild.id})
        embed = discord.Embed(
            title="All chatbot channels in this server",
            color=var.C_TEAL
        )
        if GuildDoc is not None and GuildDoc.get("channels") != []:
            for i in GuildDoc.get("channels"):
                embed.add_field(name="** **", value=self.bot.get_channel(i).mention)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This server does not have any chat bot channel")


    @commands.command()
    @has_command_permission()
    async def chatbotreport(self, ctx, *, desc):
        channel = self.bot.get_channel(843548616505294848) #Support server suggestions channel
        await channel.send(embed=discord.Embed(
            title="Chatbot suggestion",
            description=desc,
            color=var.C_MAIN
        ).add_field(name="By", value=ctx.author
        ).add_field(name="Guild ID", value=ctx.guild.id)
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        GuildPluginDoc = await db.PLUGINS.find_one({"_id": message.guild.id})
        ctx = await self.bot.get_context(message)

        if GuildPluginDoc["Chatbot"]:
            GuildChatbotDoc = await db.CHATBOT.find_one({"_id": message.guild.id})
            def channels():
                if GuildChatbotDoc is not None and GuildChatbotDoc.get("channels") != []:
                    channels = GuildChatbotDoc.get("channels")
                else:
                    channels = []
                return channels

            if (self.bot.user in message.mentions and message.author.bot == False
            or message.channel.id in channels() and message.author.bot == False):
                
                content = message.content.replace("<@!843484459113775114>", "")
                async with request("POST", f"https://axiol.up.railway.app/ai/chatbot", json={"content": content}) as response:
                    res = await response.json()

                if res["response"] == "help":
                    await ctx.invoke(self.bot.get_command('help'))

                elif res["tag"] == "prefix":
                    await message.channel.send(res["response"].replace("~", await get_prefix(ctx)))

                else:
                    await message.channel.send(res["response"])

        elif self.bot.user.mention in message.mentions:
            await ctx.invoke(self.bot.get_command("help"))


def setup(bot):
    bot.add_cog(Chatbot(bot))
