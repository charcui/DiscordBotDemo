import discord
from discord.ext import commands
from datetime import datetime
import random

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rand'], help='Lists a random number from 1 to specified (Default 1-10)')
    async def random(self, ctx, number = None):
        if number == None:
            maxVal = 10
        else:
            maxVal = int(number)

        if int(number) == 1:
            await ctx.send("Seriously")
        else:
            await ctx.send(f"From 1 to {maxVal}, your number is **{random.randint(1, maxVal)}**")

    @commands.command(name='parrot', help='Repeats after')
    async def parrot(self, ctx):
        await ctx.message.delete()
        await ctx.send(ctx.message.content[8:])

    @commands.command(name='serverinfo', help="Displays information about the server")
    async def server(self, ctx):
        if ctx.guild:
            for member in ctx.guild.members:
                if member.id == ctx.guild.owner.id:  # does not work if the owner ever changes
                    joinDateStr = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
                    joinDate = datetime.strptime(joinDateStr, "%Y-%m-%d %H:%M:%S")
                    currentDate = datetime.now()
                    timeDifference = currentDate - joinDate

            name = str({ctx.message.guild.name})
            name = name[2:len(name)-2]
            icon_url = ctx.guild.icon.url

            embed = discord.Embed(title=name, url=None,
                                  description= f"This server was created on {joinDateStr}",
                                  color=0x6BEEF8)

            embed.add_field(name="Server age", value=str(f'{timeDifference.days//365} years, {timeDifference.days%365} days'), inline=False)
            embed.add_field(name="Owner", value=str(ctx.guild.owner.name), inline=True)

            allMemberCount = len(ctx.guild.members)
            trueMemberCount = len([m for m in ctx.guild.members if not m.bot])

            embed.add_field(name="Member count", value=f"{trueMemberCount} people, {allMemberCount - trueMemberCount} bots", inline=True)
            embed.set_footer(text=f'Current time: {currentDate}')
            embed.set_image(url=icon_url)

            await ctx.send(embed=embed)

    @commands.command(name='dm', help="Sends a DM to someone with a message (ID only, recipient must be in a sever with the "
                                    "bot, bot must be online to read DMs)")
    async def dm(self, ctx, target_user: discord.User = None, *, message: str = None):
        if target_user is None or message is None:
            await ctx.send("Format it like this: `dm [userID (turn on dev mode to get)] [message]`")
            return

        try:
            await target_user.send(message)
            await ctx.send(f"I sent a DM to {target_user.mention}!")
        except discord.Forbidden:
            await ctx.send(f"I can't DM {target_user.mention}. I probably dont share a server with them.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def genCommandsSetup(bot):
    await bot.add_cog(general(bot))