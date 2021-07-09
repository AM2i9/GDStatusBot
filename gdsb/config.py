from typing import Any
from os import path
import logging

from gdsb.log import reset_terminal
import yaml

log = logging.getLogger()

# Path to configuration file
CONFIG_PATH = "config.yml"

# Checking if the file exists, and if not, creating it
if not path.exists(CONFIG_PATH):
    log.warn("No config file found, creating a new one.")
    with open(CONFIG_PATH,"w") as f:
        new_config = {"channel":None,"token":None,"prefix":"gd!","user":None}

        while not new_config["token"]:
            new_config["token"] = input("Input your bot token (https://gist.github.com/frank-dspeed/db39a021c1cb006ddc5b9b771667d273)\n>")

        prefix = input("Input your prefix [gd!]\n>")
        if prefix:
            new_config["prefix"] = prefix
        
        yaml.dump(new_config,f)
        
        reset_terminal()
        log.info(f"Basic config saved. User and Channel ID's, as well as the previous two settings, can be changed in {CONFIG_PATH} at any time.")

# Loading config
_config = yaml.safe_load(open(CONFIG_PATH))

class ConfigLoader(type):

    def __setattr__(self, name: str, value: Any):

        _config[name] = value
        yaml.dump(_config, open(CONFIG_PATH,"w"))

        return super().__setattr__(name, value)

    def __getattr__(cls, name):
        name = name.lower()

        try:
            config_value = _config[name]
        except KeyError as e:
            raise AttributeError(repr(name)) from e
        else:
            
            return config_value
    
    def __getitem__(cls, name):
        return cls.__getattr__(name)

class Config(metaclass=ConfigLoader):

    channel: int
    token: str
    prefix: str
    user: int