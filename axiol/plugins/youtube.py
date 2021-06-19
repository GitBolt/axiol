import discord
from discord.ext import commands, tasks
import requests
import variables as var
import database as db
from functions import getprefix


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #Simple check to see if this cog (plugin) is enabled
    async def cog_check(self, ctx):
        GuildDoc = db.PLUGINS.find_one({"_id": ctx.guild.id})
        if GuildDoc.get("YouTube") == True:
            return ctx.guild.id
        else:
            await ctx.send(embed=discord.Embed(
                description=f"{var.E_DISABLE} The Welcome plugin is disabled in this server",
                color=var.C_ORANGE
            ))


    @commands.command()
    async def ytadd(self, ctx, channel:discord.TextChannel=None, ytchannel:str=None):
        if channel and ytchannel is not None:
            r = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={var.YTAPI_KEY}&channelId={ytchannel}")
            if r.status_code == 400:
                await ctx.send(embed=discord.Embed(
                    title=f"{var.E_ERROR} Invalid YouTube Channel ID",
                    description="The YouTube channel ID is incorrect, maybe you copied a video ID? Maybe the channel is private?",
                    color=var.C_RED
                    ).set_thumbnail(url="https://cdn.discordapp.com/attachments/843519647055609856/855838497315225600/main.png")
                    )
            else:
                GuildDoc = db.YOUTUBE.find_one({"_id": ctx.guild.id})
                if GuildDoc is None:
                    db.YOUTUBE.insert_one({

                        "_id": ctx.guild.id,
                        "channels": {
                            ytchannel: channel.id
                        }
                                            
                        })
                elif ytchannel in GuildDoc.get("channels").keys():
                    await ctx.send("You have already setted up this YouTube channel :eyes:")
                else:
                    existingdata = GuildDoc.get("channels")
                    newdict = existingdata.copy()
                    newdict.update({ytchannel: channel.id})

                    newdata = {"$set":{
                        "channels": newdict
                    }}
                    db.YOUTUBE.update_one(GuildDoc, newdata)
                    await ctx.send(embed=discord.Embed(
                        title="Successfully added new YouTube upload",
                        description=f"Whenever the channel {ytchannel} uploads any new video, a message in {channel.mention} will be sent! To change the message or any other setting use the command `{getprefix(ctx)}help youtube`",
                        color=var.C_GREEN
                    ))
        else:   
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the Text Channel and YouTube channel ID to add upload notifications",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}addupload <#channel> <youtube_channel_id>`"
            )
            )

    @commands.command()
    async def ytremove(self, ctx, ytchannel:str=None):
        if ytchannel is not None:
            GuildDoc = db.YOUTUBE.get({"_id": ctx.guild.id})
            if GuildDoc is not None and ytchannel in GuildDoc.get("channels").keys():
                existingdata = GuildDoc.get("channels")
                newdict = existingdata.copy()
                newdict.pop(ytchannel)

                newdata = {"$set":{
                    "channels": newdict
                }}
                db.YOUTUBE.update_one(GuildDoc, newdata)
                await ctx.send(f"{var.E_ACCEPT} Successfully removed uploads notifications from https://youtube.com/channel/{ytchannel}")
            else:
                await ctx.send(f"{var.E_ERROR} The YouTube channel https://youtube.com/channel/{ytchannel} does not have any upload notifications setted up")
        else:   
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the YouTube channel ID to remove upload notifications",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}ytremove <youtube_channel_id>`"
            )
            )

    @commands.command()
    async def testapi(self, ctx, channel:str=None):
        if channel is not None:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={var.YTAPI_KEY}&channelId={channel}&part=id&order=date&maxResults=2").json()
            recentvideo_id = response["items"][0]["id"]["videoId"]
            print(recentvideo_id)
        else:
            pass


# @tasks.loop(minutes=5)
# async def uploadcheck():
#     pass
        


def setup(bot):
    pass
    #bot.add_cog(YouTube(bot))
