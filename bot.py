# Circa ~2023

import discord
import discord.ext
from discord.ext import commands
from dotenv import load_dotenv
from discord import app_commands

import os, random, json

gameInstances = {
    'hangman': {},
    'trivia': {},
}

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

class hangmanGame:
    def __init__(self):
        self.isHangman = False
        self.hangmanWord = ""
        self.guessedLetters = []
        self.wrongGuessedLetters = []
        self.isHangman = False
        self.hangmanValue = 0

global isTrivia, triviaList, triviaListAnswers, triviaValue

triviaValue = 0
isTrivia = False
triviaList = [
              "Manually aligning a bullet in a revolver wheel is called...",
              "How many languages are written from right to left?",
              ]
triviaListAnswers = ["Cocking the hammer", "12"]

global isPhrases, phrasesWord, fullPhrase
isPhrases = False

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='~', activity=discord.Game(name="prefix ~"), intents=intents)

from generalCommands import genCommandsSetup
from musicCommands import musicCommandsSetup
from funCommands import funCommandsSetup
from currencyCommands import currencyCommandsSetup

async def main():
    await genCommandsSetup(client)
    await musicCommandsSetup(client)
    await funCommandsSetup(client)
    await currencyCommandsSetup(client)

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

@client.event
async def on_ready():
    print(f'{client.user.name} ready')

# todo: GAME COMMANDS

@client.command(name='phrases', help='Begin a phrase game (231 proverbs)')
async def phrases(ctx):
    global phrasesWord
    global fullPhrase
    global isPhrases

    with open('lists/proverbs.txt', 'r') as f:
        phrasesList = f.read().split('\n')
    f.close()

    if isPhrases:
        await ctx.send("Repeating phrase:"
                       f"\n{fullPhrase}")
    else:
        selectedPhrase = phrasesList[random.randint(0, len(phrasesList))]
        selectedPhrase = selectedPhrase[:-1]

        fullPhrase = selectedPhrase
        censoredWord = ""

        splitPhrase = selectedPhrase.split()  # this is a list of the words in the phrase

        looping = True
        while looping:
            randVal = random.randint(0, len(splitPhrase)-1)
            if len(splitPhrase[randVal]) > 3:
                censoredWord = splitPhrase[randVal]
                looping = False
                f.close()
            else:
                continue

        print(censoredWord)
        phrasesWord = censoredWord

        underscores = "_ "*len(censoredWord)

        finalStr = fullPhrase.replace(censoredWord, underscores[:-1])

        isPhrases = True
        await ctx.send(f"**Phrase game begun!** \nYour phrase is: `{finalStr}`")

@client.command(name='endphrases', help='ends phrase game')
async def endPhrases(ctx):
    global isPhrases
    global fullPhrase

    if isPhrases:
        await ctx.send(f"Game ended. The phrase was **{fullPhrase}**")
        isPhrases = False
    else:
        await ctx.send("You aren't playing a phrase game!")

@client.command(name='hangman', help='begins a game of hangman')
async def hangman(ctx, mode=None):
    serverId = ctx.guild.id

    if serverId not in gameInstances['hangman']:
        gameInstances['hangman'][serverId] = hangmanGame()

    gameInstance = gameInstances['hangman'][serverId]

    if mode == "normal":
        f = open('lists/5000words.txt', 'r')
    elif mode == 'hard':
        f = open('lists/words_alpha.txt', 'r')
        gameInstance.hangmanIsHard = True
    else:
        await ctx.send("No mode specified, normal selected (Modes: normal and hard)")
        f = open('lists/5000words.txt', 'r')

    contents = f.read()
    wordsList = contents.split()

    underscores = ""

    gameInstance.guessedLetters.clear()

    if gameInstance.isHangman:
        await ctx.send("You're already playing a hangman game!")
    else:
        gameInstance.hangmanIsHard = False
        looping = True
        while looping:
            randVal = random.randint(0, len(wordsList)-1)
            if (len(wordsList[randVal]) > 4):
                f.close()

                for i in range(len(wordsList[randVal])):  # making the underscores
                    underscores += "_ "

                await ctx.send(f"**Hangman game started!** \nYour word is: `{underscores[:-1]}`")
                await ctx.send(hangmanImage(0))
                gameInstance.hangmanWord = wordsList[randVal]
                print("CHEAT for CHEATERS:", gameInstance.hangmanWord)

                gameInstance.isHangman = True
                looping = False
            else:
                continue

@client.command(name='endhangman', help='Ends a game of hangman ')
async def endHangman(ctx):
    serverId = ctx.guild.id
    gameInstance = gameInstances['hangman'][serverId]

    if gameInstance.isHangman:
        await ctx.send(f"Hangman ended! The word was **{gameInstance.hangmanWord}**")
        gameInstances['hangman'].pop(serverId, None)
    else:
        await ctx.send("You aren't playing hangman.")

def hangmanImage(currentValue):
    hangmanImage = ["""```◤ --
|   |
|
|
|
┴-```""", """```◤ --
|   |
|   ◯
|
|
┴-```""", """```◤ --
|   |
|   ◯
|  /
|
┴-```""","""```◤ --
|   |
|   ◯
|  /|
|
┴-```""","""```◤ --
|   |
|   ◯
|  /|\\
|
┴-```""","""```◤ --
|   |
|   ◯
|  /|\\
|  /
┴-```""","""```◤ --
|   |
|   ◯
|  /|\\
|  / \\
┴-```""",]

    return hangmanImage[currentValue]

