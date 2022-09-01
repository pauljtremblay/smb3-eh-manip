import logging
import time
from signal import signal, SIGINT

from pygrabber.dshow_graph import FilterGraph

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


def create_computer():
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


def print_camera_info():
    graph = FilterGraph()
    input_devices = graph.get_input_devices()
    video_capture_source = settings.get_int("video_capture_source")
    if video_capture_source == -1:
        logging.debug("No camera selected, please update to one of the below:")
        logging.debug(input_devices)
        exit()
    logging.debug(f"Selected video source: {input_devices[video_capture_source]}")


def main():
    global computer
    signal(SIGINT, handler)
    initialize_logging()
    print_camera_info()
    try:
        computer = create_computer()
        last_tick_duration = -1
        while computer is not None:
            start_time = time.time()
            computer.tick(last_tick_duration)
            last_tick_duration = time.time() - start_time
            logging.debug(f"Took {last_tick_duration}s to tick")
    except Exception as e:
        logging.error(f"Received fatal error: {e}")
        raise e


if __name__ == "__main__":
    main()
