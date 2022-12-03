import unittest

from smb3_eh_manip.app.lsfr import LSFR


class TestLSFR(unittest.TestCase):
    def test_next(self):
        lsfr = LSFR()
        for next_expected in [68, 34, 145, 72, 36, 18, 137, 68]:
            self.assertEqual(lsfr.next()[0], next_expected)
