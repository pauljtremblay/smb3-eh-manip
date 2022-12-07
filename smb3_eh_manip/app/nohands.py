"""
We want to have a manip such that with a second or so upon reaching the map
with the hands, we provide an audio cue where the player only holds left to
go over the hands unscathed with a window of >2 frames (preferably 3).

The time wasted holding left is about 24 frames. The time to wait between
coming out of the pipe and holding left is ideally <30 frames.

This class watches for level changes and times when the hands should occur.
A higher level class should be keeping track of what levels we have beaten.
"""
from smb3_eh_manip.util import events, settings

INTRA_PIPE_DURATION = 197
POST_PIPE_TO_CONTROL_DURATION = 56
# When we go in the pipe before hands, we want to start calculating which
# is a good frame to hold left. This is the minimum time between entering
# the pipe and having control of mario on the overworld, minus pipe
# transition lag frames.
SECTION_TRIGGER_TO_OVERWORLD_CONTROL = (
    INTRA_PIPE_DURATION + POST_PIPE_TO_CONTROL_DURATION
)
# when holding left exiting the pipe, the frame# from origin to specific hand
TO_HAND1_CHECK_FRAME_DURATION = 17
TO_HAND2_CHECK_FRAME_DURATION = 39
TO_HAND3_CHECK_FRAME_DURATION = 16

# How many frames does the window have to be before pressing left?
# 3 is ideal if it happens within a second, otherwise 2 frames likely
LEFT_PRESS_WINDOW = settings.get_int("nohands_left_press_window", fallback=1)
# We cant look 10s in the future, so let's default this as a reasonable
# couple seconds or so.
MAXIMUM_FRAMES_TO_LOOK_FORWARD = settings.get_int(
    "nohands_max_frames_to_look_forward", fallback=120
)

# *: upon using the start/end pipe, identify frame windows in the
# second after exiting the pipe to trigger audio cue
# *: trigger audio cue :D

TRIGGER_SECTION_NAME = settings.get(
    "nohands_trigger_section_name", fallback="8 first pipe enter"
)


class NoHands:
    def section_completed(self, section, seed_lsfr):
        if section.name != TRIGGER_SECTION_NAME:
            return
        lsfr = seed_lsfr.clone()
        lsfr.next_n(SECTION_TRIGGER_TO_OVERWORLD_CONTROL)
        current_window = 0
        passed_hands = [0, 0, 0]
        earliest_one_frame_window = None
        earliest_two_frame_window = None
        optimal_frame_offset = None
        for frame_offset in range(MAXIMUM_FRAMES_TO_LOOK_FORWARD):
            lsfr_experiment = lsfr.clone()
            lsfr_experiment.next_n(frame_offset)
            lsfr_experiment.next_n(TO_HAND1_CHECK_FRAME_DURATION)
            if lsfr_experiment.hand_check():
                current_window = 0
                continue
            passed_hands[0] += 1
            lsfr_experiment.next_n(TO_HAND2_CHECK_FRAME_DURATION)
            if lsfr_experiment.hand_check():
                current_window = 0
                continue
            passed_hands[1] += 1
            lsfr_experiment.next_n(TO_HAND3_CHECK_FRAME_DURATION)
            if lsfr_experiment.hand_check():
                current_window = 0
                continue
            passed_hands[2] += 1
            current_window += 1
            candidate_frame_offset = (
                SECTION_TRIGGER_TO_OVERWORLD_CONTROL + frame_offset,
                current_window,
            )
            if current_window == 3:
                # if we have a 3 frame window we definitely use this immediately
                optimal_frame_offset = candidate_frame_offset
                break
            elif earliest_two_frame_window is None and current_window == 2:
                earliest_two_frame_window = candidate_frame_offset
            elif earliest_one_frame_window is None:
                earliest_one_frame_window = candidate_frame_offset
        if not optimal_frame_offset:
            if earliest_two_frame_window:
                optimal_frame_offset = earliest_two_frame_window
            else:
                optimal_frame_offset = earliest_one_frame_window
        events.emit(
            events.EventType.ADD_ACTION_FRAME,
            self,
            {"action_frame": optimal_frame_offset},
        )
        return optimal_frame_offset
