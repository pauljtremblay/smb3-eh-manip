from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip.settings import config, get_config_region


class CalibrationComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            "calibrationvideo",
            config.get("app", "calibration_video_path"),
            config.get("app", "calibration_start_frame_image_path"),
            start_frame_image_region=get_config_region(
                "app", "calibration_start_frame_image_region"
            ),
        )