import logging
import sys
import time

import cv2
import numpy as np

from smb3_eh_manip.util import settings
from smb3_eh_manip.app.servers.fceux_lua_server import *
from smb3_eh_manip.app.servers.retrospy_server import RetroSpyServer
from smb3_eh_manip.ui.audio_player import AudioPlayer
from smb3_eh_manip.ui.ui_player import UiPlayer
from smb3_eh_manip.ui.video_player import VideoPlayer

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
        self.auto_detect_lag_frames_video = settings.get_boolean(
            "auto_detect_lag_frames_video"
        )
        self.auto_detect_lag_frames_retrospy = settings.get_boolean(
            "auto_detect_lag_frames_retrospy"
        )
        self.enable_auto_detect_lag_frame_ui = settings.get_boolean(
            "enable_auto_detect_lag_frame_ui"
        )
        self.enable_fceux_tas_start = settings.get_boolean(
            "enable_fceux_tas_start", fallback=False
        )
        self.write_capture_video = settings.get_boolean(
            "write_capture_video", fallback=False
        )
        self.enable_video_player = settings.get_boolean("enable_video_player")
        self.enable_audio_player = settings.get_boolean("enable_audio_player")
        self.enable_ui_player = settings.get_boolean("enable_ui_player")
        self.track_end_stage_clear_text_time = settings.get_boolean(
            "track_end_stage_clear_text_time", fallback=False
        )
        self.offset_ewma_read_frame = settings.get_boolean(
            "offset_ewma_read_frame", fallback=False
        )
        self.playing = False
        self.current_time = -1
        self.start_time = -1
        self.ewma_tick = 0
        self.ewma_read_frame = 0
        self.lag_frames = 0
        self.lag_frames_default = 0

        if self.auto_detect_lag_frames_video:
            self.auto_detect_lag_frame_windows = settings.get_frame_windows(
                "auto_detect_lag_frame_windows", fallback="2500-2725"
            )
            self.last_frame_sliced = None

        if self.auto_detect_lag_frames_retrospy:
            self.retrospy_server = RetroSpyServer()

        if self.track_end_stage_clear_text_time:
            self.last_clear_sighting_time = -1
            self.end_stage_clear_text_template = cv2.imread(
                settings.get(
                    "end_stage_clear_text_path", fallback="data/endStageClearText.png"
                )
            )
        self.reset_template = cv2.imread(
            settings.get("reset_image_path", fallback="data/reset.png")
        )
        self.template = cv2.imread(self.start_frame_image_path)
        self.capture = cv2.VideoCapture(settings.get_int("video_capture_source"))
        if not self.capture.isOpened():
            logging.info("Cannot open camera")
            sys.exit()
        if self.write_capture_video:
            path = settings.get("write_capture_video_path", fallback="capture.avi")
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

    def tick(self, last_tick_duration):
        start_read_frame = time.time()
        ret, frame = self.capture.read()
        read_frame_duration = time.time() - start_read_frame
        logging.debug(f"Took {read_frame_duration}s to read frame")
        self.ewma_tick = self.ewma_tick * 0.95 + last_tick_duration * 0.05
        self.ewma_read_frame = self.ewma_read_frame * 0.95 + read_frame_duration * 0.05
        if not ret:
            logging.warning("Can't receive frame (stream end?). Exiting ...")
            sys.exit()
        if self.write_capture_video:
            self.output_video.write(frame)
        if self.playing:
            self.update_times()
        self.check_and_update_end_stage(frame)
        self.check_and_update_autoreset(frame)
        self.check_and_update_begin_playing(frame)
        self.check_and_update_lag_frames(frame)
        if self.show_capture_video:
            cv2.imshow("capture", frame)
        if self.enable_audio_player and self.playing:
            self.audio_player.tick(self.current_frame - self.lag_frames)
        if self.enable_ui_player and self.playing:
            self.ui_player.tick(
                self.current_frame - self.lag_frames,
                self.ewma_tick,
                self.ewma_read_frame,
                self.lag_frames,
            )
        key = cv2.waitKey(1)
        if key == ord("l"):
            self.lag_frames += 1
            self.lag_frames_default += 1
            logging.info(f"Lag frame default incremented to {self.lag_frames_default}")
        elif key == ord("k"):
            self.lag_frames -= 1
            self.lag_frames_default -= 1
            logging.info(f"Lag frame default decremented to {self.lag_frames_default}")

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
            self.lag_frames = self.lag_frames_default
            if self.enable_video_player:
                self.video_player.reset()
            if self.enable_fceux_tas_start:
                emu.pause()
                latency_offset = round(self.latency_ms / settings.NES_MS_PER_FRAME)
                taseditor.setplayback(self.video_offset_frames + latency_offset)
            if self.auto_detect_lag_frames_retrospy:
                self.retrospy_server.reset()
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

    def check_and_update_lag_frames(self, frame):
        if self.auto_detect_lag_frames_retrospy:
            lag_frame_detect_start = time.time()
            self.retrospy_server.tick()
            self.lag_frames = self.retrospy_server.lag_frames_observed
            detect_duration = time.time() - lag_frame_detect_start
            if self.playing and detect_duration > 0.002:
                logging.info(f"Took {detect_duration}s detecting lag frames")
        if self.auto_detect_lag_frames_video and self.playing:
            for frame_window in self.auto_detect_lag_frame_windows:
                if (
                    self.current_frame >= frame_window[0]
                    and self.current_frame <= frame_window[1]
                ):
                    # i dont want to compare the entire frame, since even for lag
                    # frames they can change. let's remove a 100px border.
                    current_frame_sliced = frame[100:-100, 100:-100]
                    if (self.last_frame_sliced == current_frame_sliced).all():
                        self.lag_frames += 1
                        logging.info(f"Detected lag frame, total {self.lag_frames}")
                        if self.enable_auto_detect_lag_frame_ui:
                            cv2.imshow("last lag frame", current_frame_sliced)
                    self.last_frame_sliced = current_frame_sliced

                    if self.enable_auto_detect_lag_frame_ui:
                        cv2.imshow("lag frame ui", current_frame_sliced)

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
        ewma_read_frame_net = (
            -self.ewma_read_frame if self.offset_ewma_read_frame else 0
        )
        self.current_frame = self.video_offset_frames + round(
            (ewma_read_frame_net + self.latency_ms + self.current_time * 1000)
            / settings.NES_MS_PER_FRAME,
            1,
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
        confidence=float(settings.get("confidence", fallback=0.95)),
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
