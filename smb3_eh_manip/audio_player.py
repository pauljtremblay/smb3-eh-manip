import logging

import simpleaudio as sa

from smb3_eh_manip.settings import config, NES_MS_PER_FRAME

ACTION_FRAMES = [270, 1659, 18046, 19947, 22669, 23952]
FREQUENCY = 24
LATENCY_MS = config.getint("app", "latency_ms")


class AudioPlayer:
    def __init__(self, offset_frames):
        self.offset_frames = offset_frames
        self.beep50ms_wave_obj = sa.WaveObject.from_wave_file("data/beep50ms.wav")

    def reset(self, start_time):
        self.start_time = start_time
        self.trigger_frames = []
        for action_frame in ACTION_FRAMES:
            for increment in range(4, -1, -1):
                self.trigger_frames.append(action_frame - increment * FREQUENCY)
        logging.info(f"Audio trigger frames set to {self.trigger_frames}")

    def tick(self, current_time):
        current_nes_frame = self.offset_frames + round(
            (LATENCY_MS + (current_time - self.start_time) * 1000) / NES_MS_PER_FRAME
        )
        if self.trigger_frames and self.trigger_frames[0] <= current_nes_frame:
            logging.info(f"Beeped at {current_nes_frame}")
            self.beep50ms_wave_obj.play()
            self.trigger_frames.pop(0)