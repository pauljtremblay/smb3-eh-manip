"""
This is for manipulating world 3 hammer bro to go down after levels 1 and 2,
ensuring no runaway.

We intend on playing the first sections of 3-1 and 3-2 normally, but coming
out of the exit pipes, we calculate optimal windows in which we can end
the level to move the HB bro down.
"""
from smb3_eh_manip.app import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import World

# This includes stopping under the card and waiting for safety. If there are
# lots of frames, maybe its best to maintain pspeed? the y velocity is at least
# 4px different with pspeed vs without, so gotta pick either full speed or no
# speed IMO. This is safe.
THREE_ONE_SECOND_SECTION_MIN_DURATION = 594
LEVEL_TO_FACE_FRAMES = 17


class W3BroDown:
    def __init__(self):
        self.world = World.load(number=3)
        self.hb = self.world.hbs[1]

    def calculate_3_1_window(self, seed_lsfr: LSFR):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(THREE_ONE_SECOND_SECTION_MIN_DURATION + LEVEL_TO_FACE_FRAMES)
        return hb.calculate_facing_direction(
            lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES
        )
