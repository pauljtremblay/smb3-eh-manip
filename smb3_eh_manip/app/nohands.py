"""
We want to have a manip such that with a second or so upon reaching the map
with the hands, we provide an audio cue where the player only holds left to
go over the hands unscathed with a window of >2 frames (preferably 3).

The time wasted holding left is about 24 frames. The time to wait between
coming out of the pipe and holding left is ideally <30 frames.

This class watches for level changes and times when the hands should occur.
A higher level class should be keeping track of what levels we have beaten.
"""

# when holding left exiting the pipe, the frame# from origin to specific hand
TO_HAND1_CHECK_FRAME_DURATION = 18
TO_HAND2_CHECK_FRAME_DURATION = 40
TO_HAND3_CHECK_FRAME_DURATION = 17

# step1: reliable method for detecting level/world changes. keep track of this in
# parent class.
# step2: identify this pipe transition - in world 8, the 3rdish area in
# which we see 13 lag frames.
# step3: upon using the start/end pipe, identify frame windows in the
# second after exiting the pipe to trigger audio cue
# step4: trigger audio cue :D


class NoHands:
    def tick(self):
        pass
