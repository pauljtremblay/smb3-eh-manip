from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip import settings


class TwoOneComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            "twoonevideo",
            settings.get("two_one_video_path", fallback="data/eh/video.avi"),
            settings.get(
                "two_one_start_frame_image_path", fallback="data/two_one/trigger.png"
            ),
            video_offset_frames=16680,
            start_frame_image_region=settings.get_config_region(
                "two_one_start_frame_image_region"
            ),
        )
