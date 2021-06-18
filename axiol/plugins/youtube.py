import discord
from discord.ext import commands
import requests
import variables as var

class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def testapi(self, ctx, channel:str=None):
        if channel is not None:
            response = requests.get(f"https://www.googleapis.com/youtube/v3/search?key={var.YTAPI_KEY}&channelId={channel}&part=snippet,id&order=date&maxResults=2").json()
            recentvideo_id = response["items"][0]["id"]["videoId"]
            print(r.json())
        else:
            pass



def setup(bot):
    bot.add_cog(YouTube(bot))