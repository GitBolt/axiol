import re
import os
import time
import discord
import asyncio
import textwrap
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import variables as var
from functions import random_text, getprefix
from ext.permissions import has_command_permission
import database as db
TYPE_15 = "<:15:866917795513892883>" 
TYPE_30 = "<:30:866917795261579304>"
TYPE_60 = "<:60:866917796507418634>"

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


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
    
    @commands.command()
    @has_command_permission()
    async def typingtest(self, ctx):
        botmsg = await ctx.send(embed=discord.Embed(
            title="Typing Test",
            description=f"Let's see how fast you can type! React to the respective emoji below to start.\n\n{TYPE_15} 15 Seconds Test\n{TYPE_30} 30 Seconds Test\n{TYPE_60} 60 Seconds Test\n{var.E_DECLINE} Cancel Test",
            color=var.C_BLUE
            )
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

        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        reaction, user = await  self.bot.wait_for("reaction_add", check=reactioncheck)
        if str(reaction.emoji) == var.E_DECLINE:
            await ctx.send(f" {var.E_ACCEPT} Cancelled typing test.")
        else:

            if  str(reaction.emoji) == TYPE_15:
                typing_time = 15
            elif str(reaction.emoji) == TYPE_30:
                typing_time = 30
            elif str(reaction.emoji) == TYPE_60:
                typing_time = 60

            botmsg = await ctx.send(embed=discord.Embed(
                description=f"You have selected **{typing_time}** seconds for typing test, react to {var.E_ACCEPT} to start!", 
                color=var.C_MAIN
                )
                )
            await botmsg.add_reaction(var.E_ACCEPT)
            await self.bot.wait_for("reaction_add", check=confirmcheck)

            text = random_text(typing_time)
            image = Image.open(os.path.dirname(os.getcwd()) + "/axiol/resources/backgrounds/typing_board.png")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(os.path.dirname(os.getcwd()) + "/axiol/resources/fonts/Poppins-Medium.ttf", 80)
            font2 = ImageFont.truetype(os.path.dirname(os.getcwd()) + "/axiol/resources/fonts/Poppins-Light.ttf", 48)
            draw.text((810, 55),str(typing_time) ,(184,184,184),font=font)
            offset = 300
            for line in textwrap.wrap(text, width=58):
                draw.text((72, offset), line ,(169,240,255),font=font2)
                offset += 80

            with BytesIO() as image_binary:
                image.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

            try:
                initial_time = time.time()
                usermsg = await self.bot.wait_for("message", check=messagecheck, timeout=typing_time)
                content = usermsg.content

                mistakes = []
                correct = []
                for i in content:
                    if i == text[content.index(i)]:
                        correct.append(i)
                    else:
                        mistakes.append(i)

                time_taken =  round(time.time() - initial_time, 2)
                total_chars = len(correct) + len(mistakes)
                raw_wpm = round((len(usermsg.content)/5/time_taken)*60, 2)
                accuracy = round((len(correct) / total_chars) * 100, 2) if len(correct) != 0 else 0
                mistakes = str(len(mistakes)) + "/" + str(total_chars)
                error_rate = round((len(mistakes) / time_taken)*60, 2)
                print(error_rate)
                wpm = round(raw_wpm - error_rate, 2)
                description = "Your typing speed is above average :ok_hand:" if wpm >= 60 else "Your typing speed is below average"

                embed = discord.Embed(
                    title=f"{wpm} words per minute",
                    description=f"{description} {ctx.author.mention}"
                )
                embed.add_field(name="Raw WPM", value=f"{raw_wpm}", inline=False)
                embed.add_field(name="Time taken", value=f"{time_taken} Seconds", inline=False)
                embed.add_field(name="Accuracy", value=f"{accuracy}%", inline=False)
                embed.add_field(name="Mistakes", value=mistakes)
                embed.add_field(name="Error rate", value=error_rate)

                embed.color = var.C_GREEN
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Final typing speed is adjusted depending on the accuracy.")
                await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(f"Time is up! You failed to complete the test in time {ctx.author.mention}")


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
                reaction, user = await self.bot.wait_for('reaction_add', check=previewreactioncheck, timeout=20.0)
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
