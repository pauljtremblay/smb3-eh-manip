from smb3_eh_manip.app import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, Window, World
from smb3_eh_manip.util import settings

SECOND_SECTION_BEFORE_JUMP_MIN_DURATION = 209
SECOND_SECTION_AFTER_JUMP_MIN_DURATION = 389
TRANSITION_WAIT_DURATION = settings.get_int("transition_wait_duration", fallback=80)
LEVEL_TO_FACE_FRAMES = 17
DEFAULT_MAX_WAIT_FRAMES = settings.get_int(
    "w4cloudbromanip_max_wait_frames", fallback=60
)


class W4CloudBroManip:
    def __init__(self):
        self.world = World.load(number=3)
        self.hb = self.world.hbs[0]

    def calculate_4_1_window(
        self, seed_lsfr: LSFR, target_window=2, max_wait_frames=DEFAULT_MAX_WAIT_FRAMES
    ):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(
            SECOND_SECTION_BEFORE_JUMP_MIN_DURATION
            - TRANSITION_WAIT_DURATION
            + SECOND_SECTION_AFTER_JUMP_MIN_DURATION
            + LEVEL_TO_FACE_FRAMES
        )
        offset = 0
        current_window = 0
        max_window = None
        while offset < max_wait_frames:
            direction = hb.calculate_facing_direction(
                lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES
            ).direction
            if direction == Direction.RIGHT:
                current_window += 1
                if max_window is None or max_window.window < current_window:
                    max_window = Window.create_centered_window(offset, current_window)
                    if current_window == target_window:
                        return max_window
            else:
                current_window = 0
            offset += 1
            lsfr.next()
        return max_window
