import unittest

from smb3_eh_manip.app.lsfr import LSFR


class TestLSFR(unittest.TestCase):
    def test_next(self):
        lsfr = LSFR()
        for next_expected in [68, 34, 145, 72, 36, 18, 137, 68]:
            self.assertEqual(lsfr.next()[0], next_expected)

    def test_clone(self):
        lsfr = LSFR()
        lsfr.next_n(5)
        lsfr_clone = lsfr.clone()
        lsfr_clone.next()
        self.assertNotEqual(lsfr.get(0), lsfr_clone.get(0))
