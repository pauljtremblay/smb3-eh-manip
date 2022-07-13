from smb3_eh_manip.video_player import VideoPlayer
from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip.settings import config

# rounded
NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE

# avermedia livegamer 4k as seen here: https://i.imgur.com/V3MtlkP.png
CAPTURE_CARD_LATENCY_MS = 36
MONITOR_LATENCY_MS = 2
# I measured mine as 4, so i will avoid the following calculations
# LATENCY_FRAMES = int((MONITOR_LATENCY_MS + CAPTURE_CARD_LATENCY_MS) / NES_MS_PER_FRAME)
VIDEO_OFFSET_FRAMES = 106


class EhComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            VideoPlayer(
                "ehvideo",
                config.get("app", "eh_video_path"),
                config.getint("app", "latency_frames") + VIDEO_OFFSET_FRAMES,
            ),
            config.get("app", "eh_start_frame_image_path"),
        )