import unittest

from smb3_eh_manip.app.nohands import NoHands


class TestNoHands(unittest.TestCase):
    def test_pop_first_level(self):
        nohands = NoHands()
        nohands.tick(12)
        nohands.tick(63)
        self.assertEqual(2, nohands.current_section)
