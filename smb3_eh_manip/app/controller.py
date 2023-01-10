import logging
import time

from smb3_eh_manip.app.opencv import Opencv
from smb3_eh_manip.app.servers.fceux_lua_server import *
from smb3_eh_manip.app.servers.serial_server import SerialServer
from smb3_eh_manip.app.state import State
from smb3_eh_manip.ui.audio_player import AudioPlayer
from smb3_eh_manip.ui.ui_player import UiPlayer
from smb3_eh_manip.util import settings


class Controller:
    def __init__(self):
        self.latency_ms = settings.get_int("latency_ms")
        self.autoreset = settings.get_boolean("autoreset")
        self.auto_detect_lag_frames_serial = settings.get_boolean(
            "auto_detect_lag_frames_serial"
        )
        self.enable_fceux_tas_start = settings.get_boolean("enable_fceux_tas_start")
        self.enable_audio_player = settings.get_boolean("enable_audio_player")
        self.enable_ui_player = settings.get_boolean("enable_ui_player")
        self.offset_frames = settings.get_int("offset_frames", fallback=106)
        self.playing = False
        self.current_time = -1
        self.current_frame = -1
        self.start_time = -1
        self.ewma_tick = 0
        self.state = State()
        self.opencv = Opencv(self.offset_frames)

        if self.auto_detect_lag_frames_serial:
            self.serial_server = SerialServer()
        if self.enable_fceux_tas_start:
            waitForFceuxConnection()
        if self.enable_audio_player:
            self.audio_player = AudioPlayer()
        if self.enable_ui_player:
            self.ui_player = UiPlayer()

    def reset(self):
        self.playing = False
        self.current_frame = -1
        self.state.reset()
        self.opencv.reset()
        if self.enable_fceux_tas_start:
            emu.pause()
            latency_offset = round(self.latency_ms / settings.NES_MS_PER_FRAME)
            taseditor.setplayback(self.offset_frames + latency_offset)
        if self.auto_detect_lag_frames_serial:
            self.serial_server.reset()

    def start_playing(self):
        self.playing = True
        self.start_time = time.time()
        self.current_frame = 0
        self.current_time = 0
        if self.enable_fceux_tas_start:
            emu.unpause()
        self.state.reset()
        if self.auto_detect_lag_frames_serial:
            self.serial_server.reset()
        if self.enable_audio_player:
            self.audio_player.reset()
        if self.enable_ui_player:
            self.ui_player.reset()
        self.opencv.start_playing()

    def terminate(self):
        self.opencv.terminate()

    def tick(self, last_tick_duration):
        self.ewma_tick = self.ewma_tick * 0.95 + last_tick_duration * 0.05
        self.opencv.tick()
        if not self.playing and self.opencv.should_start_playing():
            self.start_playing()
        if self.playing:
            self.update_times()
        self.check_and_update_lag_frames()
        if self.playing:
            self.state.tick(round(self.current_frame))
        if self.enable_audio_player and self.playing:
            self.audio_player.tick(self.current_frame)
        if self.enable_ui_player and self.playing:
            self.ui_player.tick(
                self.current_frame,
                self.ewma_tick,
                self.state,
            )
        if self.playing and self.autoreset and self.opencv.should_autoreset():
            self.reset()
            logging.info(f"Detected reset")

    def check_and_update_lag_frames(self):
        if self.auto_detect_lag_frames_serial:
            lag_frame_detect_start = time.time()
            if self.auto_detect_lag_frames_serial:
                self.serial_server.tick(self.current_frame)
            detect_duration = time.time() - lag_frame_detect_start
            if self.playing and detect_duration > 0.002:
                logging.info(f"Took {detect_duration}s detecting lag frames")

    def update_times(self):
        self.current_time = time.time() - self.start_time
        self.current_frame = self.offset_frames + round(
            (self.latency_ms + self.current_time * 1000) / settings.NES_MS_PER_FRAME,
            1,
        )
