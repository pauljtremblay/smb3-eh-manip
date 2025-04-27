"""
Helper class for eventing. Currently unused.
"""
from dataclasses import asdict, dataclass
import logging

from pydispatch import dispatcher

from smb3_eh_manip.util import settings

LOGGER = logging.getLogger(__name__)
log_at_level: int = logging.INFO if settings.get_boolean("event_logging_verbose") else logging.DEBUG


@dataclass
class LagFramesObserved:
    current_frame: float
    observed_lag_frames: int
    observed_load_frames: int


@dataclass
class AddActionFrame:
    action_frame: int
    window: int


@dataclass
class LivesplitCurrentSplitIndexChanged:
    current_split_index: int
    last_split_index: int


def listen(event_type, callback, **kwargs):
    # Listen to all events with event_type
    dispatcher.connect(callback, signal=event_type, **kwargs)


def emit(sender, event, **kwargs):
    # Emit an event with the given event_type
    LOGGER.log(log_at_level, "Emitting %s event: %s", type(event).__name__, asdict(event))
    dispatcher.send(type(event), sender, event=event, **kwargs)
