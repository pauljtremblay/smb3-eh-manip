Video Capture Configuration
===========================

We need to configure a few things minumum:

* video_capture_source
* trigger frame image(s)
* start_frame_image_region
* latency_ms

Setting video_capture_source
----------------------------

We want to write a video of what the tool sees, then copy the trigger
frame(s). First, we need the tool to know which video 
capture source to use, and set video_capture_source in config.ini.

Run the tool. The terminal window that pops up should
say "Selected video source: <your capture card>". Another video window pops
up by default, rendering the same video source. If it doesn't, press ctrl-c
on the terminal window to close it, go to config.ini, and change the
video_capture_source value (add 1). Restart the tool, and follow this
procedure until it is the correct setting.

If you see your capture card in the tool, you win at life! If not,
you cannot continue.

Setting trigger frame image(s) and start_frame_image_region
-----------------------------------------------------------

Now let's overwrite the trigger frame image and
start_frame_image_region. By default the tool writes a capture.avi file
where the tool lives. Open the file in VLC (do not change its size!),
enable advanced controls (so you
can increment frame by frame), and find the image like what is in
data/eh/trigger.png. IIRC it is frame 106. Take a screenshot, crop
the image, and overwrite the current trigger.png. From the same screenshot,
we need to help the tool know where to look for the image. We need
to set the start_frame_image_region. Identify where you copied the image
coordinates within the screenshot and set the region value like:
left_x,top_y,right_x,bottom_y.

Now when you run the tool, and reset your console, it should say
"detected start frame" in the console. Success! This is a big step.

Setting latency_ms
------------------

Now the tool is running but its significantly behind your console.
We want to start the tool proportionally ahead, so we want to measure the
difference. This is done by setting latency_ms. I take a picture
with my phone, and get the frame difference. I commonly get 3-4 frames.
Each frame is 16.64ms, and I eventually set my latency_ms at 34 (which is
between 3 and 4 nes frames). You'll probably have to try a few iterations.

See [calibration](https://github.com/narfman0/smb3-eh-manip/blob/main/docs/calibration.md)
for other details and methods.

Autoreset
---------

Note: Highly recommended is also configuring data/reset.png and reset_image_region,
which is needed to use the autoreset feature. You can mirror the
process for start_frame_image_region to get it. Autoreset is really
handy and makes the tool shine.

Configure Regions
-----------------

The tools looks for specific images in the frame. It can look anywhere,
however, this is computationally expensive and should be avoided.

By manually setting the region the tool should use to look for the
trigger, we greatly reduce the cpu load, commonly as much as 95%.