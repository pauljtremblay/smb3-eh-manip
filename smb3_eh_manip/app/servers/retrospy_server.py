import logging
import socket
import time
from multiprocessing import Process, Value
from signal import signal, SIGINT

from smb3_eh_manip.util import events, settings
from smb3_eh_manip.util.logging import initialize_logging

PORT = 47569
LOAD_FRAME_THRESHOLD = 3  # anything higher than this number is considered a load frame instead of lag frame
SOCKET_TIMEOUT = 10
LATENCY_FRAMES_RETROSPY = settings.get_int("latency_frames_retrospy", fallback=0)


def handler(_signum, _frame):
    global running
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    running = False


def retrospy_server_process(lag_frames_observed, load_frames_observed):
    initialize_logging(console_log_level="DEBUG", filename="restrospy_server.log")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", PORT))
    while True:
        data = sock.recv(1024)
        if len(data) != 2:
            logging.debug(f"Data frame not sized properly {len(data)}")
            continue
        timestamp_diff = (data[-1] << 8) + data[-2]
        packet_lag_frames = int((timestamp_diff + 2) / settings.NES_MS_PER_FRAME) - 1
        if packet_lag_frames < 0:
            logging.debug(
                f"We think we got {packet_lag_frames} frames, correcting to 0. timestamp_diff: {timestamp_diff}"
            )
            packet_lag_frames = 0
        if packet_lag_frames:
            if packet_lag_frames > LOAD_FRAME_THRESHOLD:
                logging.debug(f"Observed {packet_lag_frames} load frames")
                total = load_frames_observed.value + packet_lag_frames
                with load_frames_observed.get_lock():
                    load_frames_observed.value = total
            else:
                logging.debug(f"Observed {packet_lag_frames} lag frames")
                total = lag_frames_observed.value + packet_lag_frames
                with lag_frames_observed.get_lock():
                    lag_frames_observed.value = total
        time.sleep(0.001)


class RetroSpyServer:
    def __init__(self):
        self.lag_frames_observed_value = Value("i", 0)
        self.lag_frames_observed = 0
        self.load_frames_observed_value = Value("i", 0)
        self.load_frames_observed = 0
        self.retrospy_server_process = Process(
            target=retrospy_server_process,
            args=(
                self.lag_frames_observed_value,
                self.load_frames_observed_value,
            ),
        )
        self.retrospy_server_process.daemon = True
        self.retrospy_server_process.start()

    def tick(self, current_frame=0):
        new_lag_frames_observed = (
            self.lag_frames_observed_value.value - self.lag_frames_observed
        )
        new_load_frames_observed = (
            self.load_frames_observed_value.value - self.load_frames_observed
        )
        self.lag_frames_observed += new_lag_frames_observed
        self.load_frames_observed += new_load_frames_observed
        if new_lag_frames_observed or new_load_frames_observed:
            events.emit(
                self,
                events.LagFramesObserved(
                    current_frame - LATENCY_FRAMES_RETROSPY,
                    new_lag_frames_observed,
                    new_load_frames_observed,
                ),
            )

    def reset(self):
        self.lag_frames_observed = 0
        with self.lag_frames_observed_value.get_lock():
            self.lag_frames_observed_value.value = 0
        self.load_frames_observed = 0
        with self.load_frames_observed_value.get_lock():
            self.load_frames_observed_value.value = 0

    @classmethod
    def input_str_from_packet(kls, packet):
        # nesdev bits ABSTUDLR src:https://www.nesdev.org/wiki/Standard_controller
        # fceux fm2 doc RLDUTSBA (Right, Left, Down, Up, sTart, Select, B, A) src:https://fceux.com/web/FM2.html
        input_str = "." if packet[7] == 0 else "R"
        input_str += "." if packet[6] == 0 else "L"
        input_str += "." if packet[5] == 0 else "D"
        input_str += "." if packet[4] == 0 else "U"
        input_str += "." if packet[3] == 0 else "T"
        input_str += "." if packet[2] == 0 else "S"
        input_str += "." if packet[1] == 0 else "B"
        input_str += "." if packet[0] == 0 else "A"
        return input_str


if __name__ == "__main__":
    global running
    running = True
    signal(SIGINT, handler)
    initialize_logging(
        filename="restrospy_server.log",
        file_log_level="DEBUG",
        console_log_level="DEBUG",
    )
    server = RetroSpyServer()
    while running:
        lag_frame_detect_start = time.time()
        server.tick()
        detect_duration = time.time() - lag_frame_detect_start
        if detect_duration > 0.002:
            logging.info(f"Took {detect_duration}s detecting lag frames")
