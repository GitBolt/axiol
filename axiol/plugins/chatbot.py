import disnake
from aiohttp import request
from disnake.ext import commands
import database as db
import constants as var
from functions import get_prefix
from ext.permissions import has_command_permission


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled"""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Chatbot"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} The Chatbot plugin is"
                        " disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    @commands.command(name="setchatbot", aliases=["enablechatbot"])
    @has_command_permission()
    async def set_chat_bot(self, ctx, channel: disnake.TextChannel = None):
        if await db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            await db.CHATBOT.insert_one(
                {"_id": ctx.guild.id, "channels": [ctx.channel.id]}
            )

        if channel is None:
            channel = ctx.channel

        guild_doc = await db.CHATBOT.find_one({"_id": ctx.guild.id})
        channel_list = guild_doc.get("channels")

        new_list = channel_list.copy()
        new_list.append(channel.id)
        new_data = {"$set": {"channels": new_list}}

        await db.CHATBOT.update_one(guild_doc, new_data)
        await ctx.send(f"{var.E_ACCEPT} Enabled Chatbot for {channel.mention}")

    @commands.command(name="removechatbot", aliases=["disablechatbot"])
    @has_command_permission()
    async def remove_chat_bot(self, ctx, channel: disnake.TextChannel = None):
        if await db.CHATBOT.find_one({"_id": ctx.guild.id}) is None:
            await db.CHATBOT.insert_one({"_id": ctx.guild.id, "channels": []})

        if channel is None:
            channel = ctx.channel

        guild_doc = await db.CHATBOT.find_one({"_id": ctx.guild.id})

        if channel.id in guild_doc.get("channels"):
            channel_list = guild_doc.get("channels")
            new_list = channel_list.copy()
            new_list.remove(channel.id)
            new_data = {"$set": {"channels": new_list}}

            await db.CHATBOT.update_one(guild_doc, new_data)
            await ctx.send(f"Disabled Chatbot from {channel.mention}")

        else:
            await ctx.send("This channel is not a bot chatting channel")

    @commands.command(name="chatbotchannels")
    @has_command_permission()
    async def chat_bot_channels(self, ctx):
        guild_doc = await db.CHATBOT.find_one({"_id": ctx.guild.id})
        embed = disnake.Embed(
            title="All chatbot channels in this server", color=var.C_TEAL
        )

        if guild_doc is not None and guild_doc.get("channels") != []:
            for i in guild_doc.get("channels"):
                embed.add_field(name="** **", value=self.bot.get_channel(i).mention)

            await ctx.send(embed=embed)

        else:
            await ctx.send("This server does not have any chat bot channel")

    @commands.command(name="chatbotreport")
    @has_command_permission()
    async def chat_bot_report(self, ctx, *, desc):
        # Support server suggestions channel
        channel = self.bot.get_channel(843548616505294848)

        await channel.send(
            embed=disnake.Embed(
                title="Chatbot suggestion", description=desc, color=var.C_MAIN
            )
            .add_field(name="By", value=ctx.author)
            .add_field(name="Guild ID", value=ctx.guild.id)
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        guild_plugin_doc = await db.PLUGINS.find_one({"_id": message.guild.id})
        ctx = await self.bot.get_context(message)

        if guild_plugin_doc["Chatbot"] and message.channel.id != 803308171577393172:
            guild_chatbot_doc = await db.CHATBOT.find_one({"_id": message.guild.id})

            def channels():
                if (
                    guild_chatbot_doc is not None
                    and guild_chatbot_doc.get("channels") != []
                ):
                    channels = guild_chatbot_doc.get("channels")

                else:
                    channels = []

                return channels

            if (
                self.bot.user in message.mentions
                and message.author.bot == False
                or message.channel.id in channels()
                and message.author.bot == False
            ):

                content = message.content.replace("<@!843484459113775114>", "")
                async with request(
                    "POST",
                    f"https://axiol.up.railway.app/ai/chatbot",
                    json={"content": content},
                ) as response:
                    res = await response.json()

                if res["response"] == "help":
                    await ctx.invoke(self.bot.get_command("help"))

                elif res["tag"] == "prefix":
                    await message.channel.send(
                        res["response"].replace("~", await get_prefix(ctx))
                    )

                else:
                    await message.channel.send(res["response"])

        elif self.bot.user.mention in message.mentions:
            await ctx.invoke(self.bot.get_command("help"))


def setup(bot):
    bot.add_cog(Chatbot(bot))
