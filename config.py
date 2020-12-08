import yaml

config_file = "config.yml"
config = yaml.safe_load(open(config_file))

def update(new_config):
    global config_file
    yaml.dump(new_config, open(config_file,"w"))