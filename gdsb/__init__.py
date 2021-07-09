import logging

import gd

from gdsb.log import reset_terminal
from gdsb.bot import start_bot

instance = None

_log = logging.getLogger()

def wait_for_gd():

    _log.info("Waiting for GD...")
    while True:
        try:
            gd.memory.get_memory()
        except RuntimeError:
            continue
        else:
            _log.info("GD Detected.")
            break

def main():
    reset_terminal()
    wait_for_gd()

    #Launching the bot
    _log.info("Starting bot...")
    start_bot()