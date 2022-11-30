from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip.util import settings


class CalibrationComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            "calibrationvideo",
            settings.get(
                "calibration_video_path", fallback="data/calibration/video.mp4"
            ),
            settings.get(
                "calibration_start_frame_image_path",
                fallback="data/calibration/trigger.png",
            ),
            start_frame_image_region=settings.get_config_region(
                "calibration_start_frame_image_region"
            ),
        )
