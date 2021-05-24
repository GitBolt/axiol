import discord
from discord.ext import commands
import utils.vars as var
from utils.funcs import getprefix

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def source(self, ctx):
        embed = discord.Embed(
        title="My Github Source Code Woohoo", 
        description="[GitBolt - Axiol](https://github.com/GitBolt/Axiol)", 
        color=var.CTEAL
        ).set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/shift-logotypes/32/Github-512.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def suggest(self, ctx, *, desc=None):
        if desc is not None:
            channel = self.bot.get_channel(843548616505294848) #Support server suggestion channel id

            embed = discord.Embed(
            title=f"{ctx.author}'s idea", 
            description=f"This idea came from a server named **{ctx.guild.name}**!", 
            color=var.CBLUE
            ).add_field(name="Suggestion", value=desc
            )
            msg = await channel.send(embed=embed)
            await msg.add_reaction(var.ACCEPT)
            await msg.add_reaction(var.DECLINE)
            await ctx.send("Suggestion sent to the support server!")
        else:
            await ctx.send(f"You need to describe your idea too! This is the format\n```{getprefix(ctx)} <description of your idea>```\nDon't forget the space after prefix :D")


    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
        title="Axiol invite",
        description="[Invite the bot from here](https://discord.com/api/oauth2/authorize?client_id=843484459113775114&permissions=8&scope=bot)",
        color=var.CBLUE
        ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png"
        )
        await ctx.send(embed=embed)


    @commands.command()
    async def embed(self, ctx, channel:discord.TextChannel=None):

        if channel is not None:
            embed = discord.Embed(
            title="Create an embed",
            description=f"React to the emojis below to choose your color! When you are done press the {var.CONTINUE} emoji to continue editing",
            color=var.CMAIN
            ).set_footer(text="This message will become the live preview of the embed you are creating!"
            )
            preview = await ctx.send(embed=embed)
            emojis = [var.ERED,var.EPINK,var.EGREEN,var.EBLUE,var.EORANGE,var.EYELLOW]
            colors = [0xFF0000, 0xFF58BC, 0x24FF00, 0x00E0FF, 0xFF5C00, 0xFFC700]

            for i in emojis:
                await preview.add_reaction(i)
            await preview.add_reaction(var.CONTINUE)
            
            def previewreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == preview
            
            def msgcheck(message):
                return message.author == ctx.author and message.channel.id == ctx.channel.id

            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=previewreactioncheck)
                if str(reaction.emoji) == var.CONTINUE:
                    break

                index = emojis.index(str(reaction))
                embed.color=colors[index]
                await preview.remove_reaction(emojis[index], ctx.author)
                await preview.edit(embed=embed)

            await preview.clear_reactions()    
            titlebotmsg = await ctx.send("Now send a message to make it the **Title** of the embed :D")
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
            embed.title = usermsg.content
            await preview.edit(embed=embed)
            await titlebotmsg.delete()

            descbotmsg = await ctx.send("Now send a message to make it the **Description**! Type `skip` if you don't want to")
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
            if usermsg.content == "skip" or usermsg.content == "`skip`":
                await descbotmsg.delete()
            else:
                embed.description = usermsg.content
                await preview.edit(embed=embed)
                await descbotmsg.delete()

            thumbnailbotmsg = await ctx.send("Now send a image or link to make it the **Thumbnail**! Type `skip` if you don't want to")
            usermsg = await self.bot.wait_for('message', check=msgcheck, timeout=60.0)
            if usermsg.attachments:
                embed.set_thumbnail(url=usermsg.attachments[0].url)
                await preview.edit(embed=embed)
                await thumbnailbotmsg.delete()
            elif usermsg.content == "skip" or usermsg.content == "`skip`":
                await thumbnailbotmsg.delete()
            else:
                embed.set_thumbnail(url=usermsg.content)
                await preview.edit(embed=embed)
                await thumbnailbotmsg.delete()
            
            await preview.add_reaction(var.ACCEPT)
            edit = await ctx.send(embed=discord.Embed(
                        description=f"React to the {var.ACCEPT} emoji in the original [preview](https://discord.com/channels/{ctx.guild.id}/{preview.channel.id}/{preview.id}) to send your embed! To edit more react to the respective emojis below",
                        color=var.CBLUE
            ).add_field(name="Add field", value="React to 🇦"
            ).add_field(name="Footer", value="React to 🇫"
            ).add_field(name="Image", value="React to 🇮"
            ).add_field(name="Author", value="React to 🇺")
            )
            def editreactioncheck(reaction, user):
                return user == ctx.author and reaction.message == edit or reaction.message == preview
            editemojis = ["🇦", "🇫", "🇮", "🇺"]
            for i in editemojis:
                await edit.add_reaction(i)

            while True:
                reaction, user = await self.bot.wait_for('reaction_add', check=editreactioncheck)
                if str(reaction.emoji) == var.ACCEPT:
                    break
                if str(reaction.emoji) == "🇦":
                    await ctx.send("AAAAAA")
                if str(reaction.emoji) == "🇫":
                    await ctx.send("FFFFF")
                if str(reaction.emoji) == "🇮":
                    await ctx.send("IIII")
                if str(reaction.emoji) == "🇺":
                    await ctx.send("UUUUU")
            await channel.send(embed=embed)
            await ctx.send("Embed sent in "+channel.mention+" !")
        else:
            await ctx.send(f"You also need to define the channel too! Format:```{getprefix(ctx)}embed <#channel>```Don't worry, the embed won't be sent right away!")

def setup(bot):
    bot.add_cog(Commands(bot))