Calibration
===========

Calibrating latency_ms is critical. There is some delay between game start
and when the tool thinks the game started, so we need to account for that.

Camera Method
-------------

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

Tool method
-----------

There are two ways to practice and test latency. These both require opencv
configuration at this time.

### Input latency tester

The first is the input latency tester. This compares the time between the player
pressing 'a' in the beginning of 1-1 and many generated action frames.

To enable the tester, in config.ini set `enable_input_latency_tester = true`. You
will also need to update the trigger frame the tool uses to identify if mario
is jumping: data/input_latency_tester/trigger.png. There is a region to
configure as well.

After configuration, when running, go to 1-1 as quickly as possible.
Several action frames have been added, and the runner should try to jump as
closely to the action frames as possible. The tool will see when mario jumps,
and report back to the runner the delay. This DOES take into account the 2 frame
delay before seeing mario jump, so this is purely your reaction time. Ideally,
you can get this to 0, but practically mine is around 1.5 or so, meaning,
1.6 frames (27ms) pass between the audio cue and me jumping.

### Video latency tester

Second is the video latency tester. This identifies the lag between when the
user perception of the video and the tools perception of the video.

To enable the tester, in config.ini set `enable_video_latency_tester = true`. You
will also need to update the trigger frame the tool uses to identify if mario
is jumping: data/video_latency_tester/trigger.png. There is a region to
configure as well.

After configuration, when running, the first action frame in your settings
will be a key action frame. On that frame, the runner should press 'start',
at which point the tool looks at how different the timing is between when it
thinks the game started and when it sees the user pressing start. From there,
it gives the user a latency. Do this several times to get an average/median.

### Final latency_ms

Since that does not account for the user's input latency, subtract as such:
`latency_ms = video_latency_tester_value - input_latency_tester_value`

Example:
Given: My video_latency_tester_value is 27, meaning I very reliably press
a 1.6 frames (27ms) after the audio cue. (Anywhere 0-16 is frame perfect).
My `input_latency_tester_value` is similar at 1.8 frames ~30ms. 
Then: my latency_ms should be at least initially set to 30ms-27ms=3ms.
Thus: `latency_ms=3` for this situation.

Of course live tweaks are always helpful but since the y subpixel impacts
2-1 so severely by changing how many frames it takes to jump to the card,
one should be slow to change the value and only after many data points
consider it.

That said, anecdotally, I have changed latency_ms during stream since I
believe there is capture card latency drift while playing. Further research
is needed in this area.