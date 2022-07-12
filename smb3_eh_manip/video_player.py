import cv2
import numpy as np


class VideoPlayer:
    def __init__(self, window_title, video_path, seek_to_frame=0):
        self.window_title = window_title
        self.video_path = video_path
        self.seek_to_frame = seek_to_frame
        self.video = None
        self.playing = False

    def reset(self):
        # the video does not start at the beginning, the capture card adds
        # latency, and monitor. so let's fast forward the video so it visually
        # appears the same.
        self.release()
        self.playing = False
        self.video = cv2.VideoCapture(self.video_path)
        if self.video is None:
            return
        if not self.video.isOpened():
            self.release()
            return
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        cv2.imshow(
            self.window_title, np.zeros(shape=[height, width, 3], dtype=np.uint8)
        )
        if self.seek_to_frame:
            # the video does not start at the beginning, the capture card adds
            # latency, and monitor. so let's fast forward the video so it visually
            # appears the same.
            self.video.set(cv2.CAP_PROP_POS_FRAMES, self.seek_to_frame)

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
            cv2.imshow(self.window_title, frame)

    def release(self):
        self.playing = False
        if self.video:
            self.video.release()
            self.video = None