smb3-eh-manip
==============

.. image:: https://badge.fury.io/py/smb3-eh-manip.png
    :target: https://badge.fury.io/py/smb3-eh-manip

.. image:: https://travis-ci.org/narfman0/smb3-eh-manip.png?branch=master
    :target: https://travis-ci.org/narfman0/smb3-eh-manip

Ingest video data to render smb3 eh manip stimuli

Installation
------------

Install via pip::

    pip install smb3-eh-manip

Development
-----------

Run test suite to ensure everything works::

    make test

Release
-------

To publish your plugin to pypi, sdist and wheels are registered, created and uploaded with::

    make release-test

For test. After ensuring the package works, run the prod target and win::

    make release-prod

License
-------

Copyright (c) 2021 Jon Robison

See LICENSE for details
