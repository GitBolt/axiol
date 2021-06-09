import os
import discord
import asyncio
import itertools
from discord.ext import commands
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

import utils.variables as var
from utils.functions import getprefix


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(embed=discord.Embed(
                description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", 
                color=var.C_BLUE))

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)


    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""

        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                source = await YTDLSource.regather_stream(source, loop=self.bot.loop)

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Now playing", description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", color=discord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass


    def get_player(self, ctx):
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player


    @commands.command(aliases=["join"])
    async def connect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(embed=discord.Embed(
                        description="Since you have not defined any voice channel in the command nor you are in one, where am I supposed to connect :thinking:", 
                        color=var.C_ORANGE))

        vc = ctx.voice_client
        if channel is not None:
            if vc:
                if vc.channel.id == channel.id:
                    return
                await vc.move_to(channel)
            else:
                await channel.connect()

            await ctx.send(embed=discord.Embed(
                        description=f"{var.E_ACCEPT} Successfully connect to {channel.name}",
                        color=var.C_GREEN
            ))


    @commands.command()
    async def play(self, ctx, *, search:str=None):
        if search is not None:

            await ctx.trigger_typing()

            vc = ctx.voice_client

            if not vc:
                await ctx.invoke(self.connect)

            player = self.get_player(ctx)

            source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

            await player.queue.put(source)
        else:
            await ctx.send(embed=discord.Embed(
            description=f"{var.E_ERROR} You need to define your search too!",
            color=var.C_RED
            ).add_field(name="Format", value=f"`{getprefix(ctx)}play <search>`"
            ).set_footer(text="For search either any YouTube link can be used or any related search query")
            )


    @commands.command()
    async def pause(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            await ctx.send(embed=discord.Embed(
                    description="I am currently not playing anything", 
                    color=var.C_ORANGE
                    ))

        elif vc.is_paused():
            await ctx.send(embed=discord.Embed(
                        description=f"I am have already paused playing",
                        color=var.C_ORANGE
            ))

        else:
            vc.pause()
            await ctx.send(embed=discord.Embed(
                        description=f"Paused playing `{vc.source.title}`",
                        color=var.C_BLUE
            ))


    @commands.command()
    async def resume(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))

        elif not vc.is_paused():
            await ctx.send(embed=discord.Embed(
                        description="Continuing to play since it was never paused",
                        color=var.C_BLUE
            ))

        else:
            vc.resume()
            await ctx.send(embed=discord.Embed(
                        description=f"Resumed playing `{vc.source.title}`",
                        color=var.C_TEAL
            ))



    @commands.command()
    async def skip(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
    

    @commands.command()
    async def remove(self, ctx, pos : int=None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos-1]
                del player.queue._queue[pos-1]
                embed = discord.Embed(title="", description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]", color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="", description=f'Could not find a track for "{pos}"', color=discord.Color.green())
                await ctx.send(embed=embed)


    @commands.command()
    async def queue(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))


        player = self.get_player(ctx)
        if player.queue.empty():
            await ctx.send(embed=discord.Embed(
                            description="Queue is empty since only one thing is playing right now", 
                            color=var.C_BLUE
                            ))

        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)


        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(f"**{(upcoming.index(_)) + 1}.** [{_['title']}]({_['webpage_url']}) - `{duration}` | {_['requester']}\n" for _ in upcoming)
        fmt = f"\n__**Now Playing**__\n[{vc.source.title}]({vc.source.web_url}) - `{duration}` | {vc.source.requester}\n\n**__Up Next__**\n" + fmt + f"\n*{len(upcoming)} songs in queue*"
        
        embed = discord.Embed(title=f'Queue for this server', description=fmt, color=var.C_MAIN)
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


    @commands.command()
    async def np(self, ctx):
        vc = ctx.voice_client
        player = self.get_player(ctx)

        if vc is not None and player.current:
            seconds = vc.source.duration % (24 * 3600) 
            hour = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            if hour > 0:
                duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
            else:
                duration = "%02dm %02ds" % (minutes, seconds)

            embed = discord.Embed(description=f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`", color=var.C_MAIN)
            embed.set_author(icon_url=self.bot.user.avatar_url, name=f"Now Playing 🎶")
            await ctx.send(embed=embed)

        elif vc is None:
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))

        else:
            await ctx.send(embed=discord.Embed(
                        description="I am currently not playing anything", 
                        color=var.C_ORANGE))
        



    @commands.command()
    async def volume(self, ctx, *, vol: float=None):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel", 
                color=var.C_ORANGE))
        
        if not vol:
            return await ctx.send(embed=discord.Embed(
                            title=f"{vc.source.title}",
                            description=f"Current volume is **{(vc.source.volume)*100}%**", 
                            color=var.C_BLUE))

        if not 0 < vol < 101:
            return await ctx.send(embed=discord.Embed(
                            description=f"{var.E_ERROR} You can only enter the volume value between 0 - 100, more than 100 would be too much :P", 
                            color=var.C_RED))

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(embed=discord.Embed(
                    description=f"{ctx.author} changed the volume to {vol}%", 
                    color=var.C_BLUE))

    @volume.error
    async def volume_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
                await ctx.send(embed=discord.Embed(
                    title="Bad Argument",
                    description=f"{var.E_ERROR} For volume you need to define only one value between 0 and 100.\n For example `{getprefix(ctx)}volume 50`",
                    color=var.C_RED
                )
                )


    @commands.command()
    async def leave(self, ctx):
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=discord.Embed(
                description="I'm not connected to a voice channel",
                color=var.C_ORANGE))

        else:
            await self.cleanup(ctx.guild)
            await ctx.send(embed=discord.Embed(
                            description=f"Successfully left the VC and cleared the queue",
                            color=var.C_GREEN
                ))


def setup(bot):
    bot.add_cog(Music(bot))