import re
import os
import time
import typing
import difflib
import asyncio
import discord
import textwrap
from io import BytesIO
from datetime import datetime
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import database as db
import variables as var
from ext.permissions import has_command_permission
from functions import random_text, getprefix, code_generator


TYPE_15 = "<:15:866917795513892883>" 
TYPE_30 = "<:30:866917795261579304>"
TYPE_60 = "<:60:866917796507418634>"

CONFIG_15 = {"time":15, "size": 75, "width": 35, "height": 120}
CONFIG_30 = {"time":30, "size": 60, "width": 45, "height": 95}
CONFIG_60 = {"time":60, "size": 54, "width": 52, "height": 82}

Differentiator = difflib.Differ()

class TypeRacer:
    def __init__(self, bot, players, required_amount):
        self.bot = bot
        self.players = []
        self.players.append(players)
        self.required_amount = required_amount

        self.created_at = datetime.now()
        self.code = code_generator()

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def time_elapsed(self):
        time =  datetime.now() - self.created_at
        if time.total_seconds() < 60:
            return f"{round(time.total_seconds(), 1)} seconds"
        else:
            return f"{round(time.total_seconds()/60, 1)} minutes"

    @staticmethod
    def create_board():
        get_text = random_text(10)
        text = get_text if get_text.endswith(".") else get_text+"."
        image = Image.open(os.path.join(os.getcwd(),("resources/backgrounds/typing_board.png")))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(os.getcwd(),("resources/fonts/Poppins-Medium.ttf")), 80)
        font2 = ImageFont.truetype(os.path.join(os.getcwd(),("resources/fonts/Poppins-Light.ttf")), CONFIG_15["size"])
        draw.text((810, 55), "60" ,(184,184,184),font=font)
        offset = 300
        for line in textwrap.wrap(text, width=CONFIG_15["width"]):
            draw.text((72, offset), line ,(169,240,255),font=font2)
            offset += CONFIG_15["height"]
        return image, text

    @staticmethod
    def calculate_result(start_time, end_time, user_content, raw_text):
        text = " ".join(raw_text.split(" ")[:len(user_content.split(" "))])
        comparision = Differentiator.compare(text, user_content)
        mistakes = [x for x in comparision if "-" in x or "+" in x]
        accuracy = round(difflib.SequenceMatcher(None, text, user_content).ratio(), 2)*100
        time_taken =  round((end_time - start_time)-1, 2)
        raw_wpm = round((len(user_content)/5/time_taken)*60, 2)
        error_rate = round(len(mistakes) / time_taken, 2)
        wpm = round(raw_wpm - error_rate, 2)
        wpm = wpm if wpm >= 0 else 0
        return wpm, accuracy

    async def join_alert(self, user):
        for player in self.players:
            await player.send(f"__New player has joined!__\n{user} just joined the queue, {len(self.players)} players now.")

    async def coro(self, player):
        try:
            m = await self.bot.wait_for("message", check=lambda m:m.author == player, timeout=60)
            if m:
                await player.send(f"You test has been completed! Waiting for other players to complete to send results.")
                return time.time(), m.content
        except asyncio.TimeoutError:
            await player.send("Time is up! You failed to complete the test in time.")

    async def start(self):
        count = 3
        embed = discord.Embed(
        title="All players joined!", 
        description=f"Match starting in {count}...", 
        color=var.C_MAIN, 
        ).add_field(name="Started", value=f"{self.time_elapsed()} ago", inline=False
        ).add_field(name="Players", value="\n".join([str(player) for player in self.players]), inline=False
        )
        msgs = {}
        for player in self.players:
            msg = await player.send(embed=embed)
            msgs.update({player:msg})

        for _ in range(2):
            count -= 1
            await asyncio.sleep(1)
            for msg in msgs.values():
                embed.description = f"Match starting in {count}..."
                await msg.edit(embed=embed)

        with BytesIO() as image_binary:
            image, text = self.create_board()
            image.save(image_binary, 'PNG')
            for player in self.players:
                image_binary.seek(0)
                embed.description = f"Match starting now!"
                await msgs[player].edit(embed=embed)
                await player.send(file=discord.File(fp=image_binary, filename='axiol_typeracer.png'))
                await msgs[player].delete()
        
        start_time = time.time()
        result_embed = discord.Embed(title="Typing race results", color=var.C_GREEN)
        results = {}
        datas = await asyncio.gather(*[self.coro(player)for  player in self.players])
        for player, data in zip(self.players, datas):
            results.update({self.calculate_result(start_time, data[0], data[1], text): player})
        ordered = sorted(results.items(), reverse=True)
        for r in ordered:
            result_embed.add_field(name=f"{ordered.index(r)+1} {r[1]}", value=f"{r[0]} WPM", inline=False)

        for player in self.players:
            await player.send(embed=result_embed)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.matches: typing.List[TypeRacer] = []
    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Fun") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Fun plugin is disabled in this server",
                color=var.C_ORANGE
            ))
    
    def check_playing(self, player:discord.Member):
        return any(player in match.players for match in self.matches)
    
    def get_match(self, player:discord.Member):
        for match in self.matches:
            if player in match.players:
                return match

    
    @commands.group(pass_context=True, invoke_without_command=True)
    @has_command_permission()
    async def typeracer(self, ctx):

        if self.check_playing(ctx.author):
            match = self.get_match(ctx.author)
            return await ctx.send(content=f"You are already in a queue {ctx.author.mention}", embed=discord.Embed(
                title=f"Queue info",
                description=f"The match currently has `{len(match.players)}` players in the queue",
                color=var.C_ORANGE
                ).add_field(name="Code", value=match.code, inline=False
                ).add_field(name="Started", value=match.time_elapsed() + " ago", inline=False
                ).add_field(name="Players required", value=match.required_amount, inline=False
                ))

        if not self.matches:
            await ctx.send(embed=discord.Embed(
                title="No matches found",
                description="There are no on going queues right now, maybe create your own?",
                color=var.C_ORANGE
            ).add_field(name="Start a new match", value=f"```{getprefix(ctx)}typeracer new <number_of_players>```")
            )
        else:
            highest_players = max([x.players for x in self.matches])
            match = [match for match in self.matches if match.players == highest_players][0]
            match.add_player(ctx.author)
            await ctx.send(embed=discord.Embed(
                title="You have been added to the queue!",
                description=f"The queue currently has **{len(match.players)}** players.",
                color=var.C_BLUE
            ).add_field(name="Code", value=match.code, inline=False
            ).add_field(name="Started", value=match.time_elapsed() + " ago", inline=False
            ).add_field(name="Players required", value=match.required_amount, inline=False
            )
            )
            await match.join_alert(ctx.author)
            if  len(match.players) >= match.required_amount:
                await match.start()
                self.matches.remove(match)


    @typeracer.command(aliases=["quit", "leave"])
    @has_command_permission()
    async def exit(self, ctx):
        match = self.get_match(ctx.author)
        if match:
            match.remove_player(ctx.author)
            await ctx.send(f"You removed yourself from the queue of the match with code __{match.code}__")
        else:
            await ctx.send("You are not in any match queue right now.")


    @typeracer.command(aliases=["start"])
    @has_command_permission()
    async def new(self, ctx, player_amount=None):
        if player_amount is None:
            return await ctx.send(embed=discord.Embed(
                title="🚫 Missing argument",
                description="You need to enter the player amount too!",
                color=var.C_RED
            ).add_field(name="format", value=f"```{getprefix(ctx)}typeracer new <player_amount>```"
            ))
        if self.get_match(ctx.author):
            return await ctx.send("You are already in a match queue!")
        if not player_amount.isnumeric():
            return await ctx.send("The argument which you entered is not numeric.")

        player_amount = int(player_amount)
        match = TypeRacer(self.bot, ctx.author, player_amount)
        self.matches.append(match)
        await ctx.send(embed=discord.Embed(
            title="You have started a new match!",
            description=f"Invite your friends by sharing the code\nThe command would be ```{getprefix(ctx)}typeracer join {match.code}```",
            color=var.C_GREEN
        ).add_field(name="Code", value=match.code, inline=False
        ).add_field(name="Players required", value=match.required_amount, inline=False
        ).set_footer(text="Waiting for players to join..."
        ).set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        )
        if player_amount == 1:
            await match.start()

    @typeracer.command()
    @has_command_permission()
    async def join(self, ctx, code=None):
        if code is None:
            return await ctx.send(embed=discord.Embed(
                title="🚫 Missing argument",
                description="You need to enter the code too!",
                color=var.C_RED
            ).add_field(name="format", value=f"```{getprefix(ctx)}typeracer join <code>```"
            ))
        if self.get_match(ctx.author):
            return await ctx.send("You are already in a match queue!")

        if code in [x.code for x in self.matches]:
            match = [match for match in self.matches if match.code == code][0]
            match.add_player(ctx.author)
            await ctx.send(embed=discord.Embed(
                title="You have been added to the queue!",
                description=f"The queue currently has **{len(match.players)}** players.",
                color=var.C_BLUE
            ).add_field(name="Code", value=match.code,
            ).add_field(name="Started", value=match.time_elapsed() + " ago", inline=False
            ).add_field(name="Players required", value=match.required_amount
            )
            )
            await match.join_alert(ctx.author)
            if len(match.players) >= match.required_amount:
                await match.start()
                self.matches.remove(match)
        else:
            await ctx.send("Invalid code.")

    @typeracer.command()
    @commands.is_owner()
    async def matches(self, ctx):
        embed = discord.Embed(title="All active matches", description=f"There are currently {len(self.matches)} queues", color=var.C_MAIN)
        for match in self.matches:
            embed.add_field(name=match.code, value=f"{len(match.players)}/{match.required_amount}", inline=False)

        await ctx.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def typingtest(self, ctx, test_type=None):
        if test_type is None:
            return await ctx.send(embed=discord.Embed(
            title="🚫 Missing arguments",
            description="You need to define the typing test type too!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}typingtest <type>`\nThere are two types available: `time` and `word`"
            ))

        elif test_type not in ["time", "word"]:
            return await ctx.send(embed=discord.Embed(
                title="🚫 Invalid type",
                description="The type can be either `time` or `word`",
                color=var.C_RED
            ).add_field(name="time", value="Time based typing test, here you have to type as much as you can from the text given under the time you choose."
            ).add_field(name="word", value="Word base typing test, here you need to complete the entire text given and the max time is 60 seconds.")
            )

        if test_type == "time":
            botmsg = await ctx.send(embed=discord.Embed(
                title=f"{test_type.capitalize()} based typing test",
                description=f"Let's see how fast you can type! React to the respective emoji below to start.\n\n{TYPE_15} 15 Seconds Test\n{TYPE_30} 30 Seconds Test\n{TYPE_60} 60 Seconds Test\n{var.E_DECLINE} Cancel Test",
                color=var.C_BLUE
                ).add_field(name="Note", value="The task is to type as much as you can in the time specified, not to complete all the text given. I will inform you when less time is left!")
                )
            await botmsg.add_reaction(TYPE_15)
            await botmsg.add_reaction(TYPE_30)
            await botmsg.add_reaction(TYPE_60)
            await botmsg.add_reaction(var.E_DECLINE)

            def reactioncheck(reaction, user):
                return user == ctx.author and reaction.message == botmsg

            def confirmcheck(reaction, user):
                if str(reaction.emoji) == var.E_ACCEPT:
                    return user == ctx.author and reaction.message == botmsg

            reaction, user = await  self.bot.wait_for("reaction_add", check=reactioncheck)
            
            if str(reaction.emoji) == var.E_DECLINE:
                return await ctx.send(f"Cancelled typing test.")
                
            if str(reaction.emoji) == TYPE_15:
                config = CONFIG_15

            if str(reaction.emoji) == TYPE_30:
                config = CONFIG_30

            if str(reaction.emoji) == TYPE_60:
                config = CONFIG_60

            botmsg = await ctx.send(f"You have selected **{config['time']}** seconds for typing test, react to {var.E_ACCEPT} to start!")
            await botmsg.add_reaction(var.E_ACCEPT)
            await self.bot.wait_for("reaction_add", check=confirmcheck)
        else:
            config = CONFIG_15
            config["time"] = 60

        text = random_text(config["time"] if test_type == "time" else 10)

        image = Image.open(os.path.join(os.getcwd(),("resources/backgrounds/typing_board.png")))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(os.path.join(os.getcwd(),("resources/fonts/Poppins-Medium.ttf")), 80)
        font2 = ImageFont.truetype(os.path.join(os.getcwd(),("resources/fonts/Poppins-Light.ttf")), config["size"])
        draw.text((810, 55), str(config["time"]) ,(184,184,184),font=font)
        offset = 300
        for line in textwrap.wrap(text, width=config["width"]):
            draw.text((72, offset), line ,(169,240,255),font=font2)
            offset += config["height"]

        with BytesIO() as image_binary:
            image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            try:
                initial_time = time.time()
                def messagecheck(message):
                    return message.author == ctx.author and message.channel.id == ctx.channel.id
                waiter = self.bot.loop.create_task(self.bot.wait_for("message", check=messagecheck, timeout=config["time"]))
                timer = config["time"]

                while not waiter.done():
                    await asyncio.sleep(1)
                    timer -= 1
                    if config["time"] == 60 and timer == 30:
                        await ctx.send("Half of the time is gone! 30 seconds left")
                    if config["time"] == 30 and timer == 15:
                        await ctx.send("Half of the time is gone! Only 15 seconds left")
                    if timer == 10:
                        await ctx.send("Only 10 secs left!")
                    if timer == 5:
                        await ctx.send(f"Only 5 seconds left {ctx.author.mention}!")
                else:
                    user_content = waiter.result().content

                    text = " ".join(text.split(" ")[:len(user_content.split(" "))])
                    comparision = Differentiator.compare(text, user_content)
                    mistakes = [x for x in comparision if "-" in x or "+" in x]
                    comparision = Differentiator.compare(text, user_content)

                    time_taken =  round((time.time() - initial_time)-1, 2)
                    raw_wpm = round((len(user_content)/5/time_taken)*60, 2)
                    mistake_ratio = f"{len(mistakes)}/{len(user_content)}"
                    accuracy = round(difflib.SequenceMatcher(None, text, user_content).ratio(), 2)*100
                    error_rate = round(len(mistakes) / time_taken, 2)
                    wpm = round(raw_wpm - error_rate, 2)
                    wpm = wpm if wpm >= 0 else 0
                    
                    description = "Your typing speed is above average 📈" if wpm >= 60 else "Your typing speed is below average 📉"

                    embed = discord.Embed(
                        title=f"{wpm} words per minute",
                        description=f"{description} {ctx.author.mention}"
                    )
                    embed.add_field(name="Raw WPM", value=f"{raw_wpm}", inline=False)
                    embed.add_field(name="Time taken", value=f"{time_taken} Seconds", inline=False)
                    embed.add_field(name="Accuracy", value=f"{accuracy}%", inline=False)
                    embed.add_field(name="Mistakes", value=mistake_ratio, inline=False)
                    embed.add_field(name="Error rate", value=f"{error_rate}%", inline=False)

                    embed.color = var.C_GREEN
                    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    embed.set_footer(text="Final typing speed is adjusted depending on the accuracy")
                    await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(description=f"Time is up! You failed to complete the test in time {ctx.author.mention}", color=var.C_RED))

    @commands.command()
    @has_command_permission()
    async def avatar(self, ctx, user:discord.User=None):
        if user is not None:
            avatar = user.avatar_url
            embed = discord.Embed(
                    title=f"Avatar of **{user}**",
                    color=var.C_TEAL
                    ).set_image(url=avatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"You need to define the user too! Follow this format:\n```{getprefix(ctx)}avatar <user>```\nFor user either user ID or mention can be used`")


    @commands.command()
    @has_command_permission()
    async def embed(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:

            embed = discord.Embed(
            title="Create an embed",
            description=f"React to the colour circle emojis below to quickly choose an embed colour! To add a custom hex color react to 🖌️\n When you are done selecting embed colour press the {var.E_CONTINUE} emoji to continue editing",
            color=var.C_MAIN
            ).set_footer(text="This message will become the live preview of the embed you are creating!"
            )
            preview = await ctx.send(embed=embed)
            emojis = [var.E_RED,var.E_PINK,var.E_GREEN,var.E_BLUE,var.E_ORANGE,var.E_YELLOW]
            colors = [0xFF0000, 0xFF58BC, 0x24FF00, 0x00E0FF, 0xFF5C00, 0xFFC700]

            await preview.add_reaction("🖌️")
            for i in emojis:
                await preview.add_reaction(i)
            await preview.add_reaction(var.E_CONTINUE)
            
            def previewreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == preview
            
            def msgcheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id

            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=previewreactioncheck)
                if str(reaction.emoji) == "🖌️":
                    await ctx.send("Send a hex colour code to make it the embed colour! You can use either 3 or 6 hex characters")
                    usermsg = await self.bot.wait_for('message', check=msgcheck)
                    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', usermsg.content.lower())
                    if match:
                        hexed = int(hex(int(usermsg.content.replace("#", ""), 16)), 0)
                        embed.color = hexed
                        await preview.edit(embed=embed)
                    else:
                        try:
                            await preview.remove_reaction("🖌️", ctx.author)
                        except discord.Forbidden:
                            pass
                        await ctx.send("Invalid hex code, try again")

                elif str(reaction.emoji) == var.E_CONTINUE:
                    break
                else:
                    index = emojis.index(str(reaction))
                    embed.color=colors[index]
                    try:
                        await preview.remove_reaction(emojis[index], ctx.author)
                    except discord.Forbidden:
                        pass
                    await preview.edit(embed=embed)
            try:
                await preview.clear_reactions()    
            except discord.Forbidden:
                pass
            titlebotmsg = await ctx.send(embed=discord.Embed(
            title="Title",
            description=f"Now send a message to make it the title of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
            color=var.C_BLUE)
            )
            usermsg = await self.bot.wait_for('message', check=msgcheck)
            embed.title = usermsg.content
            await preview.edit(embed=embed)
            await titlebotmsg.delete()

            descbotmsg = await ctx.send(embed=discord.Embed(
            title="Description",
            description=f"Now send a message to make it the description of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
            color=var.C_BLUE
            ).add_field(name="** **", value="Type `skip` if you don't want to set this")
            )
            usermsg = await self.bot.wait_for('message', check=msgcheck)
            if usermsg.content == "skip" or usermsg.content == "`skip`":
                embed.description = None
                await preview.edit(embed=embed)
                await descbotmsg.delete()
            else:
                embed.description = usermsg.content
                await preview.edit(embed=embed)
                await descbotmsg.delete()

            thumbnailbotmsg = await ctx.send(embed=discord.Embed(
            title="Thumbnail",
            description=f"Now send a message to make it the thumbnail of the [embed](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id})",
            color=var.C_BLUE
            ).add_field(name="** **", value="Type `skip` if you don't want to set this")
            )
            usermsg = await self.bot.wait_for('message', check=msgcheck)
            if usermsg.content.lower() in ["skip", "`skip`", "```skip```"]:
                await thumbnailbotmsg.delete()
            elif usermsg.attachments:
                embed.set_thumbnail(url=usermsg.attachments[0].url)
                await preview.edit(embed=embed)
                await thumbnailbotmsg.delete()
            elif usermsg.content.lower().startswith("https"):
                embed.set_thumbnail(url=usermsg.content)
                await thumbnailbotmsg.delete()
            else:
                await ctx.send("Uh oh it looks like the message you sent is not any link or image")
            
            embed.set_footer(text="")
            await preview.edit(embed=embed)
            await preview.add_reaction(var.E_ACCEPT)
            edit = await ctx.send(embed=discord.Embed(
                        description=f"React to the {var.E_ACCEPT} emoji in the original [preview](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id}) to send your embed! To edit more react to the respective emojis below",
                        color=var.C_BLUE
            ).add_field(name="Add field", value="React to 🇦", inline=False
            ).add_field(name="Footer", value="React to 🇫", inline=False
            ).add_field(name="Image", value="React to 🇮", inline=False
            ).add_field(name="Set Author", value="React to 🇺", inline=False)
            )
            def editreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == edit or reaction.message == preview
            editemojis = ["🇦", "🇫", "🇮", "🇺"]
            for i in editemojis:
                await edit.add_reaction(i)

            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=editreactioncheck)
                if str(reaction.emoji) == var.E_ACCEPT:
                    await channel.send(embed=embed)
                    await ctx.send("Embed sent in "+channel.mention+" !")
                    break
                if str(reaction.emoji) == "🇦":
                    fieldbotmsg = await ctx.send("Send a message and seperate your **Field name and value** with `|`\nFor example: This is my field name | This is the field value!")
                    usermsg = await self.bot.wait_for('message', check=msgcheck)
                    fieldlist = usermsg.content.split("|")
                    if len(fieldlist) != 2:
                        await ctx.send("Invalid format, make sure to add `|` between your field name and value")
                    else:
                        embed.add_field(name=fieldlist[0], value=fieldlist[1], inline=False)
                        await preview.edit(embed=embed)
                        await fieldbotmsg.delete()
                    try:
                        await edit.remove_reaction("🇦", ctx.author)
                    except discord.Forbidden:
                        pass

                if str(reaction.emoji) == "🇫":
                    footerbotmsg = await ctx.send("Send a message to make it the **Footer**!")
                    usermsg = await self.bot.wait_for('message', check=msgcheck)
                    embed.set_footer(text=usermsg.content)
                    await preview.edit(embed=embed)
                    await footerbotmsg.delete()
                    try:
                        await edit.clear_reaction("🇫")
                    except discord.Forbidden:
                        pass
                if str(reaction.emoji) == "🇮":
                    while True:
                        imagebotmsg = await ctx.send("Now send an image or link to add that **Image** to the embed!\nType `skip` if you don't want to set this")
                        usermsg = await self.bot.wait_for('message', check=msgcheck)   
                        try:
                            if usermsg.content in ["skip", "`skip`", "```skip```"]:
                                await ctx.send("Skipped image, react to 🇮 again to set it.")
                                await edit.remove_reaction("🇮", ctx.author)
                                break   
                            elif usermsg.attachments:
                                embed.set_image(url=usermsg.attachments[0].url)
                                await preview.edit(embed=embed)
                                await thumbnailbotmsg.delete()
                                try:
                                    edit.clear_reaction("🇮")
                                except discord.Forbidden:
                                    pass
                                break
                            else:
                                embed.set_image(url=usermsg.content)
                                await preview.edit(embed=embed)
                                await imagebotmsg.delete()
                                try:
                                    await edit.clear_reaction("🇮")
                                except discord.Forbidden:
                                    pass
                                break
                        except:
                            await ctx.send(embed=discord.Embed(title="Invalid image", description="Send the image file or link again", color=var.C_RED
                            ).set_footer(text="Make sure your message contains only the image, nothing else")
                            )

                if str(reaction.emoji) == "🇺":
                    while True:
                        if usermsg.content in ["skip", "`skip`", "```skip```"]:
                            break   
                        else:
                            authorbotmsg = await ctx.send("Now send userID or member mention to set them as the **author** of the embed\n Type `skip` if you dont't want to set this")
                            usermsg = await self.bot.wait_for("message", check=msgcheck)
                            userid = usermsg.content.strip("!@<>")
                            try:
                                authoruser = await self.bot.fetch_user(userid)
                                embed.set_author(name=authoruser, icon_url=authoruser.avatar_url)
                                await authorbotmsg.delete()
                                try:
                                    await edit.clear_reaction("🇺")
                                except discord.Forbidden:
                                    pass
                                await preview.edit(embed=embed)
                                break
                            except:
                                await ctx.send(embed=discord.Embed(title="Invalid user", description="Send the userID or mention again", color=var.C_RED
                                ).set_footer(text="Make sure your message contains only the user, nothing else")
                                )

        else:
            await ctx.send(f"You also need to define the channel too! Format:\n```{getprefix(ctx)}embed <#channel>```\nDon't worry, the embed won't be sent right away to the channel :D")

def setup(bot):
    bot.add_cog(Fun(bot))
