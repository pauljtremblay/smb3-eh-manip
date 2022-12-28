from smb3_eh_manip.app import hb
from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, World

FOUR_ONE_BEFORE_JUMP_MIN_DURATION = 232
FOUR_ONE_AFTER_JUMP_DURATION = 383
FOUR_TWO_BEFORE_JUMP_MIN_DURATION = 245
FOUR_TWO_AFTER_JUMP_DURATION = 479  # 1up fanfare


class W4CloudBroManip:
    def __init__(self):
        self.world = World.load(number=3)
        self.hb = self.world.hbs[0]

    def calculate_4_1_window(self, seed_lsfr: LSFR):
        return hb.calculate_window(
            seed_lsfr,
            FOUR_ONE_BEFORE_JUMP_MIN_DURATION,
            FOUR_ONE_AFTER_JUMP_DURATION,
            Direction.RIGHT,
            self.world,
            self.hb,
        )

    def calculate_4_2_window(self, seed_lsfr: LSFR):
        return hb.calculate_window(
            seed_lsfr,
            FOUR_TWO_BEFORE_JUMP_MIN_DURATION,
            FOUR_TWO_AFTER_JUMP_DURATION,
            Direction.DOWN,
            self.world,
            self.hb,
        )
