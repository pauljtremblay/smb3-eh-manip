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

https://github.com/narfman0/smb3-eh-manip/releases

Download the zip and extract to your favorite directory.

Quick Start
-----------

Copy or move config.ini.sample file to config.ini.

There are two methods to configure the tool, using video capture
card and/or using a retrospy/arduino.

Note: you can use video capture to detect reset/start and use
arduino to detect lag frames.

`Video Capture Configuration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/video_capture_configuration.md>`_

`Retrospy/arduino Configuration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/arduino_configuration.md>`_

Calibrating latency_ms is critical. There is some delay between game start
and when the tool thinks the game started, so we need to account for that.

`Calibration <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/calibration.md>`_

`Movements <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/movements.md>`_

`Notes <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/notes.md>`_

`Development <https://github.com/narfman0/smb3-eh-manip/blob/main/docs/development.md>`_

TODO
----

* Verify w3 bro manips
* Configuration utility
* New UI (kivy? not opencv)

License
-------

Copyright (c) 2022 Jon Robison

See LICENSE for details
