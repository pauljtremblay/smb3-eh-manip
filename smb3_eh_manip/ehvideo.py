import cv2
import numpy as np

# rounded
NES_FRAMERATE = 60.0988139
NES_MS_PER_FRAME = 1000.0 / NES_FRAMERATE
VIDEO_PATH = "data/orange-nodeath-eh-v0.avi"

# the video I made doesn't start at t=0, it starts 2 frames in :(
VIDEO_OFFSET_FRAMES = 2  # TODO would be great to fix this
# avermedia livegamer 4k as seen here: https://i.imgur.com/V3MtlkP.png
CAPTURE_CARD_LATENCY_MS = 36
MONITOR_LATENCY_MS = 2
LATENCY_FRAMES = int((MONITOR_LATENCY_MS + CAPTURE_CARD_LATENCY_MS) / NES_MS_PER_FRAME)
EXTRA_OVERHEAD_FRAMES = (
    100  # TODO this is egregious and immeasurable surely we can optimize this
)


class EHVideo:
    def __init__(self):
        self.video = None
        self.playing = False

    def reset(self):
        # the video does not start at the beginning, the capture card adds
        # latency, and monitor. so let's fast forward the video so it visually
        # appears the same.
        self.release()
        self.playing = False
        self.video = cv2.VideoCapture(VIDEO_PATH)
        if self.video is None:
            return
        if not self.video.isOpened():
            self.release()
            return
        self.video.set(
            cv2.CAP_PROP_POS_FRAMES,
            VIDEO_OFFSET_FRAMES + LATENCY_FRAMES + EXTRA_OVERHEAD_FRAMES,
        )
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        cv2.imshow("ehvideo", np.zeros(shape=[height, width, 3], dtype=np.uint8))

    def set_playing(self, playing):
        self.playing = playing

    def render(self):
        if not self.playing:
            return
        if self.video is None:
            return
        if not self.video.isOpened():
            self.release()
            return
        ret, frame = self.video.read()
        if ret == True:
            cv2.imshow("ehvideo", frame)

    def release(self):
        self.playing = False
        if self.video:
            self.video.release()
            self.video = None