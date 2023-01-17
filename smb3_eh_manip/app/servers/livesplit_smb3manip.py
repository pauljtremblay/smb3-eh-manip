import logging
import socket
from threading import Thread

from smb3_eh_manip.util import events, settings

PORT = settings.get_int("livesplit_smb3manip_port", fallback=25345)
MAX_STALE_FRAMES = settings.get_int("livesplit_smb3manip_max_stale_frames", fallback=10)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_packet(current_frame):
    sock.sendto(bytes(str(round(current_frame)), "utf-8"), ("127.0.0.1", PORT))


class LivesplitSmb3Manip:
    def __init__(self):
        self.lag_frames = 0
        self.dirty = False
        self.target_stale_frames_update = 0
        events.listen(events.LagFramesObserved, self.handle_lag_frames_observed)

    def reset(self):
        self.lag_frames = 0
        self.dirty = True
        self.target_stale_frames_update = 0

    def tick(self, controller):
        if self.dirty or self.target_stale_frames_update <= controller.current_frame:
            thread = Thread(target=send_packet, args=(controller.current_frame,))
            thread.start()
            thread.join()
            self.dirty = False
            self.target_stale_frames_update = (
                controller.current_frame + MAX_STALE_FRAMES
            )
            logging.debug(
                f"Emitted livesplit.smb3manip packet at frame {controller.current_frame}"
            )

    def handle_lag_frames_observed(self, event: events.LagFramesObserved):
        self.lag_frames += event.observed_lag_frames + event.observed_load_frames
        self.target_stale_frames_update = event.current_frame + MAX_STALE_FRAMES
        self.dirty = True
