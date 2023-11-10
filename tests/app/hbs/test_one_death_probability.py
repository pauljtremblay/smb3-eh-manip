import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction, World
from smb3_eh_manip.app.hbs import hb


class TestOneDeathProbability(unittest.TestCase):
    def test_hb_move_up_after_2_1(self):
        self.world = World.load(number=2)
        self.hb = self.world.hbs[1]
        
        lsfr = LSFR()
        # roughly, frames to exit 2-1
        lsfr.next_n(4*60*60 + 30*60)

        # over ten seconds, how likely is the hb to move up?
        iterations = 10*60
        desired_movement_count = 0
        for _ in range(iterations):
            if hb.calculate_facing_direction(lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES).direction is Direction.UP:
                desired_movement_count += 1
            lsfr.next()
        self.assert_within(desired_movement_count/iterations)

    def test_hb_move_left_after_2f_first_move(self):
        self.world = World.load(number=2)
        self.hb = self.world.hbs[1]
        self.hb.y = 4 # right of 2-4
        
        lsfr = LSFR()
        # roughly, frames to exit 2-f
        lsfr.next_n(6*60*60)

        # over ten seconds, how likely is the hb to move up?
        iterations = 10*60
        desired_movement_count = 0
        for _ in range(iterations):
            if hb.calculate_facing_direction(lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES).direction is Direction.LEFT:
                desired_movement_count += 1
            lsfr.next()
        self.assert_within(desired_movement_count/iterations)

    def test_hb_move_down_after_2f_second_move(self):
        self.world = World.load(number=2)
        self.hb = self.world.hbs[1]
        self.hb.y = 4 # left of 2-4
        self.hb.x = 7
        
        # remove mushroom house as an option
        mushroom_house_idx = 0
        for position in self.world.positions:
            if position.level and position.level.name == "mushroom house":
                break
            mushroom_house_idx += 1
        self.world.positions.pop(mushroom_house_idx)
        
        lsfr = LSFR()
        # roughly, frames to exit 2-f
        lsfr.next_n(6*60*60+30)

        # over ten seconds, how likely is the hb to move up?
        iterations = 10*60
        desired_movement_count = 0
        for _ in range(iterations):
            if hb.calculate_facing_direction(lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES).direction is Direction.DOWN:
                desired_movement_count += 1
            lsfr.next()
        self.assert_within(desired_movement_count/iterations)

    def test_hb_move_down_after_2f_third_move(self):
        self.world = World.load(number=2)
        self.hb = self.world.hbs[1]
        self.hb.y = 3 # quicksand
        self.hb.x = 7
        
        # remove left of 2-4 as an option, since we just ran from there
        remove_idx = 0
        for position in self.world.positions:
            if position.y == 4 and position.x == 7:
                break
            remove_idx += 1
        self.world.positions.pop(remove_idx)
        
        lsfr = LSFR()
        # roughly, frames to exit 2-f
        lsfr.next_n(6*60*60+60)

        # over ten seconds, how likely is the hb to move up?
        iterations = 10*60
        desired_movement_count = 0
        for _ in range(iterations):
            if hb.calculate_facing_direction(lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES).direction is Direction.LEFT:
                desired_movement_count += 1
            lsfr.next()
        self.assert_within(desired_movement_count/iterations)

    def test_hb_move_down_after_2_3(self):
        self.world = World.load(number=2)
        self.hb = self.world.hbs[1]
        self.hb.y = 3 # between 2-3 and quicksand
        self.hb.x = 6
        
        # remove mushroom house as an option (worlds don't model edges yet)
        mushroom_house_idx = 0
        for position in self.world.positions:
            if position.level and position.level.name == "mushroom house":
                break
            mushroom_house_idx += 1
        self.world.positions.pop(mushroom_house_idx)
        
        lsfr = LSFR()
        # roughly, frames to exit 2-3
        lsfr.next_n(6*60*60+10*60)

        # over ten seconds, how likely is the hb to move up?
        iterations = 10*60
        desired_movement_count = 0
        for _ in range(iterations):
            if hb.calculate_facing_direction(lsfr, self.world, self.hb, hb.LEVEL_FACE_TO_MOVE_FRAMES).direction is Direction.LEFT:
                desired_movement_count += 1
            lsfr.next()
        self.assert_within(desired_movement_count/iterations)

    def assert_within(self, probability, expected=0.5, margin=0.02):
            self.assertLess(probability, expected + margin)
            self.assertGreater(probability, expected- margin)