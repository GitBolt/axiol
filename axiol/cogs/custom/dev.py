import textwrap

import discord
from discord.ext import commands

from axiol import DEVS_ID

import io
import contextlib


class Owner(commands.Cog):
    """A private cog which only works for me."""

    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        if ctx.author.id not in DEVS_ID:
            raise commands.NotOwner
        return True

    @commands.command(aliases=["eval"])
    @commands.is_owner()
    async def e(self, ctx, *, code: str = None):
        if code is None:
            return await ctx.send(
                "Define the code too, what is supposed to execute?"
            )

        code = code.lstrip("```python").rstrip("\n```").lstrip("\n")

        local_vars = {
            "discord": discord,
            "commands": commands,
            "bot": self.client,
            "ctx": ctx,
        }
        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}",
                    local_vars
                )

                obj = await local_vars["func"]()
                result = f"{stdout.getvalue()}"

        except Exception as e:
            result = e

        if len(str(result)) >= 2000:
            result = result[:1900]
            await ctx.send(
                "Result larger than 2000 characters, "
                "returned 1900 characters only."
            )

        await ctx.send(f"```python\n{result}```")


def setup(client):
    client.add_cog(Owner(client))
