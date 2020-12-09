import discord
import config
import gd
import math
import time
import sys
import err
from discord.ext import commands, tasks

#Loads config from config.yml
con = config.config
client = commands.Bot(command_prefix=con["prefix"])

# Global variables
EMBED = None
EMBED_MESSAGE = None
PREVIOUS_LEVEL = None
PREVIOUS_EMBED_MESSAGE = None

# DATA is a variable that stores the current data state of the game. It changes every time the bot updates. STATIC on
# the other hand, is only changed by the function when it needs to be, and holds data that should not be changed each
# update.
DATA = None
STATIC = {}

#Just some lists

#This one is for the difficulty icons
faces = ["https://cdn.discordapp.com/attachments/675532248493326359/785672432966828072/Auto.png","https://cdn.discordapp.com/attachments/675532248493326359/785672432139894794/Unrated.png","https://cdn.discordapp.com/attachments/675532248493326359/785672433948164116/Easy.png","https://cdn.discordapp.com/attachments/675532248493326359/785970124657000448/Normal.png","https://cdn.discordapp.com/attachments/675532248493326359/785672437227454474/Hard.png","https://cdn.discordapp.com/attachments/675532248493326359/785672438948167680/Harder.png","https://cdn.discordapp.com/attachments/675532248493326359/785672442789101588/Insane.png","https://cdn.discordapp.com/attachments/675532248493326359/785672436708016148/EasyDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672442508476426/MediumDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785973989495013416/Hard_Demon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672441879199764/InsaneDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672438746316840/ExtremeDemon.png"]

#This one tells the program where the image for the difficulty is in the last list
difficulties = [gd.LevelDifficulty.AUTO,gd.LevelDifficulty.NA,gd.LevelDifficulty.EASY,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.INSANE,gd.DemonDifficulty.EASY_DEMON,gd.DemonDifficulty.MEDIUM_DEMON,gd.DemonDifficulty.HARD_DEMON,gd.DemonDifficulty.INSANE_DEMON,gd.DemonDifficulty.EXTREME_DEMON]

#And this one just tells the game which of the main levels are of what difficulty, becaues gd.py doesn't do those.
main_levels = [gd.LevelDifficulty.EASY,gd.LevelDifficulty.EASY,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.HARDER,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.HARDER,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.INSANE]

# The loading bar states. The second I made this I actually just stopped and stared at it for a good two minutes. I'm not joking.
loading_bar = [
"░░░░░░░░░░░░░░░░░░░░",
"▓░░░░░░░░░░░░░░░░░░░",
"▓▓░░░░░░░░░░░░░░░░░░",
"▓▓▓░░░░░░░░░░░░░░░░░",
"▓▓▓▓░░░░░░░░░░░░░░░░",
"▓▓▓▓▓░░░░░░░░░░░░░░░",
"▓▓▓▓▓▓░░░░░░░░░░░░░░",
"▓▓▓▓▓▓▓░░░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓░░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"]

@client.event
async def on_ready():
    print(f"[Info] Bot logged in as {client.user}")

    # Starts the main bot thread
    main.start()

@client.command()
async def set_channel(ctx):
    """
    Sets which channel the bot should send its messages in.
    """
    global con
    new_channel = ctx.channel.id

    con["channel"] = new_channel
    config.update(con)

    await ctx.message.channel.send(f"✅ Set bot channel to {ctx.channel}")

@tasks.loop(seconds=2)
async def main():

    """
    The main loop of the program. Everything happens here. It executes every 2 seconds to update the embed.
    """

    # Bringing in all those globals
    global con, client
    global EMBED, EMBED_MESSAGE, PREVIOUS_LEVEL, PREVIOUS_EMBED_MESSAGE, DATA, STATIC
    global faces, difficulties, main_levels
    global loading_bar

    # Fetching the game memory
    memory = getMemory()

    try:
        if memory.is_in_level():

            # Fetch gamestate data
            DATA = getData()
            
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
                extra_text=" - LEVEL COMPLETE!"
            elif DATA["level_best"] > STATIC["old_best"]:
                extra_text = " - New Best!"
                STATIC["old_best"] = DATA["level_best"]
            else:
                extra_text = ""

            #Saving the best percent of the session
            if DATA["percent"] > STATIC["session_best"]:
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

            #Start creating embed
            EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

            EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])
            
            EMBED.add_field(name="Attempt:",value=DATA["current_attempts"],inline=True)
            EMBED.add_field(name="Best Percent:",value="{0}%".format(DATA["level_best"]),inline=True)
            EMBED.add_field(name="Current Progress:",value="{0}%{2}\n{1}".format(DATA["percent"],loading_bar[math.floor(DATA["percent"]/5)],extra_text),inline=False)
            EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))
            

            #Getting channel, and sending embed
            channel = client.get_channel(con["channel"])

            if channel is not None:
                
                #If the channel is found, edit the message the embed has been sent to, and if it dosent exist, create it.
                if EMBED_MESSAGE is None:
                    EMBED_MESSAGE = await channel.send(embed=EMBED)
                else:
                    await EMBED_MESSAGE.edit(embed=EMBED)

            else:

                err.softError("Channel not found")

        else:

            # Seals off the embed if a player goes to the menu, or exits the level
            if EMBED_MESSAGE is not None:
                
                title = "Played: {0}".format(DATA["level_name"])
                color = discord.Color.default()

                EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

                EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])

                EMBED.add_field(name="Attempts:",value=DATA["current_attempts"],inline=True)
                EMBED.add_field(name="Total Attempts:",value=DATA["total_attempts"],inline=True)
                EMBED.add_field(name="Total Jumps:",value=DATA["jumps"],inline=True)
                EMBED.add_field(name="Best Session Percent:",value="{0}%\n{1}".format(STATIC["session_best"],loading_bar[math.floor(STATIC["session_best"]/5)]),inline=False)
                EMBED.add_field(name="Best Percent:",value="{0}%\n{1}".format(DATA["level_best"],loading_bar[math.floor(DATA["level_best"]/5)]),inline=False)
                EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))

                await EMBED_MESSAGE.edit(embed=EMBED)

                #Sets some globals so that the embed can be reused if the same level is played again
                PREVIOUS_EMBED_MESSAGE = EMBED_MESSAGE
                EMBED_MESSAGE = None

    except Exception as e:
        err.softError(e)

def getData():
    """
    Fetches gamestate data from memory and returns it
    """    
    memory = getMemory()

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

def getMemory():
    """
    Fetches game memory
    """
    try:
        memory = gd.memory.get_memory()
        return memory
    except:
        err.fatalError("GD not detected")

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