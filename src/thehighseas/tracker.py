import time

from bencode import bencode, bdecode
from bottle import Bottle, request, response, abort

from constants import (
    tracker_id,
    redis_connection,
    interval
    )
from values import Peer

app = Bottle()

def update_peer_info(announcement):
    this_peer = Peer(announcement)
    info_hash = announcement["info_hash"].encode("hex") + ".swarm"

    if "event" in announcement and announcement["event"] == "completed":
        redis_connection.hincrby("completions", info_hash, 1)
        redis_connection.hset(info_hash, this_peer.peer_id,
                                this_peer.to_json())
    elif "event" in announcement and announcement["event"] == "stopped":
        redis_connection.hdel(info_hash, this_peer.peer_id)
    else:
        redis_connection.hset(info_hash, this_peer.peer_id,
                                this_peer.to_json())

def build_listing(announcement):
    listing = {
        "tracker id": tracker_id,
        "interval": interval,
        }

    info_hash = announcement["info_hash"].encode("hex")

    values = redis_connection.hvals(info_hash)
    listing["peers"] = [Peer.from_json(e).to_dict() for e in values]

    listing.update(swarm_stats(info_hash))
    return bencode(listing)

def swarm_stats(info_hash):
    peers = [Peer.from_json(e) for e in redis_connection.hvals(info_hash)]
    stats = {
        "downloaded": 0,
        "complete": 0,
        "incomplete": 0}
    for peer in peers:
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

@app.get("/scrape")
def scrape():
    return scrape_stats()
        
@app.get("/announce")
def announce():
    announcement = request.query
    update_peer_info(announcement)
    return build_listing(announcement)
