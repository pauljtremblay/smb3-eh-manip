import logging
import time

import cv2

from smb3_eh_manip.app.opencv.util import locate_all_opencv
from smb3_eh_manip.util import settings

TARGET_FRAME = settings.ACTION_FRAMES[0]
# it takes 3 frames to show the 'super' ui from start press
START_OFFSET_FRAMES = 3
START_OFFSET_MS = START_OFFSET_FRAMES * settings.NES_MS_PER_FRAME
TARGET_FRAME_MS = TARGET_FRAME * settings.NES_MS_PER_FRAME
OFFSET_MS = settings.get_int("offset_frames", fallback=106) * settings.NES_MS_PER_FRAME


class LatencyMsTester:
    def __init__(self):
        self.region = settings.get_config_region("latency_ms_tester_region")
        self.template = cv2.imread(
            settings.get(
                "latency_ms_tester_path", fallback="data/latency_ms_tester/trigger.png"
            )
        )
        self.start_time = None

    def reset(self, start_time):
        self.start_time = start_time

    def tick(self, frame, current_frame):
        if frame is None or not self.start_time:
            return False
        if list(locate_all_opencv(self.template, frame, region=self.region)):
            now = time.time()
            latency_ms = round(
                (
                    round((now - self.start_time) * 1000)
                    - TARGET_FRAME_MS
                    - START_OFFSET_MS
                    + OFFSET_MS
                ),
                1,
            )
            frames_away = round(current_frame - TARGET_FRAME - START_OFFSET_FRAMES, 1)
            logging.info(
                f"frames away from {TARGET_FRAME}: {frames_away} latency: {latency_ms}"
            )
            self.start_time = None
