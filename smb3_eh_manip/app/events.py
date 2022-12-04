"""
Helper class for eventing. Currently unused.
"""
from enum import Enum

from pydispatch import dispatcher


class EventType(Enum):
    LEVEL_COMPLETED = 1
    LEVEL_STARTED = 2


def listen(event_type, callback, **kwargs):
    # Listen to all events with event_type
    dispatcher.connect(callback, signal=event_type, **kwargs)


def emit(event_type, sender, payload, **kwargs):
    # Emit an event with the given event_type
    dispatcher.send(event_type, sender, payload=payload, **kwargs)
