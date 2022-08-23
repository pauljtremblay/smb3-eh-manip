import unittest
from smb3_eh_manip import logging


class TestLogging(unittest.TestCase):
    def test_initialize_logging(self):
        logging.initialize_logging()
