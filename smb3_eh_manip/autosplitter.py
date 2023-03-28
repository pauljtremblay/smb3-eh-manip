"""
video based autosplitter for smb3
"""

import logging
import time

import cv2
from pygrabber.dshow_graph import FilterGraph
import win32file, win32pipe

from smb3_eh_manip.app.opencv.util import locate_all_opencv
from smb3_eh_manip.util import settings

LOGGER = logging.getLogger(__name__)
SPLIT_DEDUPE_WAIT_S = settings.get_int("SPLIT_DEDUPE_WAIT_S", fallback=5.0)
SPLIT_OFFSET_FRAMES = settings.get_int("SPLIT_OFFSET_FRAMES", fallback=40)
SPLIT_OFFSET_S = (SPLIT_OFFSET_FRAMES * 16.64) / 1000

"""
autosplitter_region = 565,517,82,109
"""


class Autosplitter:
    def __init__(self):
        self.region = settings.get_config_region("autosplitter_region")
        self.template = cv2.imread(
            settings.get(
                "autosplitter_path",
                fallback="data/autosplitter/trigger.png",
            )
        )
        self.handle = win32file.CreateFile(
            r"\\.\pipe\LiveSplit",
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None,
        )
        res = win32pipe.SetNamedPipeHandleState(
            self.handle, win32pipe.PIPE_READMODE_BYTE, None, None
        )
        if res == 0:
            print(f"SetNamedPipeHandleState return code: {res}")
        self.earliest_next_trigger_time = 0

    def tick(self, frame):
        if frame is None or self.earliest_next_trigger_time >= time.time():
            return
        if list(locate_all_opencv(self.template, frame, region=self.region)):
            time.sleep(SPLIT_OFFSET_S)
            self.earliest_next_trigger_time = time.time() + SPLIT_DEDUPE_WAIT_S
            win32file.WriteFile(self.handle, b"split\r\n")
            LOGGER.info(f"Livesplit autosplit")


class OpenCV:
    def __init__(self):
        self.graph = FilterGraph()
        self.graph.add_video_input_device(settings.get_int("video_capture_source"))
        self.graph.add_sample_grabber(self.on_frame_received)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()
        self.frame = None

    def tick(self):
        self.graph.grab_frame()

    def on_frame_received(self, frame):
        self.frame = frame


def main():
    opencv = OpenCV()
    autosplitter = Autosplitter()
    while True:
        opencv.tick()
        autosplitter.tick(opencv.frame)


if __name__ == "__main__":
    main()
