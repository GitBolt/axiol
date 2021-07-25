import discord
from discord.ext import commands
from functions import updatedb
from discord.ext.commands import GuildConverter
import database as db
import difflib

Differentiator = difflib.Differ()
# A private cog which only works for me
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    def cog_check(self, ctx):
        return ctx.author.id == 791950104680071188
        

    @commands.command()
    async def accuracy(self, ctx, *, txt=None):
        if txt is None:
            return await ctx.send("You need to define both main text and user inputted content sepeated by `|`")
        raw_text = txt.split("|")[0].lstrip(' ').rstrip(' ').lower()
        user_content = txt.split("|")[1].lstrip(' ').rstrip(' ').lower()

        text = " ".join(raw_text.split(" ")[:len(user_content.split(" "))])

        comparision = Differentiator.compare(text, user_content)
        mistakes = [x for x in comparision if "-" in x or "+" in x]
        comparision = Differentiator.compare(text, user_content)
        
        accuracy = difflib.SequenceMatcher(None, text, user_content).ratio()

        await ctx.send(f"Main text characters: __{len(text)}__\nInput text characters: __{len(user_content)}__\n```Mistakes: __{len(mistakes)}__\nAccuracy: {accuracy}%```")


    @commands.command()
    async def get_guilds(self, ctx, user:discord.User=None):
        if user is None:
            return await ctx.send("You need to define the user to find in which guilds they are!")
        data = {}
        for guild in self.bot.guilds:
            for member in guild.members:
                if member == user:
                    data.update({guild.name: guild.id})
        if data:
            await ctx.send(f"**{user}** found in __{len(data)}__ guilds\n```json\n{data}```")
        else:
            await ctx.send(f"**{user}** found in __0__ guilds")



    @commands.command()
    async def get_members(self, ctx, *, guild=None):
        if guild is None:
            return await ctx.send("You need to define the guild too")
        
        converter = GuildConverter()
        try:
            guildobj = await converter.convert(ctx, guild)
        except commands.errors.GuildNotFound:
            return await ctx.send(f"**{guild}** Guild not found")

        members = ""
        for i in guildobj.members:
            members += f"`{i}` - "
            if len(members) > 1500:
                members += "**\nMessage was too long so this is not complete**"
                break
            
        await ctx.send(members)


    @commands.command()
    async def get_doc(self, ctx, doc_name, guild):
        if doc_name is None or guild is None:
            return await ctx.send("You need to define both document name and guild name/id")
        converter = GuildConverter()
        try:
            guildobj = await converter.convert(ctx, guild)
        except commands.errors.GuildNotFound:
            return await ctx.send(f"**{guild}** Guild not found")

        try:
            plugindb = getattr(db, doc_name.upper())
        except:
            return await ctx.send(f"No document with name **{doc_name.upper()}**")

        doc = plugindb.find_one({"_id":guildobj.id})
        
        await ctx.send(f"**{doc_name.upper()}** Document for **{guildobj.name}**\n```json\n{doc}```")

    @commands.command()
    async def update_db(self, ctx):
        for guild in self.bot.guilds:
            updatedb(guild.id)
        

def setup(bot):
    bot.add_cog(Owner(bot))
