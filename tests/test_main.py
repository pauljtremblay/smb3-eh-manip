import unittest
from smb3_eh_manip.main import compute


class TestMain(unittest.TestCase):
    def test_compute(self):
        compute()
