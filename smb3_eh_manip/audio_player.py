import logging
import time
from multiprocessing import Process, Value

import simpleaudio as sa

from smb3_eh_manip import settings
from smb3_eh_manip.settings import ACTION_FRAMES, FREQUENCY

DEFAULT_AUDIO_CUE_PATH = "data/audio_cue.wav"


def play_beep(play):
    audio_cue_path = settings.get("audio_cue_path", fallback=DEFAULT_AUDIO_CUE_PATH)
    beep_wave_obj = sa.WaveObject.from_wave_file(audio_cue_path)
    while True:
        if play.value == 1:
            play.value = 0
            beep_wave_obj.play()
        else:
            time.sleep(0.001)


class AudioPlayer:
    def __init__(self):
        self.play = Value("i", 0)
        self.play_process = Process(target=play_beep, args=(self.play,)).start()

    def reset(self):
        self.play.value = 0
        self.trigger_frames = []
        for action_frame in ACTION_FRAMES:
            for increment in range(4, -1, -1):
                self.trigger_frames.append(action_frame - increment * FREQUENCY)
        logging.info(f"Audio trigger frames set to {self.trigger_frames}")

    def tick(self, current_frame):
        if self.trigger_frames and self.trigger_frames[0] <= current_frame:
            self.play.value = 1
            self.trigger_frames.pop(0)
