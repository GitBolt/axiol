import time
import random
import asyncio
import discord
import datetime
from discord.ext import commands, tasks
import database as db
import variables as var
from functions import getprefix
from ext.permissions import has_command_permission



class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot  = bot
        self.check_gw.start()

    @commands.command()
    @has_command_permission()
    async def gstart(self, ctx, channel:discord.TextChannel=None):
        if channel is None:
            return await ctx.send(embed=discord.Embed(
                description="🚫 You need to define the channel too!",
                color=var.C_ORANGE
                ).add_field(name="Format", value=f"```{getprefix(ctx)}gstart <#channel>```", inline=False
                ).add_field(name="Don't worry, this won't send the giveaway right away!", value="** **")
                )

        data = {"Channel": channel.mention}
        questions = {
            "Prize": "🎁 Enter the giveaway prize, what are winners going to get?", 
            "Duration": "⏳ Enter the giveaway time duration, how long should the giveaway last?", 
            "Winners": "📝 Enter the winner amount, how many winners should there be?",
            "Host": "🔍 Enter the giveaway host, who is hosting the giveaway? It can be you, someone else, a discord server or any other kind person :D"
            }
        
        def messagecheck(message):
            return message.author == ctx.author and message.channel.id == ctx.channel.id

        def reactioncheck(reaction, user):
            if str(reaction.emoji) == var.E_ACCEPT:
                return user == ctx.author and reaction.message == botmsg

        def time_converter(string, type_):
            if type_ == "Duration":
                formats = ("s", "m", "h", "d")
                conversions = {"s":1, "m":60, "h":3600, "d":86400}

                if string[-1] in formats and len([l for l in string if not l.isdigit()]) == 1:
                    return True, int(string[:-1]) * conversions[string[-1]]
                else:
                    return False, None
            #No other checks needed so just return True
            elif type_ == "Winners":
                return string.isdigit(), None
            else:
                return True, None

        embed = discord.Embed(
            color=var.C_BLUE
            ).set_footer(text="To stop the proccess, enter cancel"
            ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png")

        for q in questions:
            embed.title = q
            embed.description = questions[q]
            embed.clear_fields()
            embed.add_field(name="Information", value="\n".join([f"{x}: **{y[0] if type(y) == tuple else y}**" for x,y in data.items()]))
            await ctx.send(embed=embed)
            usermsg = await self.bot.wait_for("message", check=messagecheck, timeout=60)
            check, value = time_converter(usermsg.content, q)
            if usermsg.content == "cancel":
                await ctx.send("Cancelled giveaway proccess.")
                return

            if check:
                data.update({q: usermsg.content}) if value == None else data.update({q: (usermsg.content, value)})
            else:
                tries = 3
                status = True
                while status:
                    tries -= 1
                    if tries == 0:
                        await ctx.send(f"The giveaway proccess has been cancelled because you failed to enter {q.lower()} field in correct format.")
                        return
                    else:
                        if q == "Duration":
                            await ctx.send(embed=discord.Embed(description="Invalid format for time duration, try again.\nExample:\n> 24h", color= var.C_ORANGE
                                    ).add_field(name="All formats", value="s: seconds\nm: minutes\nh: hours\nd: days\n", inline=False
                                    ).add_field(name="Tries left", value=tries
                                    ))
                        else:
                            await ctx.send(embed=discord.Embed(description="Winner amount can only be a positive number!", color= var.C_ORANGE
                                    ).add_field(name="Example", value="5", inline=False
                                    ).add_field(name="Tries left", value=tries
                                    ))
                        usermsg = await self.bot.wait_for("message", check=messagecheck, timeout=60)
                        if usermsg.content == "cancel":
                            await ctx.send("Cancelled giveaway proccess.")
                            return
                        check, value = time_converter(usermsg.content, q)
                        if check:
                            status = False
                else:
                    data.update({q: (usermsg.content, value)})

        embed = discord.Embed(
            title="Confirm giveaway",
            description=f"You are about to start the giveaway! Press {var.E_ACCEPT} to start it.",
            color=var.C_GREEN
        ).add_field(name="Channel", value=data["Channel"], inline=False
        ).add_field(name="Prize", value=data["Prize"], inline=False
        ).add_field(name="Duration", value=data["Duration"][0], inline=False
        ).add_field(name="Winner amount", value=data["Winners"], inline=False
        ).add_field(name="Hosted by", value=data["Host"], inline=False)

        botmsg = await ctx.send(embed=embed)
        await botmsg.add_reaction(var.E_ACCEPT)
        await self.bot.wait_for("reaction_add", check=reactioncheck, timeout=60)

        end_time = round(time.time() + int(data["Duration"][1]))
        
        days, hours, minutes = round((end_time - time.time())/86400), round((end_time - time.time())/3600), round((end_time - time.time())/60)
        embed = discord.Embed(
            title=data["Prize"],
            description=f"React to the 🎉 emoji to participate!\n\n📝 Winner amount: **{data['Winners']}**\n🔍 Hosted by: **{data['Host']}**",
            color=var.C_MAIN,
            timestamp= datetime.datetime.now()
        ).add_field(name="⏳ Ending time", value=f"{days} days, {hours} hours, {minutes} minutes"
        ).set_thumbnail(url=ctx.guild.icon.url
        )
        gwmsg = await channel.send(content="New giveaway woohoo!", embed=embed)
        await gwmsg.add_reaction("🎉")
        
        db.GIVEAWAY.insert_one({"channel_id":channel.id, "message_id": gwmsg.id, "end_time": end_time, "winner_amount": int(data["Winners"])})

    @gstart.error
    async def gstart_error(self, ctx, error):
        if isinstance(error, asyncio.TimeoutError):
            await ctx.send(embed=discord.Embed(description="Time is up! you failed to respond under 60 seconds, the giveaway proccess has been stopped."), color=var.C_RED)


    @commands.command()
    @has_command_permission()
    async def gshow(self, ctx):
        pass

    
    @tasks.loop(seconds=5)
    async def check_gw(self):
        await self.bot.wait_until_ready()
        for i in db.GIVEAWAY.find({}):
            channel = self.bot.get_channel(i["channel_id"])
            message = await channel.fetch_message(i["message_id"])
            end_time = i["end_time"]
            winner_amount = i["winner_amount"]
            embed_data = message.embeds[0].to_dict()
            hosted_by = embed_data["description"].split("\n")[-1]
            days, hours, minutes = round((end_time - time.time())/86400), round((end_time - time.time())/3600), round((end_time - time.time())/60)

            if time.time() > i["end_time"]:

                users = await message.reactions[0].users().flatten()
                users.remove(self.bot.user)
                if len(users) < winner_amount:
                    winners = random.sample(users, len(users))
                else:
                    winners = random.sample(users, winner_amount)
                db.GIVEAWAY.delete_one(i)

                embed = discord.Embed(
                    title="Giveaway over",
                    description= f"🎁 {embed_data['title']}\n{hosted_by}\n📩 **{len(users)}** entries\n📋 **{len(winners)}** winners",
                    timestamp = datetime.datetime.now(),
                    color=var.C_BLUE
                ).set_footer(text="Ended")
                await message.edit(embed=embed)
                if len(users) > 0:
                    await channel.send(f"Congratulations, you have won **{embed_data['title']}**!" + ", ".join([w.mention for w in winners]))
                else:
                    await channel.send("Aw man, no one participated :(")
            else:
                embed = discord.Embed(
                    title=embed_data["title"],
                    description=embed_data["description"],
                    color=var.C_MAIN,
                    timestamp = datetime.datetime.now()
                    ).add_field(name=embed_data["fields"][0]["name"], value=f"{days} days, {hours} hours, {minutes} minutes"
                    ).set_thumbnail(url=embed_data["thumbnail"]["url"]
                    )
                await message.edit(embed=embed)
                

def setup(bot):
    bot.add_cog(Giveaway(bot))
