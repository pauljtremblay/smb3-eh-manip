import logging
import socket
import time
from multiprocessing import Process, Value
from signal import signal, SIGINT

from smb3_eh_manip.util.logging import initialize_logging
from smb3_eh_manip.util.settings import NES_MS_PER_FRAME

PORT = 47569
LAG_FRAME_THRESHOLD_PER_TICK = 3
SOCKET_TIMEOUT = 10


def handler(_signum, _frame):
    global running
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    running = False


def retrospy_server_process(lag_frames_observed):
    initialize_logging()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", PORT))
    while True:
        data = sock.recv(1024)
        if len(data) < 26:
            logging.info(f"Data frame not large enough {len(data)}")
            continue
        if len(data) > 28:
            logging.info(f"Data frame too large {len(data)}")
            continue
        timestamp_diff = (data[-1] << 8) + data[-2]
        packet_lag_frames = int((timestamp_diff + 2) / NES_MS_PER_FRAME) - 1
        if packet_lag_frames < 0:
            logging.info(
                f"We think we got {packet_lag_frames} frames, correcting to 0. timestamp_diff: {timestamp_diff}"
            )
            packet_lag_frames = 0
        if packet_lag_frames:
            if packet_lag_frames > LAG_FRAME_THRESHOLD_PER_TICK:
                logging.info(
                    f"Observed {packet_lag_frames} lag frames, which is greater than the threshold {LAG_FRAME_THRESHOLD_PER_TICK}. Disregarding."
                )
            else:
                logging.info(f"Observed {packet_lag_frames} lag frames")
                total = lag_frames_observed.value + packet_lag_frames
                with lag_frames_observed.get_lock():
                    lag_frames_observed.value = total
        time.sleep(0.001)


class RetroSpyServer:
    def __init__(self):
        self.lag_frames_observed_value = Value("i", 0)
        self.lag_frames_observed = 0
        self.retrospy_server_process = Process(
            target=retrospy_server_process, args=(self.lag_frames_observed_value,)
        ).start()

    def tick(self):
        self.lag_frames_observed = self.lag_frames_observed_value.value

    def reset(self):
        self.lag_frames_observed = 0
        with self.lag_frames_observed_value.get_lock():
            self.lag_frames_observed_value.value = 0

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
    initialize_logging()
    server = RetroSpyServer()
    while running:

        lag_frame_detect_start = time.time()
        server.tick()
        detect_duration = time.time() - lag_frame_detect_start
        if detect_duration > 0.002:
            logging.info(f"Took {detect_duration}s detecting lag frames")
