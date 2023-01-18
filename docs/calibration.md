Calibration
===========

Calibrating latency_ms is critical. There is some delay between game start
and when the tool thinks the game started, so we need to account for that.

To ensure the tool and the TV are in sync, take a 60fps video with a camera
that includes the tool's current frame and your TV/monitor's video. The
video should include a known frame so you can compare.

Example: I use frame 270, which is in the beginning when Luigi bounces
off Mario, and on frame 270 Mario ducks. If when the tool says 270 Mario
is one frame before ducking, then the tool latency is too high, and should
be lowered about 17ms.

Note: Using a TAS to compare might be helpful.

Note: Each frame is about 16.64 milliseconds. Don't forget every frame you are off multiply
by 16.64.

Note: Using this method I am still usually off about 1.5-2 frames, so I've
*reduced* my latency_ms by about 33, which works for me.

Note: I now reset my computer every day I do runs. I find there's some sort
of drift in latency but a reset helps. Would love to look into this someday.