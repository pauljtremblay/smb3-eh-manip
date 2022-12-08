import unittest

from smb3_eh_manip.app.state import State
from smb3_eh_manip.util import events


class TestState(unittest.TestCase):
    def test_load_frames_condition(self):
        state = State()
        state.handle_lag_frames_observed(events.LagFramesObserved(1, 0, 12))
        state.handle_lag_frames_observed(events.LagFramesObserved(2, 0, 63))
        state.handle_lag_frames_observed(events.LagFramesObserved(3, 1, 0))
        self.assertEqual("1-1 exit", state.active_section().name)

    def test_frame_completed_condition(self):
        state = State(category_name="warpless")
        state.tick(1)
        self.assertEqual("midnavy", state.active_section().name)
        state.tick(2)
        self.assertEqual("midnavy", state.active_section().name)
        state.tick(200000)
        self.assertEqual("8 first pipe enter", state.active_section().name)

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
