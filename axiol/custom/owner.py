import discord
from discord.ext import commands
import database as db
from functions import update_db
import io
import contextlib
import textwrap

# A private cog which only works for me
class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    def cog_check(self, ctx):
        return ctx.author.id == 791950104680071188
        

    @commands.command(aliases=["eval"])
    async def e(self, ctx, *, code:str=None):

        if code is None:
            return await ctx.send(
                "Define the code too, what is supposed to execute?"
            )
        code = code.lstrip("```python").rstrip("\n```").lstrip("\n")

        local_vars = {
            "discord": discord,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,            
        }
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(

                    f"async def func():\n{textwrap.indent(code, '    ')}", local_vars

                )
                obj = await local_vars["func"]()
                result = f"{stdout.getvalue()}"
        except Exception as e:
            result = e
        if len(str(result)) >= 2000:
            result = result[:1900]
            await ctx.send("Result larger than 2000 characters, returned 1900 characters only.")

        await ctx.send(f"```python\n{result}```")
    
    @commands.command()
    async def get_guilds(self, ctx, *,user:discord.User=None):
        if user is None:
            return await ctx.send("You need to define the user to find in which guilds they are!")
        data = {}
        for guild in self.bot.guilds:
            for member in guild.members:
                if member == user:
                    data.update({guild.name: guild.id})
        await ctx.send(f"**{user}** found in __{len(data)}__ guilds\n```json\n{data}```")


    @commands.command()
    async def get_members(self, ctx, *, guild:discord.Guild=None):
        if guild is None:
            return await ctx.send("You need to define the guild too")

        members = ""
        for member in guild.members:
            members += f"`{member}` - "
            if len(members) > 1500:
                members += "**\nMessage was too long so this is not complete**"
                break
            
        await ctx.send(members)


    @commands.command()
    async def get_doc(self, ctx, doc_name=None, *,guild:discord.Guild=None):
        if doc_name is None or guild is None:
            return await ctx.send("You need to define both document name and guild name/id")

        try:
            plugindb = getattr(db, doc_name.upper())
        except:
            return await ctx.send(f"No document with name **{doc_name.upper()}**")

        doc = plugindb.find_one({"_id":guild.id})
        
        await ctx.send(f"**{doc_name.upper()}** Document for **{guild.name}**\n```json\n{doc}```")


    @commands.command()
    async def update_db(self, ctx):
        await update_db([guild.id for guild in self.bot.guilds])
        

    @commands.command()
    async def clean_db(self, ctx):
        guildids = [guild.id for guild in self.bot.guilds]

        async for i in db.AUTOMOD.find({}):
            if i["_id"] not in guildids:
                await db.AUTOMOD.delete_one(i)
                print("AUTOMOD", i["_id"])
        print("\n")
        async for i in db.CHATBOT.find({}):
            if i["_id"] not in guildids:
                await db.CHATBOT.delete_one(i)
                print("CHATBOT", i["_id"])
        print("\n")
        async for i in db.PERMISSIONS.find({}):
            if i["_id"] not in guildids:
                await db.PERMISSIONS.delete_one(i)
                print("PERMISSIONS", i["_id"])
        print("\n")
        async for i in db.PLUGINS.find({}):
            if i["_id"] not in guildids:
                await db.PLUGINS.delete_one(i)
                print("PLUGINS", i["_id"])
        print("\n")
        async for i in db.PREFIXES.find({}):
            if i["_id"] not in guildids:
                await db.PREFIXES.delete_one(i)
                print("PREFIXES", i["_id"])
        print("\n")
        async for i in db.REACTIONROLES.find({}):
            if i["_id"] not in guildids:
                await db.REACTIONROLES.delete_one(i)
                print("REACTIONROLES", i["_id"])
        print("\n")
        async for i in db.VERIFY.find({}):
            if i["_id"] not in guildids:
                await db.VERIFY.delete_one(i)
                print("VERIFY", i["_id"])
        print("\n")
        async for i in db.WELCOME.find({}):
            if i["_id"] not in guildids:
                await db.WELCOME.delete_one(i)
                print("WELCOME", i["_id"])
                
def setup(bot):
    bot.add_cog(Owner(bot))
