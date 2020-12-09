import yaml
from os import path
import sys
import time
import err

#Path to configuration file
config_file = "config.yml"

#Checking if the file exists, and if not, creating it
if not path.exists(config_file):

    with open(config_file,"w") as f:

        new_config = {"channel":"None","token":"None","prefix":"gd!"}
        yaml.dump(new_config,f)

#Loading config
config = yaml.safe_load(open(config_file))

#checks to make sure all needed settings exist
try:
    config["channel"]
    config["token"]
    config["prefix"]
except KeyError:
    err.fatalError("Invalid config.yml")

def update(new_config):
    """
    Saves changed configuration to the config file
    """
    global config_file
    yaml.dump(new_config, open(config_file,"w"))