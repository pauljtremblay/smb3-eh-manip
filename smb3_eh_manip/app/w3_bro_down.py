"""
This is for manipulating world 3 hammer bro to go down after levels 1 and 2,
ensuring no runaway.

We intend on playing the first sections of 3-1 and 3-2 normally, but coming
out of the exit pipes, we calculate optimal windows in which we can end
the level to move the HB bro down.
"""
from smb3_eh_manip.app import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, Window, World
from smb3_eh_manip.util import settings

# This includes stopping under the card and waiting for safety. If there are
# lots of frames, maybe its best to maintain pspeed? the y velocity is at least
# 4px different with pspeed vs without, so gotta pick either full speed or no
# speed IMO. This is safe.
THREE_ONE_SECOND_SECTION_BEFORE_JUMP_MIN_DURATION = 209
THREE_ONE_SECOND_SECTION_AFTER_JUMP_MIN_DURATION = 389
TRANSITION_WAIT_DURATION = settings.get_int("transition_wait_duration", fallback=80)
LEVEL_TO_FACE_FRAMES = 17
DEFAULT_MAX_WAIT_FRAMES = settings.get_int("w3brodown_max_wait_frames", fallback=60)


class W3BroDown:
    def __init__(self):
        self.world = World.load(number=3)
        self.hb = self.world.hbs[1]

    def calculate_3_1_window(
        self, seed_lsfr: LSFR, target_window=2, max_wait_frames=DEFAULT_MAX_WAIT_FRAMES
    ):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(
            THREE_ONE_SECOND_SECTION_BEFORE_JUMP_MIN_DURATION
            - TRANSITION_WAIT_DURATION
            + THREE_ONE_SECOND_SECTION_AFTER_JUMP_MIN_DURATION
            + LEVEL_TO_FACE_FRAMES
        )
        offset = 0
        current_window = 0
        max_window = None
        while offset < max_wait_frames:
            direction = hb.calculate_facing_direction(
                lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES
            ).direction
            if direction == Direction.DOWN:
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
