"""
Helper class for eventing. Currently unused.
"""
from enum import Enum
import logging

from pydispatch import dispatcher


class EventType(Enum):
    ADD_ACTION_FRAME = 1


def listen(event_type, callback, **kwargs):
    # Listen to all events with event_type
    dispatcher.connect(callback, signal=event_type, **kwargs)


def emit(event_type, sender, event, **kwargs):
    # Emit an event with the given event_type
    logging.info(f"Emitting {event_type} event: {event}")
    dispatcher.send(event_type, sender, event=event, **kwargs)
