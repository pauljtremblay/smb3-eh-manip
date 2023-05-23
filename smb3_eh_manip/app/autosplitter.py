from smb3_video_autosplitter.autosplitter import Autosplitter as VideoAutosplitter
from smb3_video_autosplitter.settings import Settings

from smb3_eh_manip.util.settings import get_list


class Autosplitter:
    def __init__(self):
        self.default_start_or_split_frames = get_list(
            "autosplitter_start_or_split_frames", fallback="1925"
        )
        autosplitter_config = Settings.load("autosplitter_config.yml")
        self.autosplitter = VideoAutosplitter(autosplitter_config)
        self.start_or_split_frames = list(self.default_start_or_split_frames)

    def reset(self):
        self.start_or_split_frames = list(self.default_start_or_split_frames)
        self.autosplitter.livesplit.send("reset")
        self.autosplitter.reset()

    def tick(self, current_frame: int, frame):
        self.autosplitter.tick(frame)
        if (
            self.start_or_split_frames
            and self.start_or_split_frames[0] <= current_frame
        ):
            self.start_or_split_frames.pop(0)
            self.autosplitter.livesplit.send("startorsplit")

    def terminate(self):
        self.autosplitter.terminate()
