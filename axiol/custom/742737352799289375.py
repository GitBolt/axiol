import discord
from discord.ext import commands
from discord.ext.commands import check, Context
import database as db
import variables as var
from functions import getprefix


def is_user(*userids):
    async def predicate(ctx: Context):
        return ctx.author.id in userids
    return check(predicate)


#Custom cog for Chemistry Help discord server | 742737352799289375
class ChemistryHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Simple check to make sure this custom cog only runs on this server and test server
    def cog_check(self, ctx):
        return ctx.guild.id == 742737352799289375 or 807140294276415510


    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_addmsg(self, ctx, *, msg:str=None):
        if msg is not None:

            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 0})
            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ').lower()
                GuildCol.insert_one({
                    "_id": 0,
                   trigger: response
                })
                await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with response **{response}**", color=var.C_BLUE))
            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                response = msg.split("|")[1].lstrip(' ').rstrip(' ')

                GuildCol.update(data, {"$set": {trigger: response}})
                await ctx.send(embed=discord.Embed(description=f"Added the message **{trigger}** with response **{response}**", color=var.C_BLUE))
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define both the message and it's response",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addmsg <msg> | <response>`"))


    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_removemsg(self, ctx, *, msg:str=None):
        if msg is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            data = GuildCol.find_one({"_id":0})
            if data is not None:
                if msg.lower() in data.keys():
                    res = data.get(msg.lower())
                    GuildCol.update_one(data, {"$unset": {msg.lower(): ""}})
                    await ctx.send(f"Successfully removed the message **msg** which was having the response **{res}**")
                else:
                    await ctx.send("This message has no responses setted up")
            else:
                await ctx.send("You haven't setted up any message yet...")


    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_allmsgs(self, ctx):
        GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
        data = GuildCol.find_one({"_id":0})
        if data is not None:
            rramount = len(data)
            if rramount <= 10:
                exactpages = 1
            else:
                exactpages = rramount / 10
            if type(exactpages) != int:
                all_pages = round(exactpages) + 1
            else:
                all_pages = exactpages

            embed = discord.Embed(
            title="All message responses", 
            color=var.C_MAIN
            )
            async def pagination(current_page, all_pages, embed):
                pagern = current_page + 1
                embed.set_footer(text=f"Page {pagern}/{all_pages}")
                embed.clear_fields()

                rrcount = (current_page)*10
                rr_amount = current_page*10
                for i in list(data.items())[rr_amount:]:
                    rrcount += 1
                    embed.add_field(name=i[0], value=i[1], inline=False)
                    if rrcount == (current_page)*10 + 10:
                        break

            rrcount = 0
            for i in data:
                rrcount += 1
                embed.add_field(name=i, value=data.get(i), inline=False)
                if rrcount == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction("◀️")
            await botmsg.add_reaction("⬅️")
            await botmsg.add_reaction("➡️")
            await botmsg.add_reaction("▶️")

            def reactioncheck(reaction, user):
                if str(reaction.emoji) == "◀️" or str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡️" or str(reaction.emoji) == "▶️":
                    return user == ctx.author and reaction.message == botmsg
            
            current_page = 0
            while True:
                reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
                if str(reaction.emoji) == "◀️":
                    try:
                        await botmsg.remove_reaction("◀️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = 0
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await botmsg.remove_reaction("➡️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await botmsg.remove_reaction("⬅️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page -= 1
                    if current_page < 0:
                        current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await botmsg.remove_reaction("▶️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = all_pages-1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

        else:
            await ctx.send("There are no message reactions yet")

    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_addreact(self, ctx, *, msg:str=None):
        if msg is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]

            data = GuildCol.find_one({"_id": 1})
            if data is None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with reaction **{emoji}**", color=var.C_BLUE))
                except :
                    await ctx.send("Sorry but it seems like either the emoji is invalid or it's a custom emoji from a server where I am not in hence can't use this emoji either :(")
                
                GuildCol.insert_one({
                    "_id": 1,
                   trigger: emoji
                })
            else:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')

                try:
                    await ctx.message.add_reaction(emoji)
                    await ctx.send(embed=discord.Embed(description=f"Added the message **{msg}** with reaction **{emoji}**", color=var.C_BLUE))
                except :
                    await ctx.send("Sorry but it seems like either the emoji is invalid or it's a custom emoji from a server where I am not in hence can't use this emoji either :(")

                GuildCol.update(data, {"$set": {trigger: emoji}})
                
        else:
            await ctx.send(embed=discord.Embed(
            description="🚫 You need to define both the message and it's reaction",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addreaction <msg> <emoji>`"))



    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_removereact(self, ctx, *, msg:str=None):
        if msg is not None:
            GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
            data = GuildCol.find_one({"_id":1})
            if data is not None:
                trigger = msg.split("|")[0].lstrip(' ').rstrip(' ').lower()
                emoji = msg.split("|")[1].lstrip(' ').rstrip(' ')
                if trigger in data.keys():
                    GuildCol.update(data, {"$unset": {trigger.lower(): emoji}})
                    await ctx.send(f"Successfully removed {emoji} reaction from **{trigger}** message")
                else:
                    await ctx.send("This message and emoji combination does not exist")
            else:
                await ctx.send("You haven't setted up any reaction yet...")

                    

    @commands.command()
    @is_user(565059698399641600, 791950104680071188)
    async def chem_allreacts(self, ctx):
        GuildCol = db.CUSTOMDATABASE[str(ctx.guild.id)]
        data = GuildCol.find_one({"_id":1})
        if data is not None:
            rramount = len(data)
            if rramount <= 10:
                exactpages = 1
            else:
                exactpages = rramount / 10
            if type(exactpages) != int:
                all_pages = round(exactpages) + 1
            else:
                all_pages = exactpages

            embed = discord.Embed(
            title="All message reactions", 
            color=var.C_MAIN
            )
            async def pagination(current_page, all_pages, embed):
                pagern = current_page + 1
                embed.set_footer(text=f"Page {pagern}/{all_pages}")
                embed.clear_fields()

                rrcount = (current_page)*10
                rr_amount = current_page*10
                for i in list(data.items())[rr_amount:]:
                    rrcount += 1
                    embed.add_field(name=i[0], value=i[1], inline=False)
                    if rrcount == (current_page)*10 + 10:
                        break

            rrcount = 0
            for i in data:
                rrcount += 1
                embed.add_field(name=i, value=data.get(i), inline=False)
                if rrcount == 10:
                    break

            embed.set_footer(text=f"Page 1/{all_pages}")
            botmsg = await ctx.send(embed=embed)
            await botmsg.add_reaction("◀️")
            await botmsg.add_reaction("⬅️")
            await botmsg.add_reaction("➡️")
            await botmsg.add_reaction("▶️")

            def reactioncheck(reaction, user):
                if str(reaction.emoji) == "◀️" or str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡️" or str(reaction.emoji) == "▶️":
                    return user == ctx.author and reaction.message == botmsg
            
            current_page = 0
            while True:
                reaction, user = await self.bot.wait_for("reaction_add", check=reactioncheck)
                if str(reaction.emoji) == "◀️":
                    try:
                        await botmsg.remove_reaction("◀️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = 0
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "➡️":
                    try:
                        await botmsg.remove_reaction("➡️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "⬅️":
                    try:
                        await botmsg.remove_reaction("⬅️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page -= 1
                    if current_page < 0:
                        current_page += 1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

                if str(reaction.emoji) == "▶️":
                    try:
                        await botmsg.remove_reaction("▶️", ctx.author)
                    except discord.Forbidden:
                        pass
                    current_page = all_pages-1
                    await pagination(current_page, all_pages, embed)
                    await botmsg.edit(embed=embed)

        else:
            await ctx.send("There are no message reactions yet")


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id in [742848285416357970, 742849666256732170, 844657766794788884, 846840113543905383] and message.author.bot == False:

            GuildCol = db.CUSTOMDATABASE[str(message.guild.id)]
            msgdata = GuildCol.find_one({"_id": 0})
            reactiondata = GuildCol.find_one({"_id": 1})
            if msgdata is not None:
                if message.content.lower() in msgdata.keys():
                    await message.channel.send(msgdata.get(message.content.lower()))

            if reactiondata is not None:
                if message.content.lower() in reactiondata.keys():
                    await message.add_reaction(reactiondata.get(message.content.lower()))      

    
def setup(bot):
    bot.add_cog(ChemistryHelp(bot))