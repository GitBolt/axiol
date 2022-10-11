import disnake
from aiohttp import request
from disnake.ext import commands
import database as db
from functions import update_db
import io
import json
import contextlib
import textwrap


class Owner(commands.Cog):
    """A private cog which only works for me."""

    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return ctx.author.id == 791950104680071188

    @commands.command(aliases=["eval"])
    async def e(self, ctx, *, code: str = None):
        if code is None:
            return await ctx.send("Define the code too, what is supposed to execute?")

        code = code.lstrip("```python").rstrip("\n```").lstrip("\n")

        local_vars = {
            "disnake": disnake,
            "commands": commands,
            "bot": self.bot,
            "ctx": ctx,
        }
        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(f"async def func():\n{textwrap.indent(code, '    ')}", local_vars)

                obj = await local_vars["func"]()
                result = f"{stdout.getvalue()}"

        except Exception as e:
            result = e

        if len(str(result)) >= 2000:
            result = result[:1900]
            await ctx.send(
                "Result larger than 2000 characters, " "returned 1900 characters only."
            )

        await ctx.send(f"```python\n{result}```")

    @commands.command()
    async def get_guilds(self, ctx, *, user: disnake.User = None):
        if user is None:
            return await ctx.send(
                "You need to define the user to find in which guilds they are!"
            )

        data = {}
        for guild in self.bot.guilds:
            for member in guild.members:
                if member == user:
                    data.update({guild.name: guild.id})
        await ctx.send(
            f"**{user}** found in __{len(data)}__ guilds\n```json\n{data}```"
        )

    @commands.command()
    async def get_members(self, ctx, *, guild: disnake.Guild = None):
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
    async def get_doc(self, ctx, doc_name=None, *, guild: disnake.Guild = None):
        if doc_name is None or guild is None:
            return await ctx.send(
                "You need to define both document name and guild name/id"
            )

        try:
            plugin_db = getattr(db, doc_name.upper())

        except Exception:
            return await ctx.send(f"No document with name **{doc_name.upper()}**")

        doc = await plugin_db.find_one({"_id": guild.id})

        await ctx.send(
            f"**{doc_name.upper()}** Document for **{guild.name}**\n"
            f"```json\n{doc}```"
        )

    @commands.command()
    async def backup_db(self, ctx):
        headers = {
            "X-Master-Key": "$2b$10$sHW.6D.jlcsj.XuCzJcytOdqPpcZQKNhVZaOgJhEGia1P5ZlCGEUq",
            "Content-Type": "application/json",
        }
        count = 0
        # Just plugin document for now
        async for i in db.PLUGINS.find({}):
            async with request(
                "POST",
                "https://api.jsonbin.io/v3/b",
                data=json.dumps(i),
                headers=headers,
            ):
                count += 1

        await ctx.send(f"Backed up {count} plugin documents.")

    @commands.command()
    async def update_db(self, ctx):
        await update_db([guild.id for guild in self.bot.guilds])

    @commands.command()
    async def clean_db(self, ctx):
        guild_ids = [guild.id for guild in self.bot.guilds]

        async for i in db.AUTO_MOD.find({}):
            if i["_id"] not in guild_ids:
                await db.AUTO_MOD.delete_one(i)
                print("AUTO_MOD", i["_id"])

        print("\n")
        async for i in db.CHATBOT.find({}):
            if i["_id"] not in guild_ids:
                await db.CHATBOT.delete_one(i)
                print("CHATBOT", i["_id"])

        print("\n")
        async for i in db.PERMISSIONS.find({}):
            if i["_id"] not in guild_ids:
                await db.PERMISSIONS.delete_one(i)
                print("PERMISSIONS", i["_id"])

        print("\n")
        async for i in db.PLUGINS.find({}):
            if i["_id"] not in guild_ids:
                await db.PLUGINS.delete_one(i)
                print("PLUGINS", i["_id"])

        print("\n")
        async for i in db.PREFIXES.find({}):
            if i["_id"] not in guild_ids:
                await db.PREFIXES.delete_one(i)
                print("PREFIXES", i["_id"])

        print("\n")
        async for i in db.REACTION_ROLES.find({}):
            if i["_id"] not in guild_ids:
                await db.REACTION_ROLES.delete_one(i)
                print("REACTION_ROLES", i["_id"])

        print("\n")
        async for i in db.VERIFY.find({}):
            if i["_id"] not in guild_ids:
                await db.VERIFY.delete_one(i)
                print("VERIFY", i["_id"])

        print("\n")
        async for i in db.WELCOME.find({}):
            if i["_id"] not in guild_ids:
                await db.WELCOME.delete_one(i)
                print("WELCOME", i["_id"])


def setup(bot):
    bot.add_cog(Owner(bot))
