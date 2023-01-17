import logging
import socket
import sys
from threading import Thread

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import settings

PORT = settings.get_int("livesplit_smb3manip_port", fallback=25345)
MAX_STALE_FRAMES = settings.get_int("livesplit_smb3manip_max_stale_frames", fallback=3)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_packet(current_frame, lag_frames):
    current_frame = max(round(current_frame), 0)
    payload = current_frame.to_bytes(4, sys.byteorder) + lag_frames.to_bytes(
        2, sys.byteorder
    )
    sock.sendto(payload, ("127.0.0.1", PORT))


class LivesplitSmb3Manip:
    def __init__(self):
        self.target_stale_frames_update = 0

    def reset(self):
        self.lag_frames = 0
        self.target_stale_frames_update = 0

    def tick(self, state: State, current_frame: int):
        if self.target_stale_frames_update <= current_frame:
            lag_frames = (
                state.total_observed_lag_frames + state.total_observed_load_frames
            )
            thread = Thread(target=send_packet, args=(current_frame, lag_frames))
            thread.start()
            thread.join()
            self.target_stale_frames_update = current_frame + MAX_STALE_FRAMES
            logging.debug(
                f"Emitted livesplit.smb3manip packet at frame {current_frame}"
            )
