import logging
import time

import cv2
from pygrabber.dshow_graph import FilterGraph, FilterType

from smb3_eh_manip.app.opencv.input_latency_tester import InputLatencyTester
from smb3_eh_manip.app.opencv.latency_ms_tester import LatencyMsTester
from smb3_eh_manip.app.opencv.util import locate_all_opencv
from smb3_eh_manip.ui.video_player import VideoPlayer
from smb3_eh_manip.util import settings

LOGGER = logging.getLogger(__name__)


class Opencv:
    def __init__(self, offset_frames):
        self.player_window_title = settings.get(
            "player_window_title", fallback="data/eh/video.avi"
        )
        self.start_frame_image_path = settings.get(
            "start_frame_image_path", fallback="data/eh/trigger.png"
        )
        self.start_frame_image_region = settings.get_config_region(
            "start_frame_image_region"
        )
        self.show_capture_video = settings.get_boolean("show_capture_video")
        self.write_capture_video = settings.get_boolean(
            "write_capture_video", fallback=False
        )
        self.enable_video_player = settings.get_boolean("enable_video_player")
        self.enable_input_latency_tester = settings.get_boolean(
            "enable_input_latency_tester"
        )
        self.enable_latency_ms_tester = settings.get_boolean("enable_latency_ms_tester")

        self.reset_template = cv2.imread(
            settings.get("reset_image_path", fallback="data/reset.png")
        )
        self.template = cv2.imread(self.start_frame_image_path)
        self.graph = FilterGraph()
        self.graph.add_video_input_device(settings.get_int("video_capture_source"))
        self.graph.add_sample_grabber(self.on_frame_received)
        self.graph.add_null_render()
        self.graph.prepare_preview_graph()
        self.graph.run()
        self.frame = None
        if self.write_capture_video:
            path = settings.get("write_capture_video_path", fallback="capture.avi")
            fps = 60
            video_input = self.graph.filters[FilterType.video_input]
            width, height = video_input.get_current_format()
            self.output_video = cv2.VideoWriter(
                path, cv2.VideoWriter_fourcc(*"MPEG"), fps, (width, height)
            )
        if self.enable_video_player:
            self.video_player = VideoPlayer(
                settings.get("video_path", fallback="data/eh/video.avi"),
                offset_frames,
            )
        self.reset_image_region = settings.get_config_region("reset_image_region")
        if self.enable_input_latency_tester:
            self.input_latency_tester = InputLatencyTester()
        if self.enable_latency_ms_tester:
            self.latency_ms_tester = LatencyMsTester()

    def tick(self, current_frame):
        start_read_frame = time.time()
        self.graph.grab_frame()
        read_frame_duration = time.time() - start_read_frame
        LOGGER.debug(f"Took {read_frame_duration}s to read frame")
        if self.write_capture_video and self.frame is not None:
            self.output_video.write(self.frame)
        if self.enable_input_latency_tester and self.frame is not None:
            self.input_latency_tester.tick(self.frame, current_frame)
        if self.enable_latency_ms_tester and self.frame is not None:
            self.latency_ms_tester.tick(self.frame, current_frame)
        if self.show_capture_video and self.frame is not None:
            cv2.imshow("capture", self.frame)

    def should_autoreset(self):
        if self.frame is None:
            return False
        return list(
            locate_all_opencv(
                self.reset_template, self.frame, region=self.reset_image_region
            )
        )

    def reset(self):
        if self.enable_video_player:
            self.video_player.reset()

    def should_start_playing(self):
        if self.frame is None:
            return False
        results = list(
            locate_all_opencv(
                self.template, self.frame, region=self.start_frame_image_region
            )
        )
        if self.show_capture_video:
            for x, y, needleWidth, needleHeight in results:
                top_left = (x, y)
                bottom_right = (x + needleWidth, y + needleHeight)
                # cv2.rectangle(self.frame, top_left, bottom_right, (0, 0, 255), 5)
        if results:
            LOGGER.info(f"Detected start frame")
            return True
        return False

    def start_playing(self, start_time):
        if self.enable_video_player:
            self.video_player.play()
        if self.enable_input_latency_tester:
            self.input_latency_tester.reset()
        if self.enable_latency_ms_tester:
            self.latency_ms_tester.reset(start_time)

    def terminate(self):
        if self.enable_video_player:
            self.video_player.terminate()
        if self.write_capture_video:
            self.output_video.release()
        self.graph.stop()
        cv2.destroyAllWindows()

    def on_frame_received(self, frame):
        self.frame = frame
