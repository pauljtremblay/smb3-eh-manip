import unittest

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import events


class TestState(unittest.TestCase):
    def test_rng_at_frame_120(self):
        state = State()
        state.tick(110)
        state.tick(120)
        self.assertEqual(129, state.lsfr.get(0))
        self.assertEqual(102, state.lsfr.get(1))
        self.assertEqual(100, state.lsfr.get(2))
        state.reset()
        state.tick(120)
        self.assertEqual(129, state.lsfr.get(0))
        self.assertEqual(102, state.lsfr.get(1))
        self.assertEqual(100, state.lsfr.get(2))

    def test_trigger_offset2framerngincrement(self):
        state = State()
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 0, 12))
        self.assertEqual("1-1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(2, 0, 63))
        # would be 75, but two frames of rng increment during 1-1 enter, so we
        # trigger offset2framerngincrement and end up with 73
        self.assertEqual(73, state.total_observed_load_frames)

    def test_load_frames_condition(self):
        state = State()
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 0, 12))
        state.handle_lag_frames_observed(events.LagFramesObserved(2, 0, 63))
        state.handle_lag_frames_observed(events.LagFramesObserved(3, 1, 0))
        self.assertEqual("1-1 exit", state.active_section().name)

    def test_frame_completed_condition(self):
        state = State(category_name="warpless")
        state.tick(1)
        self.assertEqual("w1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 1, 12))
        state.tick(100)
        self.assertEqual("1-1 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(100, 1, 63))
        self.assertEqual("w2 airship mid", state.active_section().name)
        state.tick(200)
        self.assertEqual("w2 airship mid", state.active_section().name)
        state.tick(75000)
        self.assertEqual("3-3 enter", state.active_section().name)
        state.handle_lag_frames_observed(events.LagFramesObserved(100, 1, 63))
        state.tick(75001)
        self.assertEqual("5-1 enter", state.active_section().name)
        state.tick(75002)
        self.assertEqual("5-1 enter", state.active_section().name)

    def test_lsfr(self):
        state = State()
        state.tick(12)
        self.assertEqual(136, state.lsfr.get(0))
        state.tick(13)
        self.assertEqual(68, state.lsfr.get(0))
        state.tick(16)
        self.assertEqual(72, state.lsfr.get(0))
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 1, 0))
        state.tick(17)
        self.assertEqual(72, state.lsfr.get(0))
