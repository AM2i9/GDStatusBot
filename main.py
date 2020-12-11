import discord
import config
import gd
import math
import time
import sys
import err
import random
from lists import *
from main_levels import *
from discord.ext import commands, tasks

#Loads config from config.yml
con = config.config

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=con["prefix"],intents=intents)
# Global variables
EMBED_MESSAGE = None
PREVIOUS_LEVEL = None
PREVIOUS_EMBED_MESSAGE = None

# DATA is a variable that stores the current data state of the game. It changes every time the bot updates. STATIC on
# the other hand, is only changed by the function when it needs to be, and holds data that should not be changed each
# update.
DATA = None
STATIC = {}

@client.event
async def on_ready():
    print(f"[Info] Bot logged in as {client.user}")

    if not con["user"]:
        await getUser()

    # Starts the main bot thread
    main.start()

@client.command()
async def set_channel(ctx):
    """
    Sets which channel the bot should send its messages in.
    """
    global con
    if ctx.message.author.id != con["user"]:
        return


    new_channel = ctx.channel.id

    con["channel"] = new_channel
    config.update(con)

    await ctx.message.channel.send(f"✅ Set bot channel for {ctx.message.author} to #{ctx.channel}")

@tasks.loop(seconds=2)
async def main():

    """
    The main loop of the program. Everything happens here. It executes every 2 seconds to update the embed.
    """

    # Bringing in all those globals
    global con, client
    global EMBED_MESSAGE, PREVIOUS_LEVEL, PREVIOUS_EMBED_MESSAGE, DATA, STATIC

    # Fetching the game memory
    memory = await getMemory()

    try:
        if memory.is_in_level():

            if memory.get_level_id() != PREVIOUS_LEVEL:
                await sealEmbed()

            # Fetch gamestate data
            DATA = await getData()
            
            # Gets wether or not the level being played is the exact same level that was played just previously, so that it will continue to use the same embed
            if PREVIOUS_LEVEL != DATA["level_id"]:
                EMBED_MESSAGE = None
                PREVIOUS_EMBED_MESSAGE = None
                STATIC["start_attempts"] = DATA["total_attempts"]
                STATIC["old_best"] = DATA["level_best"]
                STATIC["session_best"] = 0
            else:
                if PREVIOUS_EMBED_MESSAGE is not None:
                    EMBED_MESSAGE = PREVIOUS_EMBED_MESSAGE

            PREVIOUS_LEVEL = DATA["level_id"]

            # So for some reason, the main levels all have their creator blank, so we just set it to RobTop
            if DATA["level_creator"] == "":
                DATA["level_creator"] = "RobTop"

            # Getting if you are playing a main level or not. If so, we have to manually set the difficulty using the list I made earlier
            if DATA["level_id"] in range(1,22):
                
                DATA["difficulty"] = main_levels[DATA["level_id"]-1]

            #Checks if the player is in practice mode or not. If they are, it will display differently
            if DATA["practice_mode"]:
                title = "Practicing: {0}".format(DATA["level_name"])
                color = discord.Color.from_rgb(59, 223, 245)
            else:
                title = "Playing: {0}".format(DATA["level_name"])
                color = discord.Color.from_rgb(18, 219, 31)

            #A few little extra texts
            if DATA["percent"] == 100:
                if DATA["practice_mode"]:
                    extra_text=" - PRACTICE COMPLETE!"
                else:
                    extra_text=" - LEVEL COMPLETE!"
                    color = discord.Color.from_rgb(237, 220, 28)

            elif DATA["level_best"] > STATIC["old_best"]:
                extra_text = " - New Best!"
                STATIC["old_best"] = DATA["level_best"]
            else:
                extra_text = ""

            #Saving the best percent of the session
            if DATA["percent"] > STATIC["session_best"] and not DATA["practice_mode"]:
                STATIC["session_best"] = DATA["percent"]

            #Getting the star rating of the level, if there is any
            if DATA["star_rating"]:
                STATIC["rating"] = " | {}⭐".format(DATA["star_rating"])
            else:
                STATIC["rating"] = ""

            # Checking if the level is featured
            if DATA["featured"]:
                STATIC["epic_featured"] = "   |   Featured 👀"
            else:
                STATIC["epic_featured"] = ""

            #Checking if the level is Epic. If it is epic, it will override the Featured.
            if DATA["epic"]:
                STATIC["epic_featured"] = "   |   Epic 🔥"

            #Calculating the current attempts on a level
            DATA["current_attempts"] = (DATA["total_attempts"] - STATIC["start_attempts"]) + 1

            #Getting channel
            channel = client.get_channel(con["channel"])

            #Start creating embed
            EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

            EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])

            #Getting user
            user = client.get_user(con['user'])

            EMBED.set_author(name=user.display_name,icon_url=user.avatar_url)
            EMBED.add_field(name="Attempt:",value=DATA["current_attempts"],inline=True)
            EMBED.add_field(name="Best %:",value="{0}%".format(DATA["level_best"]),inline=True)
            EMBED.add_field(name="Current Progress:",value="{0}%{2}\n{1}".format(DATA["percent"],progress_bar[math.floor(DATA["percent"]/5)],extra_text),inline=False)
            EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))
            

            #sending embed

            if channel is not None:
                
                #If the channel is found, edit the message the embed has been sent to, and if it dosent exist, create it.
                if EMBED_MESSAGE is None:
                    EMBED_MESSAGE = await channel.send(embed=EMBED)
                else:
                    await EMBED_MESSAGE.edit(embed=EMBED)

            else:

                err.softError("Channel not found")

        else:

                await sealEmbed()
                #Sets some globals so that the embed can be reused if the same level is played again
                PREVIOUS_EMBED_MESSAGE = EMBED_MESSAGE
                EMBED_MESSAGE = None

    except Exception as e:
        err.softError(e)

