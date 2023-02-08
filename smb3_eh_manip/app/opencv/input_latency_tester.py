import logging

import cv2

from smb3_eh_manip.app.opencv.util import locate_all_opencv
from smb3_eh_manip.util import events, settings

ACTION_FREQUENCY = 5 * 60  # roughly 5 seconds between audio cues


class InputLatencyTester:
    def __init__(self):
        self.region = settings.get_config_region("input_latency_tester_region")
        self.template = cv2.imread(
            settings.get(
                "input_latency_tester_path", fallback="data/input_latency_tester/trigger.png"
            )
        )
        self.ewma_latency_frames = 0.0
        # we can tick many times per video frame, so lets only count the first time we see the jump
        self.last_tick_found_jump = False
        self.initialize_audio_cues()

    def reset(self):
        self.initialize_audio_cues()

    def tick(self, frame, current_frame):
        if frame is None:
            return False
        if list(locate_all_opencv(self.template, frame, region=self.region)):
            if self.last_tick_found_jump:
                return
            frames_away_frame_closest = (
                (current_frame + ACTION_FREQUENCY // 2) % ACTION_FREQUENCY
                - ACTION_FREQUENCY // 2
                - 2  # it takes 2 frames for mario to actually jump
            )
            if abs(frames_away_frame_closest) > 20:
                # this was probably when landing, lets disregard
                return
            self.ewma_latency_frames = (
                self.ewma_latency_frames * 0.95 + 0.05 * frames_away_frame_closest
            )
            logging.info(
                f"ewma_latency_frames={self.ewma_latency_frames} frames_away_frame_closest={frames_away_frame_closest}"
            )
            self.last_tick_found_jump = True
        else:
            self.last_tick_found_jump = False

    def initialize_audio_cues(self):
        initial_offset = ACTION_FREQUENCY * 3
        for offset in range(1000):
            events.emit(
                self,
                events.AddActionFrame(initial_offset + ACTION_FREQUENCY * offset, 1),
            )
