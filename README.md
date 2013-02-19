The High Seas - a very straightforward bittorrent tracker
===========================================================

The High Seas is an easy to use bittorrent tracker with a very simple
web interface.  It was created with the aim of making it *much easier*
to start a bittorrent tracker.

Features
--------

* No setup whatsoever, just execute ```./thehighseas```
* A bittorrent tracker
  - All tracking is "public" (currently)
  - Scrape API supported
  - "Secret" swarms (see below for details)
* A simple web interface
  - Upload torrent files
  - Download torrent files
  - Check the status of swarms

Getting Started
---------------

### Prerequisites

- Python (version 2.x), with pip and virtualenv
    - On debian/ubuntu these are the packages:
       - ```python2.7```
       - ```python-pip```
       - ```python-virtualenv```
- Redis
    - On debian/ubuntu this is the package:
       - ```redis-server```

### Running

- Execute ```./thehighseas```
- Visit [http://localhost:11235](http://localhost:11235)
- Edit the configuration in ```config.sh``` before you deploy properly

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

Contact
-------

Email me with any questions: cal - AT - calpaterson - DOT - com