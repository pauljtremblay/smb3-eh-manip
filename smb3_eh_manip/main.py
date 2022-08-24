import logging
import time
from signal import signal, SIGINT

from smb3_eh_manip.computers.calibration_computer import CalibrationComputer
from smb3_eh_manip.computers.eh_computer import EhComputer
from smb3_eh_manip.computers.eh_vcam_computer import EhVcamComputer
from smb3_eh_manip.computers.two_one_computer import TwoOneComputer
from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip import settings


def handler(_signum, _frame):
    global computer
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    computer.terminate()
    computer = None


def main():
    global computer
    signal(SIGINT, handler)
    initialize_logging()
    computer_name = settings.get("computer")
    if computer_name == "eh":
        computer = EhComputer()
    elif computer_name == "twoone":
        computer = TwoOneComputer()
    elif computer_name == "eh_vcam":
        computer = EhVcamComputer()
    elif computer_name == "calibration":
        computer = CalibrationComputer()
    else:
        logging.warning(f"Failed to find computer {computer_name}")
    last_tick_duration = -1
    while computer is not None:
        start_time = time.time()
        computer.tick(last_tick_duration)
        last_tick_duration = time.time() - start_time
        logging.debug(f"Took {last_tick_duration}s to tick")


if __name__ == "__main__":
    main()
