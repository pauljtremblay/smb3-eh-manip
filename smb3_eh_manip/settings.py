from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE


def get_config_region(domain, name):
    """ Parse a region str from ini """
    region_str = config.get(domain, name)
    if region_str:
        return list(map(int, region_str.split(",")))
    return None