async def sealEmbed():
    """
    Seals off the embed if a player goes to the menu, or exits the level
    """       
    global EMBED_MESSAGE
    global DATA, STATIC
    global progress_bar

    if EMBED_MESSAGE is not None:
                
        title = "Played: {0}".format(DATA["level_name"])
        color = discord.Color.default()

        EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

        EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])

        #Getting user
        user = client.get_user(con['user'])

        EMBED.set_author(name=user.display_name,icon_url=user.avatar_url)

        EMBED.add_field(name="Attempts:",value=DATA["current_attempts"],inline=True)
        EMBED.add_field(name="Total Attempts:",value=DATA["total_attempts"],inline=True)
        EMBED.add_field(name="Total Jumps:",value=DATA["jumps"],inline=True)
        EMBED.add_field(name="Best Session %:",value="{0}%\n{1}".format(STATIC["session_best"],progress_bar[math.floor(STATIC["session_best"]/5)]),inline=False)
        EMBED.add_field(name="Best Lifetime %:",value="{0}%\n{1}".format(DATA["level_best"],progress_bar[math.floor(DATA["level_best"]/5)]),inline=False)
        EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))

        await EMBED_MESSAGE.edit(embed=EMBED)

async def getData():
    """
    Fetches gamestate data from memory and returns it
    """    
    memory = await getMemory()

    level_name = memory.get_level_name()
    level_creator = memory.get_level_creator()
    level_id = memory.get_level_id()

    practice_mode = memory.is_practice_mode()

    attempts = memory.get_attempts()
    jumps = memory.get_jumps()
    difficulty = memory.get_level_difficulty()

    percent = math.floor(memory.get_percent())
    level_best = math.floor(memory.get_normal_percent())

    practice_best = math.floor(memory.get_practice_percent())

    star_rating = memory.get_level_stars()
    featured = memory.is_level_featured()
    epic = memory.is_level_epic()

    data = {"level_name":level_name,"level_creator":level_creator,"level_id":level_id,"practice_mode":practice_mode,"total_attempts":attempts,"current_attempts":None,"jumps":jumps,"difficulty":difficulty,"percent":percent,"level_best":level_best,"practice_best":practice_best,"star_rating":star_rating,"featured":featured,"epic":epic}

    return data

async def getMemory():
    """
    Fetches game memory
    """
    try:
        memory = gd.memory.get_memory()
        return memory
    except:
        await sealEmbed()
        err.fatalError("GD not detected")

async def getUser():
    """
    Allows the user to link their discord account to the bot through their user id
    """
    global con

    def checkIfDm(message: discord.Message):

        if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
            return True
        else:
            return False

    token = ''.join(str(random.randint(1,10)) for i in range(7))

    print("[Info] To link your discord account to the bot, open a new direct message with the bot and send it the following code: {}".format(token))

    while True:

        message = await client.wait_for('message',check=checkIfDm)

        if message.content == token:
            
            await message.channel.send("Linking account...")
            print("[Info] Token recieved, linking account")

            con['user'] = message.author.id
            config.update(con)

            await message.channel.send("Account Linked")
            print('[Info] Account linked.')
            break

        else:

            print(["[Info] That is not the correct token, please send the correct token printed previously"])
        

# Starting the bot
print("[Info] Waiting for GD...")
# Keeps waiting for GD to open before it launches the bot
while True:
    try:
        gd.memory.get_memory()
    except:
        pass
    else:
        print("[Info] GD Detected. Starting bot...")
        break

#Launching the bot
try:
    client.run(con["token"])
except discord.errors.LoginFailure:
    err.fatalError("Invalid token. Please put a valid discord bot token in config.yml")