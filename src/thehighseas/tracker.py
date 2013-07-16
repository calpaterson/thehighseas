import time

from bencode import bencode, bdecode
from bottle import Bottle, request, response, abort

from constants import (
    tracker_id,
    redis_connection,
    interval
    )
from rootapp import app
from domain import Peer, Swarm

def update_peer_info(announcement, user_agent):
    peer = Peer.from_announcement(announcement, ip=request.remote_addr)
    peer.user_agent = user_agent
    swarm = Swarm.from_announcement(announcement)
    if "event" in announcement and announcement["event"] == "completed":
        swarm.completed_by(peer)
    elif "event" in announcement and announcement["event"] == "stopped":
        swarm.stopped_by(peer)
    else:
        swarm.update(peer)

@app.get("/tracker/scrape")
def scrape():
    try:
        stats = Swarm.from_hex_hash(request.query["infohash"]).stats()
        return bencode(stats)
    except KeyError:
        stats = {}
        for swarm in Swarm.nonsecret():
            stats.update(swarm.stats())
        return bencode(stats)

@app.get("/tracker/announce")
def announce():
    announcement = request.query
    swarm = Swarm.from_announcement(announcement)

    update_peer_info(announcement, request.headers.get("User-Agent", None))

    listing = swarm.listing(
        number_of_peers=int(request.query.get("numwant", 50)))
    listing.update({
            "tracker id": tracker_id,
            "interval": interval
            })
    return bencode(listing)
