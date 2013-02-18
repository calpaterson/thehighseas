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
    listing = {
        "tracker id": tracker_id,
        "interval": interval,
        "peers": swarm.peers(),
        "downloaded": swarm.times_downloaded(),
        "complete": swarm.number_of_seeds(),
        "incomplete": swarm.number_of_leechers()
        }
    return bencode(listing)

def swarm_stats(info_hash):
    peers = [Peer.from_json(e) for e in redis_connection.hvals(info_hash)]
    stats = {
        "downloaded": 0,
        "complete": 0,
        "incomplete": 0}
    for peer in peers:
        if peer.name() != "-":
            if peer.is_complete():
                stats["complete"] += 1
            else:
                stats["incomplete"] += 1
    return stats

def scrape_stats():
    info_hashes = redis_connection.keys("*.swarm")
    stats = {}
    for info_hash in info_hashes:
        stats[info_hash] = swarm_stats(info_hash)
    return bencode(stats)

@app.get("/tracker/scrape")
def scrape():
    return scrape_stats()

@app.get("/tracker/announce")
def announce():
    announcement = request.query
    update_peer_info(announcement)
    return build_listing(announcement)
