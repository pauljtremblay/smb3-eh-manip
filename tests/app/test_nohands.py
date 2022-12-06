import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.state import Section
from smb3_eh_manip.app import nohands as nohands_module


class TestNoHands(unittest.TestCase):
    def test_window_162665(self):
        # this is a particular frame from a tas i made *shrug*
        section = Section(nohands_module.TRIGGER_SECTION_NAME, 60)
        lsfr = LSFR([81, 237, 78, 148, 9, 33, 51, 113, 23])
        nohands = nohands_module.NoHands()
        candidate_frame_offsets = nohands.section_completed(section, lsfr)
        self.assertEqual(13, len(candidate_frame_offsets))
