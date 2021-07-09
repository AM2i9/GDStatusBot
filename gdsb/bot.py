"""
  /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$$ 
 /$$__  $$| $$__  $$ /$$__  $$| $$__  $$
| $$  \__/| $$  \ $$| $$  \__/| $$  \ $$
| $$ /$$$$| $$  | $$|  $$$$$$ | $$$$$$$ 
| $$|_  $$| $$  | $$ \____  $$| $$__  $$
| $$  \ $$| $$  | $$ /$$  \ $$| $$  \ $$
|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$/
 \______/ |_______/  \______/ |_______/ 
                                        
Geometry Dash Status Bot
Created by Patrick Brennan (AM2i9)
https://github.com/AM2i9/GDStatusBot
"""

import math
import random
import logging

import gd
import discord
from discord.ext import commands, tasks

import gdsb
from gdsb.level import Level, Session
import gdsb.constants as const
from gdsb.config import Config as conf

log = logging.getLogger()

class Bot(commands.Bot):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def on_ready(self):
        log.info(f"Bot logged in as {self.user}")

    @classmethod
    def create_instance(cls):

        intents = discord.Intents.default()
        intents.members = True
        
        return cls(
            command_prefix=conf["prefix"],
            intents=intents
        )

class GDSB(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.embed_message = None
        self.previous_level_id = None
        self.previous_embed_message = None

        self.current_level = None

        self.session = Session()

        self.embed = discord.Embed()

        self.main.start()
        
    @commands.command()
    async def set_channel(self, ctx: commands.Context):
        """
        Sets which channel the bot should send its messages in.
        """
        if ctx.message.author.id != conf.user:
            return None

        new_channel = ctx.channel.id

        conf.channel = new_channel

        log.info(f"Bot channel set to channel with: #{ctx.channel} (ID:{ctx.channel.id})")
        await ctx.message.channel.send(f"✅ Set bot channel for {ctx.message.author} to #{ctx.channel}")

    async def _read_memory(self):
        """
        Fetches game memory
        """
        try:
            memory = gd.memory.get_memory()
        except RuntimeError:
            return None
        else:
            return memory

    async def _fetch_level_info(self) -> Level:
        """
        Fetches gamestate data from memory

        Returns:
        Level: An object containing all current level info
        """
        
        memory = await self._read_memory()

        level_name = memory.get_level_name()
        level_creator = memory.get_level_creator()
        level_id = memory.get_level_id()

        level = Level(id=level_id, name=level_name,
                        creator = level_creator)

        level.practice_mode = memory.is_practice_mode()

        level.attempts = memory.get_attempts()
        level.jumps = memory.get_jumps()
        level.difficulty = memory.get_level_difficulty()

        level.percent = math.floor(memory.get_percent())
        level.best_percent = math.floor(memory.get_normal_percent())

        level.practice_best = math.floor(memory.get_practice_percent())

        level.rating = memory.get_level_stars()
        level.featured = memory.is_level_featured()
        level.epic = memory.is_level_epic()

        return level
    
    def _get_progress_bar(self, percent: int) -> str:
        """
        Generate a progress bar based on a percentage

        Parameters:
        percent (int): The current level percentage
        """
        
        full_bars = percent // 5

        bar = "▓" * full_bars
        bar += "░" * (20 - full_bars)

        return bar

    def _get_rating_text(self) -> str:
        """
        Generate text for dispaly on the embed showing the
        current level's rating
        """

        rating_text = ""
        if self.current_level.rating:
            rating_text = f"{self.current_level.rating}⭐"

        return rating_text

    def _get_category_text(self) -> str:
        """
        Generate text for dispaly on the embed showing the
        current level's category (Featured/Epic)
        """

        category = ""
        if self.current_level.is_featured():
            category = "Featured 👀"
        elif self.current_level.is_epic():
            category = "Epic 🔥"

        return category

    @tasks.loop(seconds=2)
    async def main(self):

        """
        The main loop of the program. Everything happens here. It executes every 2 seconds to update the embed.
        """

        # Fetching the game memory
        memory = await self._read_memory()

        if not memory:
            log.warn("Could not find GD. Program will wait until it is found.")
            gdsb.wait_for_gd()
            return

        if memory.is_in_level():

            if memory.get_level_id() != self.previous_level_id:
                await self.seal_embed()

            # Fetch gamestate data
            self.current_level = await self._fetch_level_info()
            
            # Gets wether or not the level being played is the exact same level that was played just previously, so that it will continue to use the same embed
            if self.previous_level_id != self.current_level.id:

                self.embed_message = None
                self.previous_embed_message = None

                self.session.start_attempts = self.current_level.attempts
                self.session.old_best = self.current_level.best_percent
                self.session.best = 0

            else:

                if self.previous_embed_message is not None:
                    self.embed_message = self.previous_embed_message

            self.previous_level_id = self.current_level.id

            # So for some reason, the main levels all have their creator blank, so we just set it to RobTop
            if self.current_level.creator == "":
                self.current_level.creator = "RobTop"

            # Getting if you are playing a main level or not. If so, we have to manually set the difficulty using the list I made earlier
            if self.current_level.id in range(1,22):
                
                self.current_level.difficulty = const.MAIN_LEVEL_DIFFICULTIES[self.current_level.id-1]

            # Checks if the player is in practice mode or not. If they are, it will display a different color
            if self.current_level.is_practice_mode():
                title = "Practicing: {0}"
                color = discord.Color.from_rgb(59, 223, 245)
            else:
                title = "Playing: {0}"
                color = discord.Color.from_rgb(18, 219, 31)

            # A few little extra texts that go next to the title
            extra_text = ""
            if self.current_level.percent == 100:

                if self.current_level.is_practice_mode():
                    extra_text=" - PRACTICE COMPLETE!"
                else:
                    extra_text=" - LEVEL COMPLETE!"
                    color = discord.Color.from_rgb(237, 220, 28)

            elif self.current_level.best_percent > self.session.old_best:
                extra_text = " - New Best!"
                self.session.old_best = self.current_level.best_percent

            # Saving the best percent of the session
            if self.current_level.percent > self.session.best and not self.current_level.is_practice_mode():
                self.session.best = self.current_level.percent

            # Calculating the current attempts on a level
            self.current_level.attempts = (self.current_level.attempts - self.session.start_attempts) + 1

            rating_text = self._get_rating_text()
            category = self._get_category_text()

            self.embed.title = title.format(self.current_level.name)
            self.embed.description = f"By {'  |  '.join((self.current_level.creator, rating_text, category))}"
            self.embed.color = color

            self.embed.set_thumbnail(url=const.FACES[const.DIFFICULTIES.index(self.current_level.difficulty)])

            # Getting user
            user = self.bot.get_user(conf.user)

            self.embed.set_author(name=user.display_name, icon_url=user.avatar_url)

            progress_bar_state = self._get_progress_bar(self.current_level.percent)

            fields = (
                {"name": "Attempt:", "value": self.current_level.attempts, "inline": True},
                {"name": "Best %:", "value": f"{self.current_level.best_percent}%", "inline": True},
                {"name": "Current Progress:", "value": f"{self.current_level.percent}%{extra_text}\n{progress_bar_state}", "inline": False}
            )

            for i, field in enumerate(fields):

                if len(self.embed.fields) < len(fields):
                    self.embed.add_field(**field)
                else:
                    self.embed.set_field_at(i, **field)
            
            self.embed.set_footer(text="Level ID: {0}".format(self.current_level.id))
            
            # Sending embed

            channel = self.bot.get_channel(conf.channel)

            if not channel:
                log.error(f"Could not find channel with id: {conf.channel}. Use '{conf.prefix}set_channel' to set the channel.")
            else:
                #If the channel is found, edit the message the embed has been sent to, and if it dosent exist, create it.
                if self.embed_message is None:
                    self.embed_message = await channel.send(embed=self.embed)
                else:
                    await self.embed_message.edit(embed=self.embed)
                
        else:

            if memory:
                await self.seal_embed()

                #Sets some globals so that the embed can be reused if the same level is played again
                self.previous_embed_message = self.embed_message
                self.embed_message = None
    
    @main.before_loop
    async def before_main(self):

        await self.bot.wait_until_ready()

        if not conf.user:
            await self.get_user()

    async def seal_embed(self):
        """
        Seals off the embed if a player goes to the menu, or exits the level
        """       

        if self.embed_message is not None:

            self.embed.title = f"Played: {self.current_level.name}"
            self.embed.color = discord.Color.default()

            self.embed.clear_fields()

            self.embed.add_field(name="Attempts:",value=self.current_level.attempts,inline=True)
            self.embed.add_field(name="Total Attempts:",value=self.current_level.attempts,inline=True)
            self.embed.add_field(name="Total Jumps:",value=self.current_level.jumps,inline=True)
            self.embed.add_field(name="Best Session %:",value=f"{self.session.best}%\n{self._get_progress_bar(self.session.best)}",inline=False)
            self.embed.add_field(name="Best Lifetime %:",value=f"{self.current_level.best_percent}%\n{self._get_progress_bar(self.current_level.best_percent)}",inline=False)

            await self.embed_message.edit(embed=self.embed)
            self.embed = discord.Embed()

    async def get_user(self):
        """
        Allows the user to link their discord account to the bot through their user id
        """

        def check_if_dm(message: discord.Message):

            if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.bot.user:
                return True
            else:
                return False

        token = ''.join(str(random.randint(1,10)) for i in range(7))

        log.warn(f"To use the bot, you need to link your Discord account to the bot. To link your Discord account to the bot, open a new direct message with the bot and send it the following code: {token}")

        while True:

            message = await self.bot.wait_for('message',check=check_if_dm)

            if message.content == token:
                
                await message.channel.send("Linking account...")
                log.info("Token recieved, linking account")

                conf.user = message.author.id

                await message.channel.send("Account Linked")
                log.info('Account linked.')
                break

            else:

                log.info("That is not the correct token, please send the correct token printed previously")

def start_bot():
    
    try:
        gdsb.instance = Bot.create_instance()
        gdsb.instance.add_cog(GDSB(gdsb.instance))

        gdsb.instance.run(conf.token)
    except discord.errors.LoginFailure as e:
        log.error(f"Could not login: {e}")
    except discord.errors.PrivilegedIntentsRequired:
        log.error(f"You must enable Server Members Intent on your bot in the Developer Portal. For more information, read the 'Heads up' on release 1.1.0 (https://github.com/AM2i9/GDStatusBot/releases/tag/v1.1.0)")