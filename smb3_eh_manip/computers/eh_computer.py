from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip import settings


class EhComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            "ehvideo",
            settings.get("eh_video_path"),
            settings.get("eh_start_frame_image_path"),
            video_offset_frames=106,
            start_frame_image_region=settings.get_config_region(
                "eh_start_frame_image_region"
            ),
        )
