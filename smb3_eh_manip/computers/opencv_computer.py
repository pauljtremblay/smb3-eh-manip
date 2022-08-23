import logging
import sys
import time

import cv2
import numpy as np

from smb3_eh_manip.audio_player import AudioPlayer
from smb3_eh_manip import settings
from smb3_eh_manip.fceux_lua_server import *
from smb3_eh_manip.ui_player import UiPlayer
from smb3_eh_manip.video_player import VideoPlayer

CLEAR_SIGHTING_DURATION_SECONDS = 10


class OpencvComputer:
    def __init__(
        self,
        player_window_title,
        player_video_path,
        start_frame_image_path,
        video_offset_frames=0,
        start_frame_image_region=None,
    ):
        self.player_window_title = player_window_title
        self.start_frame_image_path = start_frame_image_path
        self.start_frame_image_region = start_frame_image_region
        self.video_offset_frames = video_offset_frames
        self.latency_ms = settings.get_int("latency_ms")
        self.show_capture_video = settings.get_boolean("show_capture_video")
        self.autoreset = settings.get_boolean("autoreset")
        self.enable_fceux_tas_start = settings.get_boolean("enable_fceux_tas_start")
        self.write_capture_video = settings.get_boolean("write_capture_video")
        self.enable_video_player = settings.get_boolean("enable_video_player")
        self.enable_audio_player = settings.get_boolean("enable_audio_player")
        self.enable_ui_player = settings.get_boolean("enable_ui_player")
        self.track_end_stage_clear_text_time = settings.get_boolean(
            "track_end_stage_clear_text_time"
        )
        self.playing = False
        self.current_time = -1
        self.start_time = -1

        if self.track_end_stage_clear_text_time:
            self.last_clear_sighting_time = -1
            self.end_stage_clear_text_template = cv2.imread(
                settings.get("end_stage_clear_text_path")
            )
        self.reset_template = cv2.imread(settings.get("reset_image_path"))
        self.template = cv2.imread(self.start_frame_image_path)
        self.capture = cv2.VideoCapture(settings.get_int("video_capture_source"))
        if not self.capture.isOpened():
            logging.info("Cannot open camera")
            sys.exit()
        if self.write_capture_video:
            path = settings.get("write_capture_video_path")
            fps = float(self.capture.get(cv2.CAP_PROP_FPS)) or 60
            height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.output_video = cv2.VideoWriter(
                path, cv2.VideoWriter_fourcc(*"MPEG"), fps, (width, height)
            )
        if self.enable_video_player:
            self.video_player = VideoPlayer(player_video_path, video_offset_frames)
        self.reset_image_region = settings.get_config_region("reset_image_region")
        self.end_stage_clear_text_region = settings.get_config_region(
            "end_stage_clear_text_region"
        )
        if self.enable_fceux_tas_start:
            waitForFceuxConnection()
        if self.enable_audio_player:
            self.audio_player = AudioPlayer()
        if self.enable_ui_player:
            self.ui_player = UiPlayer()

    def tick(self):
        start_read_frame = time.time()
        ret, frame = self.capture.read()
        logging.debug(f"Took {(time.time()-start_read_frame)*1000:.1f}ms to read frame")
        if not ret:
            logging.warn("Can't receive frame (stream end?). Exiting ...")
            sys.exit()
        if self.write_capture_video:
            self.output_video.write(frame)
        if self.playing:
            self.update_times()
        self.check_and_update_end_stage(frame)
        self.check_and_update_autoreset(frame)
        self.check_and_update_begin_playing(frame)
        if self.show_capture_video:
            cv2.imshow("capture", frame)
        if self.enable_audio_player and self.playing:
            self.audio_player.tick(self.current_frame)
        if self.enable_ui_player and self.playing:
            self.ui_player.tick(self.current_frame)
        cv2.waitKey(1)

    def check_and_update_autoreset(self, frame):
        if (
            self.autoreset
            and self.playing
            and list(
                OpencvComputer.locate_all_opencv(
                    self.reset_template, frame, region=self.reset_image_region
                )
            )
        ):
            self.playing = False
            self.start_time = -1
            self.current_time = -1
            self.current_frame = -1
            if self.enable_video_player:
                self.video_player.reset()
            if self.enable_fceux_tas_start:
                emu.pause()
                latency_offset = round(self.latency_ms / settings.NES_MS_PER_FRAME)
                taseditor.setplayback(self.video_offset_frames + latency_offset)
            logging.info(f"Detected reset")

    def check_and_update_begin_playing(self, frame):
        if not self.playing:
            results = list(
                OpencvComputer.locate_all_opencv(
                    self.template, frame, region=self.start_frame_image_region
                )
            )
            if self.show_capture_video:
                for x, y, needleWidth, needleHeight in results:
                    top_left = (x, y)
                    bottom_right = (x + needleWidth, y + needleHeight)
                    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 5)
            if results:
                self.playing = True
                self.start_time = time.time()
                self.current_frame = 0
                self.current_time = 0
                if self.enable_fceux_tas_start:
                    emu.unpause()
                if self.enable_video_player:
                    self.video_player.play()
                if self.enable_audio_player:
                    self.audio_player.reset()
                if self.enable_ui_player:
                    self.ui_player.reset()
                logging.info(f"Detected start frame")

    def check_and_update_end_stage(self, frame):
        if (
            self.track_end_stage_clear_text_time
            and self.playing
            and self.current_time - self.last_clear_sighting_time
            > CLEAR_SIGHTING_DURATION_SECONDS
            and list(
                OpencvComputer.locate_all_opencv(
                    self.end_stage_clear_text_template,
                    frame,
                    region=self.end_stage_clear_text_region,
                )
            )
        ):
            self.last_clear_sighting_time = self.current_time
            logging.info(
                f"Cleared a level at {self.current_time} on frame {self.current_frame}"
            )

    def update_times(self):
        self.current_time = time.time() - self.start_time
        self.current_frame = self.video_offset_frames + round(
            (self.latency_ms + self.current_time * 1000) / settings.NES_MS_PER_FRAME, 1
        )

    def terminate(self):
        if self.enable_video_player:
            self.video_player.terminate()
        if self.write_capture_video:
            self.output_video.release()
        self.capture.release()
        cv2.destroyAllWindows()

    @classmethod
    def locate_all_opencv(
        cls,
        needleImage,
        haystackImage,
        limit=10000,
        region=None,  # [x, y, width, height]
        confidence=float(settings.get("confidence")),
    ):
        """
        RGBA images are treated as RBG (ignores alpha channel)
        """

        confidence = float(confidence)

        needleHeight, needleWidth = needleImage.shape[:2]

        if region:
            haystackImage = haystackImage[
                region[1] : region[1] + region[3], region[0] : region[0] + region[2]
            ]
        else:
            region = (0, 0)  # full image; these values used in the yield statement
        if (
            haystackImage.shape[0] < needleImage.shape[0]
            or haystackImage.shape[1] < needleImage.shape[1]
        ):
            # avoid semi-cryptic OpenCV error below if bad size
            raise ValueError(
                "needle dimension(s) exceed the haystack image or region dimensions"
            )

        # get all matches at once, credit: https://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image/9253805#9253805
        result = cv2.matchTemplate(haystackImage, needleImage, cv2.TM_CCOEFF_NORMED)
        match_indices = np.arange(result.size)[(result > confidence).flatten()]
        matches = np.unravel_index(match_indices[:limit], result.shape)

        if len(matches[0]) == 0:
            return

        # use a generator for API consistency:
        matchx = matches[1] + region[0]  # vectorized
        matchy = matches[0] + region[1]
        for x, y in zip(matchx, matchy):
            yield (x, y, needleWidth, needleHeight)
