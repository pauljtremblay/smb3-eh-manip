import logging
import socket
import sys
from threading import Thread
from enum import Enum

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import settings

EPOCH_OFFSET = 1673989120228  # TODO i dont want to pass 8 bytes so subtracting this ehre and adding on other side
PORT = settings.get_int("livesplit_smb3manip_port", fallback=25345)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class PacketType(Enum):
    INVALID = 0
    START_TIME_UPDATED = 1
    LAG_FRAMES_UPDATED = 2


def send_packet(packet_type: PacketType, payload: bytes):
    sock.sendto(
        packet_type.value.to_bytes(2, sys.byteorder) + payload, ("127.0.0.1", PORT)
    )


class LivesplitSmb3Manip:
    def __init__(self):
        self.last_lag_frames = 0

    def reset(self):
        self.last_lag_frames = 0

    def start_playing(self, offset_start_time: int):
        payload = (offset_start_time - EPOCH_OFFSET).to_bytes(4, sys.byteorder)
        thread = Thread(
            target=send_packet, args=(PacketType.START_TIME_UPDATED, payload)
        )
        thread.start()
        thread.join()

    def tick(self, state: State, current_frame: int):
        lag_frames = state.total_observed_lag_frames + state.total_observed_load_frames
        if self.last_lag_frames != lag_frames:
            self.last_lag_frames = lag_frames
            payload = lag_frames.to_bytes(2, sys.byteorder)
            thread = Thread(
                target=send_packet, args=(PacketType.LAG_FRAMES_UPDATED, payload)
            )
            thread.start()
            thread.join()
            logging.debug(
                f"Emitted livesplit.smb3manip packet at frame {current_frame}"
            )
