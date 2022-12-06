import unittest

from smb3_eh_manip.app.state import State


class TestState(unittest.TestCase):
    def test_pop_first_level(self):
        nohands = State()
        nohands.handle_lag_frames_observed(0, 12)
        nohands.handle_lag_frames_observed(0, 63)
        self.assertEqual("1-1 exit", nohands.active_section()["name"])
