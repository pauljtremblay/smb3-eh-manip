import logging
import socket
from signal import signal, SIGINT

from smb3_eh_manip.logging import initialize_logging
from smb3_eh_manip.settings import NES_MS_PER_FRAME

TAS_FILENAME = "taspart.fm2"
TAS_FILE_WRITE = False
PORT = 47569
LAG_FRAME_THRESHOLD_PER_TICK = 3


def handler(_signum, _frame):
    global running
    print("SIGINT or CTRL-C detected. Exiting gracefully")
    running = False


class RetroSpyServer:
    def __init__(self):
        self.lag_frames_observed = 0
        if TAS_FILE_WRITE:
            self.f = open(TAS_FILENAME, "wt")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", PORT))

    def tick(self):
        data, _addr = self.sock.recvfrom(1024)
        if len(data) < 26:
            logging.info(f"Data frame not large enough {len(data)}")
            return
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
                self.lag_frames_observed += packet_lag_frames
        input_str = self.input_str_from_packet(data)
        if TAS_FILE_WRITE:
            self.f.write(
                "|0|" + input_str + "||| timestamp_diff=" + str(timestamp_diff) + "\n"
            )

    def reset(self):
        self.lag_frames_observed = 0

    def close(self):
        if TAS_FILE_WRITE:
            self.f.close()
        self.sock.close()

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
        server.tick()
    server.close()