def updateHangman(serverId, letterGuess):
    print("Guess:", letterGuess)
    gameInstance = gameInstances['hangman'][serverId]

    letterGuess = letterGuess.lower()
    guessIsRight = False
    wordIsGuessed = False
    returnStr = ""

    for letter in gameInstance.hangmanWord:
        letterNotGuessedYet = True
        for guessedLetter in gameInstance.guessedLetters:
            if guessedLetter == letter:
                letterNotGuessedYet = False
                returnStr += str(letter) + " "
                break

        if letterGuess == letter and letterNotGuessedYet:
            guessIsRight = True
            returnStr += str(letter) + " "
            if letterGuess not in gameInstance.guessedLetters:
                gameInstance.guessedLetters.append(letterGuess)

        elif letterNotGuessedYet:
            returnStr += "_ "
            continue

    if "_" not in returnStr and len(returnStr) > 0:
        wordIsGuessed = True
        gameInstance.guessedLetters.clear()
        gameInstance.wrongGuessedLetters.clear()

    return returnStr[:-1], guessIsRight, wordIsGuessed

@client.command(name='trivia', help=f'Currently has {len(triviaList)} questions')
async def trivia(ctx):
    global isTrivia
    global triviaValue
    global triviaList

    if isTrivia:
        await ctx.send(f"You're already playing a trivia game.")
    else:
        triviaValue = random.randint(0, len(triviaList))
        isTrivia = True
        await ctx.send(triviaList[triviaValue])

@client.command(name = 'endtrivia', help='Ends trivia if active')
async def endTrivia(ctx):
    global isTrivia
    if isTrivia:
        isTrivia = False
        await ctx.send("Trivia ended.")
    else:
        await ctx.send("You're not playing a trivia game.")

# todo: EXECUTION

triggerPhrasesList = [
    ['rizz', "<:datme:1091548579170107412>"],
]

@client.event  # includes games
async def on_message(message):
    serverId = message.guild.id if message.guild is not None else None
    userId = str(message.author.id)
    points = pointsData.get(userId, 0)

    if isinstance(message.channel, discord.DMChannel):  # store dms
        recievedChannel = client.get_channel(1159937322771546163)
        sentChannel = client.get_channel(1159938920063184957)

        if message.author.id == 902742925606260818:  # send messages by itself
            await sentChannel.send(f"**{message.author}**: {message.content}")
        else:
            await recievedChannel.send(f"**<@{message.author.id}>** ({message.author.id}): {message.content}")
            if message.attachments:  # send images as well
                for i in len(message.attachments):
                    await recievedChannel.send(f"**{message.author}** (image): {message.attachments[i].url}")

    global isTrivia, triviaList, triviaListAnswers, triviaValue
    global phrasesWord, fullPhrase, isPhrases

    if client.user.id != message.author.id:
        if 'hangman' in gameInstances and serverId in gameInstances['hangman']:
            hmGameInst = gameInstances['hangman'][serverId]

            if hmGameInst.isHangman:
                hangmanWinPoints = 30

                if len(message.content) == 1 and message.content.lower()[0].isalpha():
                    result = updateHangman(serverId, message.content)

                    if result[1] == False and message.content.lower() not in hmGameInst.wrongGuessedLetters:
                        await message.channel.send("Wrong guess!")
                        hmGameInst.wrongGuessedLetters.append(message.content.lower())
                        hmGameInst.hangmanValue += 1
                    elif message.content.lower() in hmGameInst.wrongGuessedLetters:
                        await message.channel.send("You already guessed that letter.")

                    await message.channel.send(hangmanImage(hmGameInst.hangmanValue))  # print image
                    await message.channel.send(f"`{result[0]}`")  # print the current word progress

                    wrongLetters = ""
                    for letter in hmGameInst.wrongGuessedLetters:
                        wrongLetters += letter + ", "
                    await message.channel.send(f"Current wrong letters: {wrongLetters}")

                    if result[2]:
                        points += hangmanWinPoints
                        await message.channel.send(f"# {message.author.name} WINS!! The word was **{hmGameInst.hangmanWord}**! "
                                                   f"${hangmanWinPoints} gained! (Current: ${points:,})")
                        gameInstances['hangman'].pop(serverId, None)  # ends game

                    elif hmGameInst.hangmanValue > 5:
                        await message.channel.send(f"# You LOSE! The word was **{hmGameInst.hangmanWord}**")
                        gameInstances['hangman'].pop(serverId, None)  # ends game

                elif message.content.lower() == hmGameInst.hangmanWord:
                    points += hangmanWinPoints
                    await message.channel.send(f"# {message.author.name} WINS!! The word was **{hmGameInst.hangmanWord}**! "
                                               f"${hangmanWinPoints} gained! (Current: ${points:,})")
                    gameInstances['hangman'].pop(serverId, None)  # ends game

        if isTrivia:
            triviaWinPoints = 15
            if (triviaListAnswers[triviaValue] == message.content.lower()):  # trivia game
                ques = triviaList[triviaValue]
                ans = triviaListAnswers[triviaValue]
                isTrivia = False
                points += triviaWinPoints
                await message.channel.send(f"Correct, the answer to **{ques}** is **{ans}**!"
                                           f"**{message.author.name}** you win {triviaWinPoints}$! (current: ${points:,})")

        if isPhrases:
            phrasesWinPoints = 20
            if (phrasesWord.lower() == message.content.lower()):
                points += phrasesWinPoints
                await message.channel.send(f"Correct, **{message.author.name}**! The full saying goes: **{fullPhrase}**. "
                                           f"You win {phrasesWinPoints}$! (Current: ${points:,})")
                isPhrases = False

        else:   # auto responses
            for phrase in triggerPhrasesList:
                if phrase[0] in message.content.lower():
                    await message.channel.send(phrase[1])

    if isPhrases or isTrivia or (serverId in gameInstances['hangman']):  # if there's a game happening, don't update points
        pointsData[userId] = points
        savePointsData()

    await client.process_commands(message)

client.run(TOKEN)