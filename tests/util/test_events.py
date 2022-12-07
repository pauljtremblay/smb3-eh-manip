import unittest

from smb3_eh_manip.util import events

EVENT_TYPE = "eventtype"


class Receiver:
    def __init__(self):
        self.event = None
        events.listen(EVENT_TYPE, self.handler)

    def handler(self, event=None):
        self.event = event


class TestEvents(unittest.TestCase):
    def test_event(self):
        receiver = Receiver()
        events.emit(EVENT_TYPE, self, {"test": 1})
        self.assertEqual(1, receiver.event["test"])
