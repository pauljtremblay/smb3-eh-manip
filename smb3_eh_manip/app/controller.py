import logging

from smb3_eh_manip.app.opencv_computer import OpencvComputer


class Controller:
    def __init__(self):
        self.computer = OpencvComputer()

    def reset(self):
        self.computer.reset()

    def terminate(self):
        self.computer.terminate()

    def tick(self, last_tick_duration):
        self.computer.tick(last_tick_duration)
        if self.computer.should_autoreset():
            self.reset()
            logging.info(f"Detected reset")
