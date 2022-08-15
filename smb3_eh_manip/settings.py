from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE

FREQUENCY = 24


def get_config_region(domain, name):
    """ Parse a region str from ini """
    return get_list(domain, name)


def get_list(domain, name):
    """ Parse a region str from ini """
    list_str = config.get(domain, name, fallback=None)
    if list_str:
        return list(map(int, list_str.split(",")))
    return None


def get_action_frames():
    computer_name = config.get("app", "computer")
    if computer_name == "eh":
        frames = get_list("app", "eh_action_frames")
        return (
            frames
            if frames
            else [270, 1659, 16000, 16828, 18046, 18654, 19947, 20611, 22670, 23952]
        )
    elif computer_name == "twoone":
        frames = get_list("app", "twoone_action_frames")
        return frames if frames else [90, 1194, 1799, 3094]
    else:
        raise Exception(
            f"Action frames not available for computer name {computer_name}"
        )


ACTION_FRAMES = get_action_frames()