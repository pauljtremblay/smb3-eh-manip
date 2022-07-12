from smb3_eh_manip.video_player import VideoPlayer
from smb3_eh_manip.computers import OpencvComputer


class CalibrationComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            VideoPlayer("calibrationvideo", "data/smb3practice-start11.mp4"),
            "data/smb3practice-start11-begin.png",
        )
