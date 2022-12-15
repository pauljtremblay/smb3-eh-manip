import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.nohands import NoHands


class TestNoHands(unittest.TestCase):
    def test_window_162665(self):
        lsfr = LSFR([81, 237, 78, 148, 9, 33, 51, 113, 23])
        nohands = NoHands()
        optimal_frame_offset = nohands.calculate_optimal_window(lsfr)
        self.assertEqual(226, optimal_frame_offset.action_frame)
        self.assertEqual(2, optimal_frame_offset.window)
