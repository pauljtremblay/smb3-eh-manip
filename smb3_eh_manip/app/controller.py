import logging

from smb3_eh_manip.app.servers.fceux_lua_server import *
from smb3_eh_manip.app.state import State
from smb3_eh_manip.computers.calibration_computer import CalibrationComputer
from smb3_eh_manip.computers.eh_computer import EhComputer
from smb3_eh_manip.computers.eh_vcam_computer import EhVcamComputer
from smb3_eh_manip.computers.two_one_computer import TwoOneComputer
from smb3_eh_manip.util import settings


class Controller:
    def __init__(self):
        self.computer = Controller.create_computer()
        self.state = State()
        # TODO temporary :\
        self.computer.state = self.state

    def reset(self):
        self.computer.reset()
        self.state.reset()

    def terminate(self):
        self.computer.terminate()

    def tick(self, last_tick_duration):
        self.computer.tick(last_tick_duration)
        if self.computer.should_autoreset():
            self.reset()
            logging.info(f"Detected reset")
        if self.computer.playing:
            self.state.tick(self.computer.current_frame)

    @classmethod
    def create_computer(cls):
        computer_name = settings.get("computer")
        if computer_name == "eh":
            return EhComputer()
        elif computer_name == "twoone":
            return TwoOneComputer()
        elif computer_name == "eh_vcam":
            return EhVcamComputer()
        elif computer_name == "calibration":
            return CalibrationComputer()
        else:
            logging.error(f"Failed to find computer {computer_name}")
