The High Seas - an ultra straightforward bittorrent tracker
===========================================================

The High Seas is an easy to use bittorrent tracker with a simple web interface.
It is also fast.

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

* Python2, with pip and virtualenv
* Redis

### Running

- Execute ```./thehighseas```
- Visit [http://localhost:11235](http://localhost:11235)

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