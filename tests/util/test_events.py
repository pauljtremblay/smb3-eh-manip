import unittest

from smb3_eh_manip.util import events


class Receiver:
    def __init__(self):
        self.event = None
        events.listen(events.AddActionFrame, self.handler)

    def handler(self, event: events.AddActionFrame):
        self.event = event


class TestEvents(unittest.TestCase):
    def test_event(self):
        receiver = Receiver()
        events.emit(events.AddActionFrame, self, events.AddActionFrame(1))
        self.assertEqual(1, receiver.event.action_frame)
