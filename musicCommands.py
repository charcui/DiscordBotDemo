import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

queues = {}

def play_next(guild_id, voice):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn'}
    queue = queues.get(guild_id, [])
    if queue:
        song_url = queue.pop(0)
        queues[guild_id] = queue
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(song_url, download=False)
        URL = info['url']
        voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(guild_id, voice))

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join', help='Joins VC', pass_context=True)
    async def joinVoice(self, ctx):
        if (ctx.author.voice):
            if ctx.author.id == 349777907918569473:
                await ctx.send("ok paw omw")
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You're not in a voice chat.")

    @commands.command(name='leave', help='Leaves VC', pass_context=True)
    async def leaveVoice(self, ctx):
        if (ctx.voice_client):
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("I'm not in a voice chat.")

    @commands.command(name='skip', help='Skips song')
    async def skip(self, ctx):
        voice = ctx.voice_client
        if voice and voice.is_playing():
            await ctx.send("Song skipped!")
            voice.stop()
        else:
            await ctx.send("No song is playing.")

    @commands.command(aliases=['p'], help='Plays a YouTube link (also works with p)')
    async def play(self, ctx, *args):
        url = " ".join(args)
        YDL_OPTIONS = {'format': 'bestaudio',
                       'noplaylist': 'True',
                       'default_search': 'ytsearch'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        voice = ctx.voice_client

        if not ctx.author.voice:
            await ctx.send("You're not in a voice chat!")
            return

        if not voice:
            voice_channel = ctx.author.voice.channel
            voice = await voice_channel.connect()

        if voice.is_playing() or voice.is_paused():
            queue = queues.get(ctx.guild.id, [])
            queue.append(url)
            queues[ctx.guild.id] = queue
            await ctx.send("Song queued!")

        else:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                YDL_OPTIONS['download'] = False
                info = ydl.extract_info(url, download=False)

                if 'entries' in info:
                    URL = info['entries'][0]['url']
                else:
                    URL = info['url']

            voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx.guild.id, voice))

    @commands.command(aliases=['q'], help='Shows the queue of songs (also works with q)')
    async def queue(self, ctx):
        queue = queues.get(ctx.guild.id, [])
        if queue:
            await ctx.send("Songs cued:")
            for i, url in enumerate(queue, start=1):
                await ctx.send(f"{i}. {url}")
        else:
            await ctx.send("No songs queued!")

    @commands.command(name='clear', help='Clears queue')
    async def clearQueue(self, ctx):
        if ctx.guild.id in queues:
            queues[ctx.guild.id] = []
            await ctx.send("Queue cleared.")
        else:
            await ctx.send("Nothing to clear!")

async def musicCommandsSetup(bot):
    await bot.add_cog(music(bot))