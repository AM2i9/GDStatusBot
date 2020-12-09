import discord
import config
import gd
import math
import time
import sys
from discord.ext import commands, tasks

con = config.config
client = commands.Bot(command_prefix=con["prefix"])

EMBED = None
EMBED_MESSAGE = None
PREVIOUS_LEVEL = None
PREVIOUS_EMBED_MESSAGE = None
DATA = None
STATIC = {}

faces = ["https://cdn.discordapp.com/attachments/675532248493326359/785672432966828072/Auto.png","https://cdn.discordapp.com/attachments/675532248493326359/785672432139894794/Unrated.png","https://cdn.discordapp.com/attachments/675532248493326359/785672433948164116/Easy.png","https://cdn.discordapp.com/attachments/675532248493326359/785970124657000448/Normal.png","https://cdn.discordapp.com/attachments/675532248493326359/785672437227454474/Hard.png","https://cdn.discordapp.com/attachments/675532248493326359/785672438948167680/Harder.png","https://cdn.discordapp.com/attachments/675532248493326359/785672442789101588/Insane.png","https://cdn.discordapp.com/attachments/675532248493326359/785672436708016148/EasyDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672442508476426/MediumDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785973989495013416/Hard_Demon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672441879199764/InsaneDemon.png","https://cdn.discordapp.com/attachments/675532248493326359/785672438746316840/ExtremeDemon.png"]
difficulties = [gd.LevelDifficulty.AUTO,gd.LevelDifficulty.NA,gd.LevelDifficulty.EASY,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.INSANE,gd.DemonDifficulty.EASY_DEMON,gd.DemonDifficulty.MEDIUM_DEMON,gd.DemonDifficulty.HARD_DEMON,gd.DemonDifficulty.INSANE_DEMON,gd.DemonDifficulty.EXTREME_DEMON]
main_levels = [gd.LevelDifficulty.EASY,gd.LevelDifficulty.EASY,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.NORMAL,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARD,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.HARDER,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.INSANE,gd.LevelDifficulty.HARDER,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.HARDER,gd.DemonDifficulty.HARD_DEMON,gd.LevelDifficulty.INSANE]

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
    print(f"Bot logged in as {client.user}")
    main.start()


@client.command()
async def set_channel(ctx):
    global con
    new_channel = ctx.channel.id

    con["channel"] = new_channel
    config.update(con)

    await ctx.message.channel.send(f"✔️Set bot channel to {ctx.channel}")

@tasks.loop(seconds=2)
async def main():

    global con, client
    global EMBED, EMBED_MESSAGE, PREVIOUS_LEVEL, PREVIOUS_EMBED_MESSAGE, DATA, STATIC
    global faces, difficulties, main_levels
    global loading_bar

    memory = None

    try:
        memory = gd.memory.get_memory()
    except RuntimeError:
        print("GD Not detected. Exiting...")
        time.sleep(5)
        sys.exit("Geometry Dash not running.")

    try:
        if memory.is_in_level():

            DATA = getData()
            
            if PREVIOUS_LEVEL != DATA["level_id"]:
                EMBED_MESSAGE = None
                PREVIOUS_EMBED_MESSAGE = None
                STATIC["start_attempts"] = DATA["total_attempts"]
                STATIC["old_best"] = DATA["level_best"]
            else:
                if PREVIOUS_EMBED_MESSAGE is not None:
                    EMBED_MESSAGE = PREVIOUS_EMBED_MESSAGE

            PREVIOUS_LEVEL = DATA["level_id"]

            if DATA["level_creator"] == "":
                DATA["level_creator"] = "RobTop"

            if DATA["level_id"] in range(1,22):
                
                DATA["difficulty"] = main_levels[DATA["level_id"]-1]

            if DATA["practice_mode"]:
                title = "Practicing: {0}".format(DATA["level_name"])
                color = discord.Color.from_rgb(59, 223, 245)
            else:
                title = "Playing: {0}".format(DATA["level_name"])
                color = discord.Color.from_rgb(18, 219, 31)

            if DATA["level_best"] > STATIC["old_best"]:
                if DATA["level_best"] == 100:
                    extra_text=" - LEVEL COMPLETE!"
                else:
                    extra_text = " - New Best!"
                STATIC["old_best"] = DATA["level_best"]
            else:
                extra_text = ""

            if DATA["star_rating"]:
                STATIC["rating"] = " | {}⭐".format(DATA["star_rating"])
            else:
                STATIC["rating"] = ""

            if DATA["featured"]:
                STATIC["epic_featured"] = "   |   Featured 👀"
            else:
                STATIC["epic_featured"] = ""

            if DATA["epic"]:
                STATIC["epic_featured"] = "   |   Epic 🔥"

            DATA["current_attempts"] = (DATA["total_attempts"] - STATIC["start_attempts"]) + 1

            EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

            EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])
            
            EMBED.add_field(name="Attempts:",value=DATA["current_attempts"],inline=True)
            EMBED.add_field(name="Best Percent:",value="{0}%".format(DATA["level_best"]),inline=True)
            EMBED.add_field(name="Current Progress:",value="{0}%{2}\n{1}".format(DATA["percent"],loading_bar[math.floor(DATA["percent"]/5)],extra_text),inline=False)
            EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))

            channel = client.get_channel(con["channel"])

            if channel is not None:

                if EMBED_MESSAGE is None:
                    EMBED_MESSAGE = await channel.send(embed=EMBED)
                else:
                    await EMBED_MESSAGE.edit(embed=EMBED)

        else:

            if EMBED_MESSAGE is not None:

                title = "Played: {0}".format(DATA["level_name"])
                color = discord.Color.default()

                EMBED = discord.Embed(type="rich",title=title,description="By {0}{1}{2}".format(DATA["level_creator"], STATIC["rating"], STATIC["epic_featured"]),color=color)

                EMBED.set_thumbnail(url=faces[difficulties.index(DATA["difficulty"])])

                EMBED.add_field(name="Attempts:",value=DATA["current_attempts"],inline=True)
                EMBED.add_field(name="Total Attempts:",value=DATA["total_attempts"],inline=True)
                EMBED.add_field(name="Total Jumps:",value=DATA["jumps"],inline=True)
                EMBED.add_field(name="Best Percent:",value="{0}%\n{1}".format(DATA["level_best"],loading_bar[math.floor(DATA["level_best"]/5)]),inline=False)
                EMBED.add_field(name="Best Practice Percent:",value="{0}%\n{1}".format(DATA["practice_best"],loading_bar[math.floor(DATA["practice_best"]/5)]),inline=False)
                EMBED.set_footer(text="Level ID: {0}".format(DATA["level_id"]))

                await EMBED_MESSAGE.edit(embed=EMBED)

                PREVIOUS_EMBED_MESSAGE = EMBED_MESSAGE
                EMBED_MESSAGE = None
        
    except:
        pass

def getAttempts():

    try:
        memory = gd.memory.get_memory()
    except RuntimeError:
        print("GD Not detected. Exiting...")
        time.sleep(5)
        sys.exit("Geometry Dash not running.")

    attempts = memory.get_attempts()

    return attempts

def getData():
    
    try:
        memory = gd.memory.get_memory()
    except RuntimeError:
        print("GD Not detected. Exiting...")
        time.sleep(5)
        sys.exit("Geometry Dash not running.")

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

try:
    gd.memory.get_memory()
except:
    print("No GD detected")
else:
    client.run(con["token"])