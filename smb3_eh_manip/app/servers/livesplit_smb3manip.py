import logging
import socket
import sys
from threading import Thread
from enum import Enum

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import settings

"""
When using the manip tool, theres a big stinkin' UI that is helpful to put in
OBS, but too big imo. A livesplit component has been created:
https://github.com/narfman0/LiveSplit.Smb3Manip/releases

This module emits packets the component needs to render, like when we reset
and when lag frames are encountered.
"""

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
        self.emit_message(PacketType.START_TIME_UPDATED, payload)
        logging.debug(
            f"Emitted livesplit.smb3manip packet offset_start_time {offset_start_time}"
        )

    def tick(self, state: State, current_frame: int):
        lag_frames = state.total_observed_lag_frames + state.total_observed_load_frames
        if self.last_lag_frames != lag_frames:
            self.last_lag_frames = lag_frames
            payload = lag_frames.to_bytes(2, sys.byteorder)
            self.emit_message(PacketType.LAG_FRAMES_UPDATED, payload)
            logging.debug(
                f"Emitted livesplit.smb3manip packet at frame {current_frame}"
            )

    def emit_message(self, packet_type: PacketType, payload: bytes):
        thread = Thread(target=send_packet, args=(packet_type, payload))
        thread.start()
        thread.join()
