import discord
from discord.ext import commands
import utils.variables as var
import utils.database as db
from utils.functions import getprefix
import random


class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("Verification") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Verification plugin is disabled in this server",
                color=var.C_ORANGE
            ))

    @commands.command()
    async def verifyinfo(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        verifytype = GuildDoc.get("type")
        if verifytype == "command":

            embed = discord.Embed(
            title=f"This server has Command verification",
            description="This is a basic type of verification where users enter a command in the verification channel and they are quickly verified and given access to other channels, this can be used to verify people and low-medium level raid/spam bot.",
            color=var.C_TEAL
            )
        else:
            embed = discord.Embed(
            title="This server has Bot verification",
            description="This is a slightly more advanced bot captcha like verification most suitable to bypass advance bot raids, after users enter the command a captcha image is sent in the channel with distorted text (good enough for a human to read) and if the users enter the code correctly they are verified. The image lasts only for 15 seconds, entering the command again will send another new image.",
            color=var.C_TEAL
            )
        embed.add_field(name="Verification Channel", value=self.bot.get_channel(GuildDoc.get("channel")).mention)
        embed.add_field(name="Not Verified Role", value=ctx.guild.get_role(GuildDoc.get("roleid")).mention)
        await ctx.send(embed=embed)



    @commands.command()
    async def verifychannel(self, ctx, channel:discord.TextChannel=None):
        if channel is not None:
            GuildDoc = db.VERIFY.find_one({"_id": ctx.guild.id})  
            NVerified = ctx.guild.get_role(GuildDoc.get("roleid"))
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(ctx.guild.default_role, view_channel=True) 
            await self.bot.get_channel(GuildDoc.get("channel")).set_permissions(NVerified, view_channel=False)
            newdata = {"$set":{
                "channel": channel.id
            }}
            db.VERIFY.update_one(GuildDoc, newdata)
            await self.bot.get_channel(channel.id).set_permissions(NVerified, view_channel=True)
            
            embed = discord.Embed(
            title="Successfully changed the verification channel",
            description=f"Members will now be verified in {channel.mention}!",
            color=var.C_BLUE
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the verification channel to change it",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}verifychannel #channel`"))



    @commands.command()
    async def verifyswitch(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        if GuildDoc.get("type") == "command":
            newdata = {"$set":{
                "type": "bot"
            }}
        else:
            newdata = {"$set":{
                "type": "command"
            }}
        db.VERIFY.update_one(GuildDoc, newdata)
        await ctx.send(embed=discord.Embed(
                    title="Switched to " + newdata.get("$set").get("type") + " verification",
                    description="Use the command again to switch to the other method",
                    color=var.C_GREEN)
        )
    


    @commands.command()
    async def verifyremove(self, ctx):
        GuildDoc = db.VERIFY.find_one({"_id":ctx.guild.id})
        db.VERIFY.delete_one(GuildDoc)
        await discord.utils.get(ctx.guild.roles, name="Not Verified").delete()
        GuildPluginDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        newdata = {"$set":{
            "Verification": False
        }}
        db.PLUGINS.update_one(GuildPluginDoc, newdata)
        await ctx.send("Successfully removed verification from this server!")



    @commands.command()
    async def verify(self, ctx):
        if ctx.channel.id in db.VERIFY.distinct("channel"): #Verify channel IDs
            await ctx.message.delete()
            if db.VERIFY.find_one({"_id":ctx.guild.id}).get("type") == "command": #Command verification
                roleid = db.VERIFY.find_one({"_id": ctx.guild.id}).get("roleid")
                role = ctx.guild.get_role(roleid)

                await ctx.send(f"Verification successful {var.E_ACCEPT} - **{ctx.author}**", delete_after=1)
                await ctx.author.remove_roles(role)

            else: #Bot verification
                Image = random.choice([
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170831586787398/7h3fpaw1.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170832744415283/bs4hm1gd.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170834484789309/hdmxe425.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170834514018304/kp6d1vs9.png',
                        'https://cdn.discordapp.com/attachments/807140294764003350/808170835957383189/jd3573vq.png',
                        ])    

                embed = discord.Embed(
                    title="Beep Bop,  are you a bot?",
                    description = 'Enter the text given in the image below to verify yourself',
                    colour = var.C_MAIN
                    ).set_image(url=Image
                    ).set_footer(text='You have 15 seconds to enter the text, if you failed to enter it in time then type the command again.'
                    )
                botmsg = await ctx.send(embed=embed, delete_after=15.0)

                def codecheck(message):
                    return message.author == ctx.author and message.channel.id == ctx.channel.id
                
                usermsg = await self.bot.wait_for('message', check=codecheck, timeout=15.0)

                #ayo bots aren't this smart
                code = embed.image.url[77:-4]
                if usermsg.content == code:
                    roleid = db.VERIFY.find_one({"_id": ctx.guild.id}).get("roleid")
                    role = ctx.guild.get_role(roleid)
                    await ctx.send(f"Verification successful {var.E_ACCEPT} - **{ctx.author}**", delete_after=1)
                    await ctx.author.remove_roles(role)
                    await botmsg.delete()
                    await usermsg.delete()
                else:
                    await ctx.send("Wrong, try again", delete_after=1)
                    await botmsg.delete()
                    await usermsg.delete()



def setup(bot):
    bot.add_cog(Verification(bot))