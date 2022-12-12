from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, FacingDirection, HammerBro, World

BRO_MOVEMENT_FRAMES = 32  # it takes 32 frames for a HB to make 1 movement
LEVEL_FACE_TO_MOVE_FRAMES = 39
FORT_FACE_TO_MOVE_FRAMES = 102


def validate_direction(world, direction, hb):
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
    return world.get_position(hb.x + target_x, hb.y + target_y)


def calculate_facing_direction(
    facing_lsfr: LSFR, world: World, hb: HammerBro, level_face_to_move_frames: int
):
    lsfr = facing_lsfr.clone()
    facing = lsfr.random_n(hb.index) & 0x3
    lsfr.next_n(level_face_to_move_frames)
    tries = 4
    direction = lsfr.random_n(hb.index) & 0x3  # 0=right, 1=left, 2-down, 3=up
    increment = 1 if (lsfr.random_n(hb.index) & 0x80) else -1
    while tries > 0:
        direction += increment
        direction &= 3
        if (facing ^ direction) == 1:
            continue
        tries -= 1
        if tries == 0:
            direction = facing ^ 1
        if not validate_direction(world, direction, hb):
            continue
        break
    return FacingDirection(Direction(facing), Direction(direction))
