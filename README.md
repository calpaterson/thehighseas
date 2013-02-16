The High Seas - an ultra straightforward bittorrent tracker
===========================================================

The High Seas is a very simple and straightforward bittorrent tracker
designed to get you up and running with the minimum of fuss.

Features
--------

* No setup whatsoever, just execute ```thehighseas```
* A bittorrent tracker
  - All tracking is "public" (currently)
  - Scrape API supported
  - "Secret" swarms
    - See below
* A simple web interface
  - Upload torrent files
  - Download torrent files
  - Check the status of swarms

"Secret" swarms
---------------

Most of the time, to start tracking a new swarm, you upload a "metainfo" file
(a ".torrent" file) to the tracker.  This file contains general information
about the files the swarm is sharing, their sizes, their names and checksums
for the files.  The tracker then hosts this metainfo file so that anyone can
join the swarm and start sharing the files.

This is fine for when you want anyone to be able to join a swarm.  Sometimes,
though, files are private.

In this case, you don't need to upload the metainfo file to THS.  Just start
sharing - THS will track any swarm that announces to it.  You'll need to
distribute the metainfo file yourself though.

Getting Started
---------------

### Prerequisites

* Python2, with pip and virtualenv
* Redis

### Running

Execute ./thehighseas

THS does not detach from the terminal.  Closing the terminal or hitting ^C
("ctrl-c") will shutdown THS.  If you want to run THS on a permanent basis,
consider using a [process
supervisor](http://en.wikipedia.org/wiki/Process_supervision), such as:

* [Upstart](http://upstart.ubuntu.com/)
* [Runit](http://mmonit.com/monit/)
* [Monit](http://smarden.org/runit/)