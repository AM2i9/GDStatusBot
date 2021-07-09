import logging
import sys
import os

import colorlog

logfile_format_str = '[%(asctime)s] %(levelname)s: %(message)s'
console_fmt_str = '%(log_color)s[%(levelname)s] %(message)s'

root_log = logging.getLogger()
root_log.setLevel(logging.DEBUG)

stream = logging.StreamHandler(sys.stdout)
file = logging.FileHandler("gdsb.log")
console_formatter = colorlog.ColoredFormatter(console_fmt_str)
file_formatter = logging.Formatter(logfile_format_str)
stream.setFormatter(console_formatter)
file.setFormatter(file_formatter)

root_log.addHandler(stream)
root_log.addHandler(file)

logging.getLogger('discord').setLevel(logging.CRITICAL)

def reset_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""  /$$$$$$  /$$$$$$$   /$$$$$$  /$$$$$$$ 
 /$$__  $$| $$__  $$ /$$__  $$| $$__  $$
| $$  \__/| $$  \ $$| $$  \__/| $$  \ $$
| $$ /$$$$| $$  | $$|  $$$$$$ | $$$$$$$ 
| $$|_  $$| $$  | $$ \____  $$| $$__  $$
| $$  \ $$| $$  | $$ /$$  \ $$| $$  \ $$
|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$/
 \______/ |_______/  \______/ |_______/ 
                                        
Geometry Dash Status Bot
Created by Patrick Brennan (AM2i9)
https://github.com/AM2i9/GDStatusBot""")