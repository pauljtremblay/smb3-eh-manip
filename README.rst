smb3-eh-manip
==============

.. image:: https://badge.fury.io/py/smb3-eh-manip.png
    :target: https://badge.fury.io/py/smb3-eh-manip

.. image:: https://ci.appveyor.com/api/projects/status/github/narfman0/smb3-eh-manip?branch=main
    :target: https://ci.appveyor.com/project/narfman0/smb3-eh-manip

Ingest video data from a capture card to render a smb3 eh TAS

Installation
------------

Navigate to the most recent versioned release here:

https://github.com/narfman0/smb3-eh-manip/tags

Download the zip and extract to your favorite directory.

Quick Start
-----------

Copy the config.ini.sample file config.ini.

There are two methods to configure the tool, using video capture
card and/or using a retrospy/arduino.

Note: you can use video capture to detect reset/start and use
arduino to detect lag frames.

`Video Capture Configuration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/video_capture_configuration.md>`_

`Retrospy/arduino Configuration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/arduino_configuration.md>`_

Calibrating latency_ms is critical. There is some delay between game start
and when the tool thinks the game started, so we need to account for that.

`Calibration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/calibration.md>`_

Notes
-----

We need to maintain score to avoid or incur lag frames. The current TAS
skips lag frames in 2-1 and 2f but gets them in 2-2. So make sure your score
IS past the threshold in 2-2.

1-Airship is all about setting yourself up for
success at the end of 2-1. So get any of the following:
65660 before 243 firekill, bonk strats for EZ 243
65610 before 244 firekill
65560 before 245 firekill, fast strat
2-1: Skip the final goomba in 2-1 if you are ahead, or kill the extra pirahnas if
you are behind for the hundredths place.
2-2: A little hop before the hill helps control the speed variance. Get 2, 3,
or 4 coins for 50 modifications.

.. csv-table:: End level score sum of digits thresholds
    :header: "Level", "Sum Score", "Target Score At End", "Target Notes"

    "1-A", -, 65610, "Before wand grab, 244 firekill"
    "2-1", 29, 80660, "Before end card, have <29"
    "2-2", 23, 95610, "Before end card, have >23"
    "2-f", 17, 110860, "Before bag grab, have <17"

.. csv-table:: Success windows
    :header: "Level", "Start Frame", "Window"

    "2-1", 18046, "[purple]good-good"
    "2-2", 19947, "[purple]good-good-good"
    "2-f", 22669, "good-[purple]bad-good"

TODO
----

* Configuration utility
* livesplit integration (for triggers)

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
