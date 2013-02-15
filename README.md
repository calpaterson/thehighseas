The High Seas - an ultra straightforward bittorrent tracker
===========================================================

The High Seas is a very simple and straightforward bittorrent tracker
designed to get you up and running with the minimum of fuss.

THS also comes with a very simple web interface built in, so you can
upload, download and check the status of swarms.

Requirements
------------

* Redis
* Python2, with pip and virtualenv

Building
--------

Run ./build.sh

This will download and build everything you need to get started.

Running
-------

Run ./run.sh

This script does not detach from the terminal.  Closing the terminal
or hitting ^C ("ctrl-c") will shutdown THS.  If you want to run THS on
a permanent basis, consider using a [process
supervisor](http://en.wikipedia.org/wiki/Process_supervision), such as:

* Upstart
* Runit
* Monit