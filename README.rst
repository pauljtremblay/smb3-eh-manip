smb3-eh-manip
==============

.. image:: https://badge.fury.io/py/smb3-eh-manip.png
    :target: https://badge.fury.io/py/smb3-eh-manip

Ingest video data from a capture card to render a smb3 eh TAS

Installation
------------

Note: Ensure python3 is installed

Download this package and install dependencies via pip::

    pip install -r requirements_test.txt

Quick Start
-----------

We need to configure a few things minumum:

* video_capture_source
* trigger frame image(s)
* eh_start_frame_image_region
* latency_ms

Copy the config.ini.sample file config.ini.

We want to write a video of what the tool sees, then copy the trigger
frame(s). First however, we need the tool to know which video 
capture source to use, and set video_capture_source in config.ini.

Double click run.bat to run the tool. Note the video window output:
if it is anything other than your expected capture card, go to config.ini,
see the video_capture_source value, and change the number until it works.
Mine is 2, but 0-10 could all be reasonable, or even higher
if you have a lot of video capture devices configured.

If you see your capture card in the tool, you win at life! If not,
you cannot continue. Now let's overwrite the trigger frame image and
eh_start_frame_image_region. By default the tool writes a capture.avi file
where the tool lives. Open the file in VLC (do not change its size!),
enable advanced controls (so you
can increment frame by frame), and find the image like what is in
data/eh/trigger.png. IIRC it is frame 106. Take a screenshot, crop
the image, and overwrite the current trigger.png. From the same screenshot,
we need to help the tool know where to look for the image. We need
to set the eh_start_frame_image_region. Identify where you copied the image
coordinates within the screenshot and set the region value like:
left_x,top_y,right_x,bottom_y.

Now when you run the tool, and reset your console, it should say
"detected start frame" in the console. Success! This is a big step.

Now the tool is running but its significantly behind your console.
We want to start the tool proportionally ahead, so we want to measure the
difference. This is done by setting latency_ms. I take a picture
with my phone, and get the frame difference. I commonly get 3-4 frames.
Each frame is 16.64ms, and i eventually set my latency_ms at 60 (which is
between 3 and 4 nes frames). You'll probably have to try a few iterations.

Note: Highly recommended is also configuring reset_image_region,
which is needed to use the autoreset feature. You can mirror the
process for eh_start_frame_image_region to get it. Autoreset is really
handy and makes the tool shine.

Configure Regions
-----------------

The tools looks for specific images in the frame. It can look anywhere,
however, this is computationally expensive and should be avoided.

By manually setting the region the tool should use to look for the
trigger, we greatly reduce the cpu load, commonly as much as 95%.

Calibration
-----------

Players can run the smb3 practice rom which includes in-level frame timer that
increments by one each frame. With `computer` set to `calibration`, run the
tool, run the game, and enter 1-1. The second window running the video should
appear with some perceived latency. Take a picture with the fastest camera
setting, and compare the frame counts.

Example: After starting 1-1, I took about a second to take a picture. The ingame
timer on my tv was 55, and the ingame timer on the TAS was 50. Thus, my
`latency_ms` should be set to 5*16.64=83 in `config.ini`.

Note: I am not convinced this is consistent when running+recording with OBS.
More testing is required. This is extremely important to be consistent, otherwise
this tool is significantly less helpful.

Notes
-----

.. csv-table:: End level score sum of digits maximums
    :header: "Level", "Sum Score", "Target Score At End", "Target Notes"

    "1-A", -, 65610, "Before wand grab, 244 firekill"
    "2-1", 29, 80660, "Before end card"
    "2-2", 23, 95610, "Before end card"
    "2-f", 17, 110860, "Before bag grab"

.. csv-table:: Success windows
    :header: "Level", "Start Frame", "Window"

    "2-1", 18046, "[purple]good-good"
    "2-2", 19947, "[purple]good-good-good"
    "2-f", 22669, "good-[purple]bad-good"

TODO
----

* Develop practice methodology (starting from 2-1, validate if runner ended on correct frame)

Development
-----------

Run test suite to ensure everything works::

    make test

Release
-------

To run tests, publish your plugin to pypi test and prod, sdist and wheels are
registered, created and uploaded with::

    make release

License
-------

Copyright (c) 2022 Jon Robison

See LICENSE for details
