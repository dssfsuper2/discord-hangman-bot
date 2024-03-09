from discord import app_commands
import discord
from discord.ext import commands
import assets
import random
global errors, word, wlen, mask, guessed, wrong, game_active, wordlist
wordlist = []
with open('words.txt', 'r') as wlist:
    for thing in wlist.readlines():
        wordlist.append(thing.strip())
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
game_active = False
bot = commands.Bot(command_prefix='!', intents=intents)
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'synced {len(synced)} commands')
    except Exception as e:
        print(e)


@bot.tree.command(name="start")
async def hangman(interaction: discord.Interaction):
    global game_active
    global errors, word, wlen, mask, guessed, wrong
    if not game_active:
        errors = 0
        word = random.choice(wordlist)
        print(word)
        wlen = len(word)
        mask = "_"*wlen
        guessed = []
        wrong = []
        await interaction.response.send_message(f"The game started")
        await interaction.channel.send(mask.replace("_", '\_'))
        game_active = True
    else:
        await interaction.response.send_message(f"The game is already started")


@bot.tree.command(name="letter")
@app_commands.describe(letter="What is this letter?")
async def guess(interaction: discord.Interaction, letter: str):
    global game_active
    global errors, word, wlen, mask, guessed, wrong
    # the game was not started
    if not game_active:
        await interaction.response.send_message("a game is not started yet, you cannot guess")
    # the game was started
    else:
        # the guess is a letter
        if letter in alphabet:
            # the guess was already made
            if letter in guessed:
                # noinspection PyUnresolvedReferences
                await interaction.response.send_message("you already guessed this letter")
            # it is a new guess
            else:
                guessed.append(letter)
                # the guess is correct
                if letter in word:
                    w = list(word)
                    m = list(mask)
                    for i, it in enumerate(w):
                        if it == letter:
                            m[i] = letter
                    mask = "".join(m)
                    if list(mask).count("_") == 0:
                        await interaction.response.send_message(f"{mask}\nyou won")
                        game_active = False
                    await interaction.response.send_message("you got it right!")
                    w = list(word)
                    m = list(mask)
                    for i, das in enumerate(w):
                        if das == letter:
                            m[i] = letter
                    mask = "".join(m)

                else:
                    errors += 1
                    wrong.append(letter)
                    if errors > 5:
                        await interaction.response.send_message(f"you lost, the word was {word}")
                        game_active = False
                    else:
                        await interaction.response.send_message(f"you got it wrong")
        # the guess is not a letter
        else:
            await interaction.response.send_message("this is not a letter")
        if game_active:
            await interaction.channel.send(f'{mask.replace("_", "\_")}\nyou have committed {errors} errors\nyou have '
                                           f'guessed the letters: {" ".join(guessed)}\nand the following ones are '
                                           f'wrong: {" ".join(wrong)}')

# Run the bot with your token
bot.run(assets.TOKEN)
