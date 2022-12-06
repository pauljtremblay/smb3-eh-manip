import unittest

from smb3_eh_manip.app.state import State


class TestState(unittest.TestCase):
    def test_pop_first_level(self):
        state = State()
        state.handle_lag_frames_observed(0, 12)
        state.handle_lag_frames_observed(0, 63)
        self.assertEqual("1-1 exit", state.active_section().name)

    def test_lsfr(self):
        state = State()
        state.tick(12)
        self.assertEqual(136, state.lsfr.get(0))
        state.tick(13)
        self.assertEqual(68, state.lsfr.get(0))
        state.tick(16)
        self.assertEqual(72, state.lsfr.get(0))
        state.handle_lag_frames_observed(1, 0)
        state.tick(17)
        self.assertEqual(72, state.lsfr.get(0))
