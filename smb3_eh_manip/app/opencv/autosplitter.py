import logging

import cv2

from smb3_eh_manip.app.opencv.util import locate_all_opencv
from smb3_eh_manip.app.servers.livesplit_client import LivesplitClient
from smb3_eh_manip.util import settings

LOGGER = logging.getLogger(__name__)
AUTOSPLITTER_OFFSET_FRAMES = settings.get_int("autosplitter_offset_frames", fallback=60)


class Autosplitter:
    def __init__(self, livesplit_client: LivesplitClient):
        self.region = settings.get_config_region("autosplitter_region")
        self.template = cv2.imread(
            settings.get(
                "autosplitter_path",
                fallback="data/autosplitter/trigger.png",
            )
        )
        self.livesplit_client = livesplit_client
        self.reset()

    def reset(self):
        self.minimum_next_trigger_frame = None

    def tick(self, frame, current_frame):
        if frame is None or current_frame == -1:
            return
        if (
            self.minimum_next_trigger_frame is not None
            and self.minimum_next_trigger_frame < current_frame
        ):
            return
        if list(locate_all_opencv(self.template, frame, region=self.region)):
            breakpoint()
            self.minimum_next_trigger_frame = current_frame + AUTOSPLITTER_OFFSET_FRAMES
            LOGGER.info(f"Autosplitter on frame {current_frame}")
            self.livesplit_client.split()
