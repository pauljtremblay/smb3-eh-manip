from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE

ACTION_FRAMES = [270, 1659, 16828, 18046, 18654, 19947, 20611, 22669, 23952]
FREQUENCY = 24


def get_config_region(domain, name):
    """ Parse a region str from ini """
    region_str = config.get(domain, name, fallback=None)
    if region_str:
        return list(map(int, region_str.split(",")))
    return None