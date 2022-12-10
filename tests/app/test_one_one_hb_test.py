import unittest

from smb3_eh_manip.app.lsfr import LSFR
from smb3_eh_manip.app.models import Direction
from smb3_eh_manip.app.one_one_hb_test import OneOneHBTest


class TestOneOneHBTest(unittest.TestCase):
    def test_left_move(self):
        subject = OneOneHBTest()
        lsfr = LSFR([232, 229, 52, 254, 151, 106, 68, 144, 25])
        self.assertEqual(Direction.LEFT, subject.calculate_next_left_window(lsfr))
