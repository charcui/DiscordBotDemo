from discord.ext import commands
import random

class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='word', help='Returns a word starting with that letter')
    async def word(self, ctx, letter):
        f = open('lists/words_alpha.txt', 'r')
        contents = f.read()
        wordsList = contents.split()

        looping = True
        while looping:
            randVal = random.randint(0, len(wordsList))
            if (wordsList[randVal][0] == letter):
                await ctx.send(wordsList[randVal])
                looping = False
                f.close()
            else:
                continue

    @commands.command(name='w', help='Returns a word containing the letter combo')
    async def wordCombo(self, ctx, letters):
        f = open('lists/words_alpha.txt', 'r')
        contents = f.read()
        wordsList = contents.split()

        looping = True
        while looping:
            randVal = random.randint(0, len(wordsList))
            if (letters in wordsList[randVal]):
                await ctx.send(wordsList[randVal])
                looping = False
                f.close()
            else:
                continue

async def funCommandsSetup(bot):
    await bot.add_cog(fun(bot))