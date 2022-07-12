from smb3_eh_manip.video_player import VideoPlayer
from smb3_eh_manip.computers import OpencvComputer


class CalibrationComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            VideoPlayer("calibrationvideo", "data/smb3practice-start11.m4v"),
            "data/smb3practice_frame23.png",
        )
