import re
import os
import time
import typing
import difflib
import asyncio
import disnake
import textwrap
from io import BytesIO
from datetime import datetime
from disnake.ext import commands
from PIL import Image, ImageDraw, ImageFont
import database as db
import constants as var
from ext.permissions import has_command_permission
from functions import get_random_text, get_prefix, get_code

TYPE_15 = "<:15:866917795513892883>"
TYPE_30 = "<:30:866917795261579304>"
TYPE_60 = "<:60:866917796507418634>"

CONFIGS = {
    "default": {"time": 60, "size": 75, "width": 35, "height": 120},
    "15": {"time": 15, "size": 75, "width": 35, "height": 120},
    "30": {"time": 30, "size": 60, "width": 45, "height": 95},
    "60": {"time": 60, "size": 55, "width": 50, "height": 82},
}

Differentiator = difflib.Differ()


class TypeRacer:
    def __init__(self, bot, players, required_amount):
        self.bot = bot
        self.players = []
        self.players.append(players)
        self.required_amount = required_amount

        self.created_at = datetime.now()
        self.code = get_code(5)

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def time_elapsed(self):
        time = datetime.now() - self.created_at
        if time.total_seconds() < 60:
            return f"{round(time.total_seconds(), 1)} seconds"

        else:
            return f"{round(time.total_seconds() / 60, 1)} minutes"

    @staticmethod
    async def create_board():
        text = await get_random_text(10)

        image = Image.open(
            os.path.join(os.getcwd(), "resources/backgrounds/typing_board.png")
        )

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            os.path.join(os.getcwd(), "resources/fonts/Poppins-Medium.ttf"), 80
        )

        font2 = ImageFont.truetype(
            os.path.join(os.getcwd(), "resources/fonts/Poppins-Light.ttf"),
            CONFIGS["15"]["size"],
        )

        draw.text((810, 55), "60", (184, 184, 184), font=font)
        offset = 300

        for line in textwrap.wrap(text, width=CONFIGS["15"]["width"]):
            draw.text((72, offset), line, (169, 240, 255), font=font2)
            offset += CONFIGS["15"]["height"]

        return image, text

    @staticmethod
    def calculate_result(start_time, end_time, user_content, raw_text):
        text = " ".join(raw_text.split(" ")[: len(user_content.split(" "))])

        comparaison = Differentiator.compare(text, user_content)
        mistakes = [x for x in comparaison if "-" in x or "+" in x]

        accuracy = (
            round(difflib.SequenceMatcher(None, text, user_content).ratio(), 2) * 100
        )

        time_taken = round((end_time - start_time) - 1, 2)
        raw_wpm = round((len(user_content) / 5 / time_taken) * 60, 2)
        error_rate = round(len(mistakes) / time_taken, 2)
        wpm = round(raw_wpm - error_rate, 2)
        wpm = wpm if wpm >= 0 else 0

        return wpm, accuracy

    async def join_alert(self, user):
        for player in self.players:
            await player.send(
                f"__New player has joined!__\n{user} just joined the queue,"
                f" {len(self.players)} players now."
            )

    async def coro(self, player):
        try:
            m = await self.bot.wait_for(
                "message", check=lambda m: m.author == player, timeout=60
            )

            if m:
                await player.send(
                    f"You test has been completed! "
                    f"Waiting for other players to complete to send results."
                )

                return time.time(), m.content

        except asyncio.TimeoutError:
            await player.send("Time is up! You failed to complete the test in time.")

    async def start(self):
        count = 5

        embed = (
            disnake.Embed(
                title="All players joined!",
                description=f"Match starting in {count}...",
                color=var.C_MAIN,
            )
            .add_field(name="Started", value=f"{self.time_elapsed()} ago", inline=False)
            .add_field(
                name="Players",
                value="\n".join([str(player) for player in self.players]),
                inline=False,
            )
        )

        msgs = {}
        for player in self.players:
            msg = await player.send(embed=embed)
            msgs.update({player: msg})

        for _ in range(4):
            count -= 1
            await asyncio.sleep(1)
            for msg in msgs.values():
                embed.description = f"Match starting in {count}..."
                await msg.edit(embed=embed)

        with BytesIO() as image_binary:
            image, text = await self.create_board()
            image.save(image_binary, "PNG")
            for player in self.players:
                image_binary.seek(0)
                embed.description = f"Match starting now!"
                await msgs[player].edit(embed=embed)

                await player.send(
                    file=disnake.File(fp=image_binary, filename="axiol_typeracer.png")
                )

                await msgs[player].delete()

        start_time = time.time()
        result_embed = disnake.Embed(title="Typing race results", color=var.C_GREEN)

        results = {}
        datas = await asyncio.gather(*[self.coro(player) for player in self.players])

        for player, data in zip(self.players, datas):
            results.update(
                {self.calculate_result(start_time, data[0], data[1], text): player}
            )

        ordered = sorted(results.items(), reverse=True)
        for r in ordered:
            result_embed.add_field(
                name=f"{ordered.index(r) + 1} {r[1]}",
                value=f"{r[0][0]} WPM, {r[0][1]}% Accuracy",
                inline=False,
            )

        for player in self.players:
            await player.send(embed=result_embed)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.matches: typing.List[TypeRacer] = []

    async def cog_check(self, ctx):
        """Simple check to see if this cog (plugin) is enabled."""
        guild_doc = await db.PLUGINS.find_one({"_id": ctx.guild.id})

        if guild_doc.get("Fun"):
            return True

        else:
            await ctx.send(
                embed=disnake.Embed(
                    description=(
                        f"{var.E_DISABLE} " "The Fun plugin is disabled in this server"
                    ),
                    color=var.C_ORANGE,
                )
            )

    def check_playing(self, player: disnake.Member):
        return any(player in match.players for match in self.matches)

    def get_match(self, player: disnake.Member):
        for match in self.matches:
            if player in match.players:
                return match

    @commands.group(name="typeracer", pass_context=True, invoke_without_command=True)
    @has_command_permission()
    async def type_racer(self, ctx):
        if self.check_playing(ctx.author):
            match = self.get_match(ctx.author)

            return await ctx.send(
                content=f"You are already in a queue {ctx.author.mention}",
                embed=disnake.Embed(
                    title=f"Queue info",
                    description=(
                        f"The match currently has `{len(match.players)}` "
                        "players in the queue"
                    ),
                    color=var.C_ORANGE,
                )
                .add_field(name="Code", value=match.code, inline=False)
                .add_field(
                    name="Started", value=match.time_elapsed() + " ago", inline=False
                )
                .add_field(
                    name="Players required", value=match.required_amount, inline=False
                ),
            )

        if not self.matches:
            await ctx.send(
                embed=disnake.Embed(
                    title="No matches found",
                    description=(
                        "There are no on going queues right now,"
                        " maybe create your own?"
                    ),
                    color=var.C_ORANGE,
                ).add_field(
                    name="Start a new match",
                    value=(
                        f"```{await get_prefix(ctx)}typeracer new"
                        f" <number_of_players>```"
                    ),
                )
            )

        else:
            highest_players = max(x.players for x in self.matches)
            match = [
                match for match in self.matches if match.players == highest_players
            ][0]

            match.add_player(ctx.author)

            await ctx.send(
                embed=disnake.Embed(
                    title="You have been added to the queue!",
                    description=f"The queue currently has **{len(match.players)}** players.",
                    color=var.C_BLUE,
                )
                .add_field(name="Code", value=match.code, inline=False)
                .add_field(
                    name="Started", value=match.time_elapsed() + " ago", inline=False
                )
                .add_field(
                    name="Players required", value=match.required_amount, inline=False
                )
            )

            await match.join_alert(ctx.author)
            if len(match.players) >= match.required_amount:
                await match.start()
                self.matches.remove(match)

    @type_racer.command(aliases=["quit", "leave"])
    @has_command_permission()
    async def exit(self, ctx):
        match = self.get_match(ctx.author)
        if match:
            match.remove_player(ctx.author)
            await ctx.send(
                "You removed yourself from the queue of "
                f"the match with code __{match.code}__"
            )

        else:
            await ctx.send("You are not in any match queue right now.")

    @type_racer.command(aliases=["start"])
    @has_command_permission()
    async def new(self, ctx, player_amount=None):
        if player_amount is None:
            return await ctx.send(
                embed=disnake.Embed(
                    title="🚫 Missing argument",
                    description="You need to enter the player amount too!",
                    color=var.C_RED,
                ).add_field(
                    name="format",
                    value=(
                        f"```{await get_prefix(ctx)}typeracer"
                        f" new <player_amount>```"
                    ),
                )
            )

        if self.get_match(ctx.author):
            return await ctx.send("You are already in a match queue!")

        if not player_amount.isnumeric():
            return await ctx.send("The argument which you entered is not numeric.")

        player_amount = int(player_amount)
        match = TypeRacer(self.bot, ctx.author, player_amount)
        self.matches.append(match)
        await ctx.send(
            embed=disnake.Embed(
                title="You have started a new match!",
                description=(
                    f"Invite your friends by sharing the code\n"
                    f"The command would be ```{await get_prefix(ctx)}typeracer "
                    f"join {match.code}```"
                ),
                color=var.C_GREEN,
            )
            .add_field(name="Code", value=match.code, inline=False)
            .add_field(
                name="Players required", value=match.required_amount, inline=False
            )
            .set_footer(text="Waiting for players to join...")
            .set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        )

        if player_amount == 1:
            await match.start()

    @type_racer.command()
    @has_command_permission()
    async def join(self, ctx, code=None):
        if code is None:
            return await ctx.send(
                embed=disnake.Embed(
                    title="🚫 Missing argument",
                    description="You need to enter the code too!",
                    color=var.C_RED,
                ).add_field(
                    name="format",
                    value=(f"```{await get_prefix(ctx)}typeracer" f" join <code>```"),
                )
            )

        if self.get_match(ctx.author):
            return await ctx.send("You are already in a match queue!")

        if code in [x.code for x in self.matches]:
            match = [match for match in self.matches if match.code == code][0]
            match.add_player(ctx.author)

            await ctx.send(
                embed=disnake.Embed(
                    title="You have been added to the queue!",
                    description=(
                        "The queue currently has " f"**{len(match.players)}** players."
                    ),
                    color=var.C_BLUE,
                )
                .add_field(
                    name="Code",
                    value=match.code,
                )
                .add_field(
                    name="Started", value=match.time_elapsed() + " ago", inline=False
                )
                .add_field(name="Players required", value=match.required_amount)
            )

            await match.join_alert(ctx.author)

            if len(match.players) >= match.required_amount:
                await match.start()
                self.matches.remove(match)

        else:
            await ctx.send("Invalid code.")

    @type_racer.command()
    @commands.is_owner()
    async def matches(self, ctx):
        embed = disnake.Embed(
            title="All active matches",
            description=f"There are currently {len(self.matches)} queues",
            color=var.C_MAIN,
        )

        for match in self.matches:
            embed.add_field(
                name=match.code,
                value=f"{len(match.players)}/{match.required_amount}",
                inline=False,
            )

        await ctx.send(embed=embed)

    @commands.command(name="typingtest")
    @has_command_permission()
    async def typing_test(self, ctx, duration="default"):

        if not duration in ["default", "15", "30", "60"]:
            return await ctx.send(
                embed=disnake.Embed(
                    title="🚫 Invalid arguments",
                    description="Duration can only be one of these three: `15`, `30`, `60`.",
                    color=var.C_RED,
                )
            )

        config = CONFIGS[duration]

        def confirm_check(r, u):
            if str(r.emoji) == var.E_ACCEPT:
                return u == ctx.author and r.message == bot_msg

        bot_msg = await ctx.send(
            f"You have selected **{config['time']}** {'(Default)' if duration == 'default' else '(Custom)'}"
            f" seconds for typing test, react to {var.E_ACCEPT} to start!"
        )

        await bot_msg.add_reaction(var.E_ACCEPT)

        await self.bot.wait_for("reaction_add", check=confirm_check)

        text = await get_random_text(10 if duration == "default" else config["time"])

        image = Image.open(
            os.path.join(os.getcwd(), "resources/backgrounds/typing_board.png")
        )
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            os.path.join(os.getcwd(), "resources/fonts/Poppins-Medium.ttf"), 80
        )

        font2 = ImageFont.truetype(
            os.path.join(os.getcwd(), "resources/fonts/Poppins-Light.ttf"),
            config["size"],
        )
        draw.text((810, 55), str(config["time"]), (184, 184, 184), font=font)
        offset = 300

        for line in textwrap.wrap(text, width=config["width"]):
            draw.text((72, offset), line, (169, 240, 255), font=font2)
            offset += config["height"]

        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)

            await ctx.send(file=disnake.File(fp=image_binary, filename="image.png"))

            try:
                initial_time = time.time()

                def message_check(message):
                    return (
                        message.author == ctx.author
                        and message.channel.id == ctx.channel.id
                    )

                waiter = self.bot.loop.create_task(
                    self.bot.wait_for(
                        "message", check=message_check, timeout=config["time"]
                    )
                )

                timer = config["time"]
                bot_msg = None

                while not waiter.done():
                    await asyncio.sleep(1)
                    timer -= 1
                    if config["time"] == 60 and timer == 30:
                        bot_msg = await ctx.send(
                            "Half of the time is gone! 30 seconds left"
                        )

                    if config["time"] == 30 and timer == 15:
                        bot_msg = await ctx.send(
                            "Half of the time is gone! Only 15 seconds left"
                        )

                    if timer == 10:

                        if config["time"] != 15:
                            await bot_msg.edit(content="Only 10 seconds left!")
                        else:
                            bot_msg = await ctx.send("Only 10 seconds left!")

                    if timer == 5:
                        await bot_msg.edit(
                            content=f"Only 5 seconds left {ctx.author.mention}!"
                        )

                else:
                    user_content = waiter.result().content

                    text = " ".join(text.split(" ")[: len(user_content.split(" "))])

                    comparaison = list(Differentiator.compare(text, user_content))
                    mistakes = [x for x in comparaison if "-" in x or "+" in x]

                    time_taken = round((time.time() - initial_time) - 1, 2)
                    raw_wpm = round((len(user_content) / 5 / time_taken) * 60, 2)

                    mistake_ratio = f"{len(mistakes)}/{len(user_content)}"

                    accuracy = round(
                        difflib.SequenceMatcher(None, text, user_content).ratio() * 100,
                        2,
                    )

                    error_rate = round(len(mistakes) / time_taken, 2)
                    wpm = round(raw_wpm - error_rate, 2)
                    wpm = wpm if wpm >= 0 else 0

                    description = (
                        "Your typing speed is above average 📈"
                        if wpm >= 60
                        else "Your typing speed is below average 📉"
                    )

                    embed = disnake.Embed(
                        title=f"{wpm} words per minute",
                        description=f"{description} {ctx.author.mention}",
                    )

                    embed.add_field(name="Raw WPM", value=f"{raw_wpm}", inline=False)

                    embed.add_field(
                        name="Time taken", value=f"{time_taken} Seconds", inline=False
                    )

                    embed.add_field(name="Accuracy", value=f"{accuracy}%", inline=False)

                    embed.add_field(name="Mistakes", value=mistake_ratio, inline=False)

                    embed.add_field(
                        name="Error rate", value=f"{error_rate}%", inline=False
                    )

                    embed.color = var.C_GREEN
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

                    embed.set_footer(
                        text=(
                            "Final typing speed is adjusted "
                            "depending on the accuracy"
                        )
                    )

                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(
                    embed=disnake.Embed(
                        description=(
                            "Time is up! You failed to complete "
                            f"the test in time {ctx.author.mention}"
                        ),
                        color=var.C_RED,
                    )
                )

    @commands.command()
    @has_command_permission()
    async def avatar(self, ctx, user: disnake.User = None):
        avatar_user = ctx.author if user is None else user
        avatar = avatar_user.avatar.url

        embed = disnake.Embed(
            title=f"Avatar of **{avatar_user}**", color=var.C_TEAL
        ).set_image(url=avatar)

        await ctx.send(embed=embed)

    @commands.command()
    @has_command_permission()
    async def embed(self, ctx, channel: disnake.TextChannel = None):
        if channel is None:
            return await ctx.send(
                embed=disnake.Embed(
                    description="🚫 You need to define the channel too!",
                    color=var.C_ORANGE,
                )
                .add_field(
                    name="Format",
                    value=f"```{await get_prefix(ctx)}embed <#channel>```",
                    inline=False,
                )
                .add_field(
                    name="Don't worry, this won't send the embed right away!",
                    value="** **",
                )
            )

        embed = disnake.Embed(
            title="Create an embed",
            description=(
                f"React to the colour circle emojis below to quickly "
                f"choose an embed colour! To add a custom hex color react"
                f" to 🖌️\nWhen you are done selecting embed colour press "
                f"the {var.E_CONTINUE} emoji to continue editing"
            ),
            color=var.C_MAIN,
        ).set_footer(
            text=(
                "This message will become the live preview of "
                "the embed you are creating!"
            )
        )

        preview = await ctx.send(embed=embed)
        emojis = [
            var.E_RED,
            var.E_PINK,
            var.E_GREEN,
            var.E_BLUE,
            var.E_ORANGE,
            var.E_YELLOW,
        ]

        colors = [0xFF0000, 0xFF58BC, 0x24FF00, 0x00E0FF, 0xFF5C00, 0xFFC700]

        await preview.add_reaction("🖌️")

        for i in emojis:
            await preview.add_reaction(i)

        await preview.add_reaction(var.E_CONTINUE)

        def preview_reaction_check(r, u):
            return u == ctx.author and r.message == preview

        def msg_check(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        while True:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=preview_reaction_check
            )

            if str(reaction.emoji) == "🖌️":
                await ctx.send(
                    "Send a hex colour code to make it the embed colour! "
                    "You can use either 3 or 6 hex characters"
                )

                user_msg = await self.bot.wait_for("message", check=msg_check)

                match = re.search(
                    r"^#(?:[0-9a-fA-F]{3}){1,2}$", user_msg.content.lower()
                )

                if match:
                    hexed = int(hex(int(user_msg.content.replace("#", ""), 16)), 0)

                    embed.color = hexed
                    await preview.edit(embed=embed)

                else:
                    try:
                        await preview.remove_reaction("🖌️", ctx.author)

                    except disnake.Forbidden:
                        pass

                    await ctx.send("Invalid hex code, try again")

            elif str(reaction.emoji) == var.E_CONTINUE:
                break

            else:
                index = emojis.index(str(reaction))
                embed.color = colors[index]
                try:
                    await preview.remove_reaction(emojis[index], ctx.author)

                except disnake.Forbidden:
                    pass

                await preview.edit(embed=embed)

        try:
            await preview.clear_reactions()

        except disnake.Forbidden:
            pass

        PREVIEW_URL = f"(https://disnake.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})"
        title_bot_msg = await ctx.send(
            embed=disnake.Embed(
                title="Title",
                description=(
                    f"Now send a message to make it the title of the "
                    f"[embed]{PREVIEW_URL}"
                ),
                color=var.C_BLUE,
            ).set_footer(text="Type cancel to stop this proccess")
        )

        user_msg = await self.bot.wait_for("message", check=msg_check)
        if user_msg.content in ["cancel", "`cancel`", "```cancel```"]:
            await ctx.send("Stopped embed creation proccess.")
            return

        embed.title = user_msg.content
        await preview.edit(embed=embed)
        await title_bot_msg.delete()
        try:
            await user_msg.delete()
        except disnake.Forbidden:
            pass

        desc_bot_msg = await ctx.send(
            embed=disnake.Embed(
                title="Description",
                description=(
                    f"Now send a message to make it the description of the"
                    f" [embed]{PREVIEW_URL}"
                ),
                color=var.C_BLUE,
            )
            .add_field(name="** **", value="Type `skip` if you don't want to set this")
            .set_footer(text="Type cancel to stop this proccess")
        )

        user_msg = await self.bot.wait_for("message", check=msg_check)
        if user_msg.content in ["cancel", "`cancel`", "```cancel```"]:
            await ctx.send("Stopped embed creation proccess.")
            return

        if user_msg.content in ["skip", "`skip`", "```skip```"]:
            embed.description = None
            await preview.edit(embed=embed)
            await desc_bot_msg.delete()
            try:
                await user_msg.delete()
            except disnake.Forbidden:
                pass

        else:
            embed.description = user_msg.content
            await preview.edit(embed=embed)
            await desc_bot_msg.delete()
            try:
                await user_msg.delete()
            except disnake.Forbidden:
                pass

        thumbnail_bot_msg = await ctx.send(
            embed=disnake.Embed(
                title="Thumbnail",
                description=(
                    f"Now send a message to make it the thumbnail of the "
                    f"[embed](https://disnake.com/channels/{ctx.guild.id}"
                    f"/{preview.channel.id}/{preview.id})"
                ),
                color=var.C_BLUE,
            )
            .add_field(name="** **", value="Type `skip` if you don't want to set this")
            .set_footer(text="Type cancel to stop this proccess")
        )

        while True:
            user_msg = await self.bot.wait_for("message", check=msg_check)

            if user_msg.content in ["cancel", "`cancel`", "```cancel```"]:
                await ctx.send("Stopped embed creation proccess.")
                return

            if user_msg.content in ["skip", "`skip`", "```skip```"]:
                await thumbnail_bot_msg.delete()
                break

            elif user_msg.attachments:
                embed.set_thumbnail(url=user_msg.attachments[0].url)
                await preview.edit(embed=embed)
                await thumbnail_bot_msg.delete()
                try:
                    await user_msg.delete()
                except disnake.Forbidden:
                    pass
                break

            elif user_msg.content.startswith("https"):
                embed.set_thumbnail(url=user_msg.content)
                await thumbnail_bot_msg.delete()
                try:
                    await user_msg.delete()
                except:
                    pass
                break

            else:
                await ctx.send(
                    "Uh oh it looks like the message "
                    "you sent is not any link or image, "
                    "try again."
                )

        embed.set_footer(text="")
        await preview.edit(embed=embed)
        await preview.add_reaction(var.E_ACCEPT)

        edit = await ctx.send(
            embed=disnake.Embed(
                description=(
                    f"React to the {var.E_ACCEPT} emoji in the original"
                    f" [preview]{PREVIEW_URL}"
                    f"to send your embed! To edit more react to the"
                    f" respective emojis below"
                ),
                color=var.C_BLUE,
            )
            .add_field(name="Add field", value="React to 🇦", inline=False)
            .add_field(name="Footer", value="React to 🇫", inline=False)
            .add_field(name="Image", value="React to 🇮", inline=False)
            .add_field(name="Set Author", value="React to 🇺", inline=False)
        )

        def edit_reaction_check(r, u):
            return u == ctx.author and r.message == edit or r.message == preview

        edit_emojis = ["🇦", "🇫", "🇮", "🇺"]

        for i in edit_emojis:
            await edit.add_reaction(i)

        while True:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", check=edit_reaction_check
            )

            if str(reaction.emoji) == var.E_ACCEPT:
                await channel.send(embed=embed)
                await ctx.send("Embed sent in " + channel.mention + " !")
                return

            if str(reaction.emoji) == "🇦":
                field_bot_msg = await ctx.send(
                    "Send a message and seperate your **Field name "
                    "and value** with `|`\nFor example: This is my field "
                    "name | This is the field value!"
                )

                user_msg = await self.bot.wait_for("message", check=msg_check)

                field_list = user_msg.content.split("|")
                if len(field_list) != 2:
                    await ctx.send(
                        "Invalid format, make sure to add `|` between "
                        "your field name and value"
                    )

                else:
                    embed.add_field(
                        name=field_list[0], value=field_list[1], inline=False
                    )

                    await preview.edit(embed=embed)
                    await field_bot_msg.delete()
                    await user_msg.delete()

                try:
                    await edit.remove_reaction("🇦", ctx.author)

                except disnake.Forbidden:
                    pass

            if str(reaction.emoji) == "🇫":
                footer_bot_msg = await ctx.send(
                    "Send a message to make it the **Footer**!"
                )

                user_msg = await self.bot.wait_for("message", check=msg_check)

                embed.set_footer(text=user_msg.content)
                await preview.edit(embed=embed)
                await footer_bot_msg.delete()
                await user_msg.delete()

                try:
                    await edit.clear_reaction("🇫")

                except disnake.Forbidden:
                    pass

            if str(reaction.emoji) == "🇮":
                while True:
                    image_bot_msg = await ctx.send(
                        "Now send an image or link to add that **Image** "
                        "to the embed!\nType `skip` if you don't want to "
                        "set this"
                    )

                    user_msg = await self.bot.wait_for("message", check=msg_check)

                    if user_msg.content in ["skip", "`skip`", "```skip```"]:
                        await ctx.send("Skipped image, react to 🇮 again to set it.")

                        await edit.remove_reaction("🇮", ctx.author)
                        break

                    elif user_msg.attachments:
                        embed.set_image(url=user_msg.attachments[0].url)
                        await preview.edit(embed=embed)
                        await thumbnail_bot_msg.delete()
                        await user_msg.delete()
                        break

                    elif user_msg.content.startswith("https"):
                        embed.set_image(url=user_msg.content)
                        await preview.edit(embed=embed)
                        await image_bot_msg.delete()
                        await user_msg.delete()
                        break
                    else:
                        await ctx.send(
                            "Look the message you sent is not a file or link, try again."
                        )
                    try:
                        await edit.clear_reaction("🇮")

                    except disnake.Forbidden:
                        pass

            if str(reaction.emoji) == "🇺":
                while True:

                    if user_msg.content in ["skip", "`skip`", "```skip```"]:
                        break

                    else:
                        author_bot_msg = await ctx.send(
                            "Now send userID or member mention to set them"
                            " as the **author** of the embed\n Type `skip`"
                            " if you don't want to set this"
                        )

                        user_msg = await self.bot.wait_for("message", check=msg_check)

                        userid = user_msg.content.strip("!@<>")
                        try:
                            author_user = await self.bot.fetch_user(int(userid))

                            embed.set_author(
                                name=author_user, icon_url=author_user.avatar.url
                            )

                            await author_bot_msg.delete()
                            await user_msg.delete

                            try:
                                await edit.clear_reaction("🇺")

                            except disnake.Forbidden:
                                pass

                            await preview.edit(embed=embed)
                            break

                        except Exception:
                            await ctx.send(
                                embed=disnake.Embed(
                                    title="Invalid user",
                                    description=("Send the userID or mention again"),
                                    color=var.C_RED,
                                ).set_footer(
                                    text=(
                                        "Make sure your message contains"
                                        " only the user, nothing else"
                                    )
                                )
                            )


def setup(bot):
    bot.add_cog(Fun(bot))
