"""
This is a test class for manipulating HBs. It manips the world 1 HB to move
left after 1-1 depending on when the player enters the level.
"""
from dataclasses import dataclass

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, FacingDirection, World

# from the entering the level, we want to set up some windows in which the HB will move left.

BRO_MOVEMENT_FRAMES = 32  # it takes 32 frames for a HB to make 1 movement
LEVEL_FACE_TO_MOVE_FRAMES = 39
FORT_FACE_TO_MOVE_FRAMES = 102

ONE_ONE_DURATION_FRAMES = 1449  # stop and jump under the end card
ONE_ONE_LEVEL_TO_FACE_FRAMES = 17


class OneOneHBTest:
    def __init__(self):
        self.world = World.load(number=1)
        self.hb = self.world.hbs[0]

    def calculate_next_left_window(self, seed_lsfr: LSFR):
        lsfr = seed_lsfr.clone()
        lsfr.next_n(ONE_ONE_DURATION_FRAMES + ONE_ONE_LEVEL_TO_FACE_FRAMES)
        facing = lsfr.random_n(self.hb.index) & 0x3
        lsfr.next_n(LEVEL_FACE_TO_MOVE_FRAMES)
        tries = 4
        direction = lsfr.random_n(self.hb.index) & 0x3  # 0=right, 1=left, 2-down, 3=up
        increment = 1 if (lsfr.random_n(self.hb.index) & 0x80) else -1
        while tries > 0:
            direction += increment
            direction &= 3
            if (facing ^ direction) == 1:
                continue
            tries -= 1
            if tries == 0:
                direction = facing ^ 1
            if not self.validate_direction(direction):
                continue
            break
        self.hb.facing_direction = Direction(direction)
        return FacingDirection(Direction(facing), self.hb.facing_direction)

    def validate_direction(self, direction):
        target_x = 0
        target_y = 0
        if direction == 0:
            target_x += 1
        elif direction == 1:
            target_x -= 1
        elif direction == 2:
            target_y -= 1
        else:
            target_y += 1
        # TODO if there is a position here at all validate it.
        # we can't validate spade card games e.g. but that doesn't apply yet.
        return self.world.get_position(self.hb.x + target_x, self.hb.y + target_y)
