from asyncio.log import logger
from signal import signal, SIGINT

from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip.settings import config
from smb3_eh_manip.computers import (
    EhComputer,
    EhVcamComputer,
    CalibrationComputer,
    TwoOneComputer,
)


def handler(_signum, _frame):
    global computer
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    computer.terminate()
    computer = None


def main():
    global computer
    initialize_logging()
    computer_name = config.get("app", "computer")
    if computer_name == "eh":
        computer = EhComputer()
    elif computer_name == "twoone":
        computer = TwoOneComputer()
    elif computer_name == "eh_vcam":
        computer = EhVcamComputer()
    elif computer_name == "calibration":
        computer = CalibrationComputer()
    else:
        logger.warn(f"Failed to find computer {computer_name}")
    while computer is not None:
        computer.tick()


if __name__ == "__main__":
    signal(SIGINT, handler)
    main()