from smb3_eh_manip.video_player import VideoPlayer
from smb3_eh_manip.computers.opencv_computer import OpencvComputer

# rounded
NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE

# the video I made doesn't start at t=0, it starts 2 frames in :(
VIDEO_OFFSET_FRAMES = 2  # TODO would be great to fix this
# avermedia livegamer 4k as seen here: https://i.imgur.com/V3MtlkP.png
CAPTURE_CARD_LATENCY_MS = 36
MONITOR_LATENCY_MS = 2
LATENCY_FRAMES = int((MONITOR_LATENCY_MS + CAPTURE_CARD_LATENCY_MS) / NES_MS_PER_FRAME)
EXTRA_OVERHEAD_FRAMES = (
    110  # TODO this is egregious and immeasurable surely we can optimize this
)


class EhComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            VideoPlayer(
                "ehvideo",
                "data/orange-nodeath-eh-v0.avi",
                VIDEO_OFFSET_FRAMES + LATENCY_FRAMES + EXTRA_OVERHEAD_FRAMES,
            ),
            "data/smb3OpencvFrame.png",
        )