import re
import asyncio
import discord
from discord.ext import commands
import variables as var
from functions import getprefix
import database as db
from ext.permissions import has_command_permission

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @has_command_permission()
    async def source(self, ctx):
        embed = discord.Embed(
        title="My Github Source Code Woohoo", 
        description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", 
        color=var.C_TEAL
        ).set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/shift-logotypes/32/Github-512.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def invite(self, ctx):
        embed = discord.Embed(
        title="My invite link!",
        description="[Invite me from here](https://discord.com/oauth2/authorize?client_id=843484459113775114&permissions=473295959&scope=bot)",
        color=var.C_BLUE
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def suggest(self, ctx, *, desc=None):
        if desc is not None:
            channel = self.bot.get_channel(843548616505294848) #Support server suggestion channel

            embed = discord.Embed(
            title=f"{ctx.author}'s idea", 
            description=f"This idea came from a server named **{ctx.guild.name}**!", 
            color=var.C_BLUE
            ).add_field(name="Suggestion", value=desc
            )
            msg = await channel.send(embed=embed)
            await msg.add_reaction(var.E_ACCEPT)
            await msg.add_reaction(var.E_DECLINE)
            await ctx.send("Suggestion sent to the support server!")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format\n```{getprefix(ctx)} <description of your idea>```\nDon't forget the space after prefix :D")


    @commands.command()
    @has_command_permission()
    async def about(self, ctx):
        guildcount = 0
        membercount = 0
        ping = f"{round(self.bot.latency*1000)}ms"
        for guild in self.bot.guilds:
            guildcount +=1
            membercount += guild.member_count

        embed = discord.Embed(
        title="Some information about me :flushed:",
        color=var.C_MAIN
        ).add_field(name="Server Count", value=guildcount, inline=False
        ).add_field(name="Members", value=membercount, inline=False
        ).add_field(name="Made by", value="Bolt#8905", inline=False
        ).add_field(name="Creation date", value="16 May, 2021", inline=False
        ).set_footer(text=f"Ping: {ping}"

        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    @has_command_permission()
    async def stats(self, ctx):
        embed = discord.Embed(
        title=f"{ctx.guild.name}", 
        color=var.C_TEAL)
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=False)
        embed.add_field(name="All Members", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=False)
        embed.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels), inline=False)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=False)
        embed.add_field(name="Boost Level", value=ctx.guild.premium_tier, inline=False)
        embed.add_field(name="Created at", value=str(ctx.guild.created_at.strftime("%Y - %m - %d")) , inline=False)
        embed.set_thumbnail(url = ctx.guild.icon_url)

        GuildVerifyDoc = db.VERIFY.find_one({"_id": ctx.guild.id})
        if GuildVerifyDoc is not None:
            role = ctx.guild.get_role(GuildVerifyDoc.get("roleid"))
        
            count = 0
            for member in ctx.guild.members:
                if role in member.roles:
                    count += 1
            embed.add_field(name="Non Verified Members", value=count)

        await ctx.send(embed=embed)


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


    @commands.command()
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


def setup(bot):
    bot.add_cog(Commands(bot))
