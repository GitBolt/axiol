import os
import time
import asyncio
import discord
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import variables as var
import textwrap
from functions import random_text

TYPE_15 = "<:15:866917795513892883>" 
TYPE_30 = "<:30:866917795261579304>"
TYPE_60 = "<:60:866917796507418634>"

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
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

                embed.color = var.C_GREEN
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Final typing speed is adjusted depending on the accuracy.")
                await ctx.send(embed=embed)

            except asyncio.TimeoutError:
                await ctx.send(f"Time is up! You failed to complete the test in time {ctx.author.mention}")

def setup(bot):
    bot.add_cog(Fun(bot))
