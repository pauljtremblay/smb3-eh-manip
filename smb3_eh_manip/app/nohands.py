"""
We want to have a manip such that with a second or so upon reaching the map
with the hands, we provide an audio cue where the player only holds left to
go over the hands unscathed with a window of >2 frames (preferably 3).

The time wasted holding left is about 24 frames. The time to wait between
coming out of the pipe and holding left is ideally <30 frames.

This class watches for level changes and times when the hands should occur.
A higher level class should be keeping track of what levels we have beaten.
"""
import logging
import yaml

from smb3_eh_manip.util import settings

# when holding left exiting the pipe, the frame# from origin to specific hand
TO_HAND1_CHECK_FRAME_DURATION = 18
TO_HAND2_CHECK_FRAME_DURATION = 40
TO_HAND3_CHECK_FRAME_DURATION = 17

# step1: reliable method for detecting level/world changes. keep track of this in
# parent class.
# step2: identify this pipe transition - in world 8, the 3rdish area in
# which we see 13 lag frames.
# step3: upon using the start/end pipe, identify frame windows in the
# second after exiting the pipe to trigger audio cue
# step4: trigger audio cue :D

class NoHands:
    def __init__(self):
        self.category_name = settings.get("category", fallback="nww")
        self.reset()

    def reset(self):
        self.last_lag_frame_count = 0
        with open(f'data/categories/{self.category_name}.yml', 'r') as file:
            self.category = yaml.safe_load(file)

    def tick(self, lag_frames):
        recent_lag_frames = lag_frames - self.last_lag_frame_count
        if not recent_lag_frames:
            return
        breakpoint()
        if self.active_section() == recent_lag_frames:
            section = self.category.sections.pop()
            logging.info(f"Completed {section}")

    def active_section(self):
        return list(self.category["sections"])[0]