import discord
from discord.ext import commands
import youtube_dl
from utils.functions import getprefix
import utils.variables as var

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command()
    async def play(self, ctx, url=None):
        if url is not None:
            user_vc = ctx.author.voice.channel

            vc = await user_vc.connect()

            ydl_opts = {'format': 'bestaudio'}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
            
            vc.play(discord.FFmpegPCMAudio(URL))

        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define the url to play music too",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}play <url>`"
            )
            )         


    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client:
            await voice_client.disconnect()
            await ctx.send(f"Disconnected from the voice channel")
        else:
            await ctx.send("I am not connected to any voice channel")


def setup(bot):
    bot.add_cog(Music(bot))