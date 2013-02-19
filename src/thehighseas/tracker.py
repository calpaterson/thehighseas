import time

from bencode import bencode, bdecode
from bottle import Bottle, request, response, abort

from constants import (
    tracker_id,
    redis_connection,
    interval
    )
from rootapp import app
from values import Peer, Swarm

def update_peer_info(announcement):
    peer = Peer.from_announcement(announcement, ip=request.remote_addr)
    swarm = Swarm.from_announcement(announcement)
    if "event" in announcement and announcement["event"] == "completed":
        swarm.completed_by(peer)
    elif "event" in announcement and announcement["event"] == "stopped":
        swarm.stopped_by(peer)
    else:
        swarm.update(peer)

def build_listing(announcement):
    swarm = Swarm.from_announcement(announcement)
    listing = swarm.listing()
    listing.update({
            "tracker id": tracker_id,
            "interval": interval
            })
    return bencode(listing)

@app.get("/tracker/scrape")
def scrape():
    try:
        stats = Swarm.from_hex_hash(request.query["infohash"]).stats()
        return bencode(stats)
    except KeyError:
        stats = {}
        for swarm in Swarm.nonsecret():
            stats.update(swam.stats())
        return bencode(stats)

@app.get("/tracker/announce")
def announce():
    announcement = request.query
    update_peer_info(announcement)
    return build_listing(announcement)
