import discord
import config
import gd
import math
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="gf!")
con = config.config

EMBED = None
EMBED_MESSAGE = None

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
    global EMBED, EMBED_MESSAGE

    memory = None

    try:
        memory = gd.memory.get_memory()
    except RuntimeError:
        print("GD Not detected. Exiting...")
        time.sleep(5)
        sys.exit("Geometry Dash not running.")

    try:
        if memory.is_in_level():

            level_name = memory.get_level_name()
            level_creator = memory.get_level_creator()
            level_best = memory.get_normal_percent()
            level_id = memory.get_level_id()
            practice_mode = memory.is_practice_mode()
            percent = memory.get_percent()
            attempts = memory.get_attempts()
            difficulty = memory.get_level_difficulty()
            level_best = memory.get_normal_percent()

            if level_creator == "":
                level_creator = "RobTop"

            EMBED = discord.Embed(type="rich",title=level_name,description=f"By {level_creator}")
            EMBED.set_thumbnail(url="https://cdn.discordapp.com/attachments/675532248493326359/785672433948164116/Easy.png")
            EMBED.add_field(name="Total Attempts:",value=attempts,inline=True)
            EMBED.add_field(name="Progress:",value=f"{math.floor(percent)}%",inline=False)
            EMBED.set_footer(text=f"Level ID: {level_id}")

            channel = client.get_channel(con["channel"])

            if channel is not None:

                if EMBED_MESSAGE is None:
                    EMBED_MESSAGE = await channel.send(embed=EMBED)
                else:
                    await EMBED_MESSAGE.edit(embed=EMBED)
        else:
            EMBED_MESSAGE = None
    except:
        pass

try:
    gd.memory.get_memory()
except:
    print("No GD detected")
else:
    client.run(con["token"])