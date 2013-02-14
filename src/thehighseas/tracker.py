from base64 import b64encode, b64decode
import time

from bencode import bencode, bdecode
from bottle import Bottle, request, response, abort
from redis import StrictRedis
import simplejson

app = Bottle()

_redis_connection_ = StrictRedis()

_tracker_id_ = "thehighseas"

_interval_ = 5

def update_peer_info(announcement):
    this_peer = Peer(announcement)
    info_hash = announcement["info_hash"].encode("hex") + ".swarm"
    _redis_connection_.hset(info_hash, this_peer.peer_id,
                            this_peer.to_json())
    if "event" in announcement:
        record_event(announcement)

def build_listing(announcement):
    listing = {
        "tracker id": _tracker_id_,
        "interval": _interval_,
        }

    info_hash = announcement["info_hash"].encode("hex")

    values = _redis_connection_.hvals(info_hash)
    listing["peers"] = [Peer.from_json(e).to_dict() for e in values]

    listing.update(stats_for_info_hash(info_hash))
    return bencode(listing)

def stats_for_info_hash(info_hash):
    peers = [Peer.from_json(e) for e in _redis_connection_.hvals(info_hash)]
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
    info_hashes = _redis_connection_.keys("*.swarm")
    stats = {}
    for info_hash in info_hashes:
        stats[info_hash] = stats_for_info_hash(info_hash)
    return bencode(stats)

def record_event(announcement):
    event = annoucement["event"]
    if event == "completed":
        # Incement xxxx.completed
        pass
    elif event == "stopped":
        # Remove peer
        pass
    elif event == "started":
        pass

class Peer(object):
    def __init__(self, announcement=None):
        if announcement is not None:
            self.peer_id = announcement["peer_id"]
            self.port = announcement["port"]
            if announcement["left"] == "0":
                self.status = "complete"
            else:
                self.status = "incomplete"
            self.last_seen = int(time.time())
            try:
                self.ip = announcement["ip"]
            except KeyError:
                self.ip = request.remote_addr
            self.uploaded = int(announcement["uploaded"])
            self.downloaded = int(announcement["downloaded"])
            self.left = int(announcement["left"])

    def __eq__(self, other):
        return self.peer_id == other.peer_id

    def is_complete(self):
        return self.status == "complete"

    def to_json(self):
        return simplejson.dumps(
            {"peer_id": b64encode(self.peer_id),
             "ip": self.ip,
             "port": self.port,
             "status": self.status,
             "last_seen": self.last_seen,
             "uploaded": self.uploaded,
             "downloaded": self.downloaded,
             "left": self.left},
            separators=(',',':'))

    def to_dict(self):
        return {"peer_id": self.peer_id,
                "ip": self.ip,
                "port": self.port}

    @classmethod
    def from_json(cls, json_string):
        dict_ = simplejson.loads(json_string)
        peer = Peer()
        peer.peer_id = b64decode(dict_["peer_id"])
        peer.ip = dict_["ip"]
        peer.port = dict_["port"]
        peer.status = dict_["status"]
        peer.last_seen = dict_["last_seen"]
        peer.uploaded = dict_["uploaded"]
        peer.downloaded = dict_["downloaded"]
        peer.left = dict_["left"]
        return peer

@app.get("/scrape")
def scrape():
    return scrape_stats()
        
@app.get("/announce")
def announce():
    announcement = request.query
    update_peer_info(announcement)
    return build_listing(announcement)
