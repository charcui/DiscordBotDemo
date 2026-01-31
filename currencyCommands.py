import discord
from discord.ext import commands
import random
import json

shopInstances = {}

def loadPointsData():  # LOADING POINTS JSON
    try:
        with open('lists/pointsData.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": {}}

pointsData = loadPointsData()

def savePointsData():
    try:
        with open('lists/pointsData.json', 'w') as file:
            json.dump(pointsData, file, indent=4)
    except Exception as e:
        print(f"Error saving points data: {e}")

def roundToZero(n):
    result = 0 if n < 0 else n
    return result

class currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['bal'], help='Checks balance')
    async def balance(self, ctx, targetUser: discord.User = None):
        if targetUser is None:
            userId = str(ctx.author.id)
            messageRecipient = ctx.author
        else:
            userId = str(targetUser.id)
            messageRecipient = targetUser

        points = pointsData.get(userId, 0)

        if points < 0:
            points = 0
            pointsData[userId] = points
            savePointsData()

        if points == 0:
            await ctx.send(f'{messageRecipient.mention} has ${points}, and is poor.')
        else:
            await ctx.send(f"{messageRecipient.mention} has ${points:,}, and is rich.")

    @commands.command(name='bet', help='Gamble! Must be over $20')
    async def bet(self, ctx, input=None):
        userId = str(ctx.author.id)
        points = pointsData.get(userId, 0)

        randVal = random.randint(0, 100)
        earned = 0
        returnMsg = ""

        if input == None:
            await ctx.send("Type a number over 20. ")

        input = int(input)
        if points == 0:
            await ctx.send(f"You only have $0.")
        elif points <= 20:
            await ctx.send(f"You dont even have $20... (Current balance ${points:,})")
        elif input > points:
            await ctx.send(f"You only have ${points:,}.")

        else:
            input = int(input)

            if (type(input) != int):
                print("ERROR: input isnt a num")

            if (input<20):
                await ctx.send("You must put more than than 20$ on the line.")

            else:
                if (randVal > 99):
                    earned = input*(random.randint(10, 20))
                    returnMsg = f'{ctx.author.mention} broke the machines, and now they\'re spitting out cash, ' \
                                f'earning ${earned:,} ! (New total ${(points+earned):,})'

                elif (randVal > 95):
                    earned = input*(random.randint(3, 8))
                    returnMsg = f'{ctx.author.mention} won huge: ${earned:,}! (New total ${(points+earned):,})'

                elif (randVal > 65):
                    earned = input*(random.randint(2, 4))
                    returnMsg = f'CHA CHING! {ctx.author.mention} just WON ${earned:,}! (new total ${(points+earned):,})'

                elif (randVal > 12):
                    earned = input*-(random.randint(2, 3))
                    returnMsg = f'Unlucky! {ctx.author.mention} just lost ${abs(earned):,} (New total ${roundToZero(points+earned):,})'

                else:
                    earned = input*-(random.randint(3, 7))
                    returnMsg = f'Uh oh... {ctx.author.mention} is so bad that the casino kicked them out and sued.' \
                                f'You lost ${abs(earned):,} (New total ${roundToZero(points+earned):,})'

            points += earned

            points = 0 if points < 0 else points

            pointsData[userId] = points
            savePointsData()  # saves the data after adding to it

            await ctx.send(returnMsg)

async def currencyCommandsSetup(bot):
    await bot.add_cog(currency(bot))