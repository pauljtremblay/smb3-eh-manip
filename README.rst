smb3-eh-manip
==============

.. image:: https://badge.fury.io/py/smb3-eh-manip.png
    :target: https://badge.fury.io/py/smb3-eh-manip

Ingest video data from a capture card to render a smb3 eh TAS

Installation
------------

Note: Ensure python3 is installed

Install this package and dependencies via pip::

    pip install smb3-eh-manip

Running
-------

Copy the config.ini.sample file to the directory you'd like to run
the tool from, and name it config.ini. When calibrating, consider setting
latency_ms to 0, otherwise know the calibration video is offset that
amount.

Note: You must calibrate before eh attempts to set your latency_ms! See
the calibration section, below.

From a cmd prompt, powershell, or terminal with working python3::

    python -m smb3_eh_manip.main

config.ini
----------

In config.ini you'll note several configurable values. These are values
that work for *my* config, with an avermedia capture card. The images and values
might be different, especially for different capture cards.

`*_region` a comma separated list of x,y,width,height the tool uses to locate
the corresponding image within the frame.

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
`latency_is` should be set to 5*16.64=83 in `config.ini`.

Note: I am not convinced this is consistent when running+recording with OBS.
More testing is required. This is extremely important to be consistent, otherwise
this tool is significantly less helpful.

Usage
-----

Set `computer` to `eh` and optionally set `show_capture_video` to `false`.
Run the app. Ensure it is synced with the TAS.

Revel in victory.

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

* Update docs to simplify and make more usable
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
