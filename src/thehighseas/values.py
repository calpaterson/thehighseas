import time
from base64 import b64encode, b64decode

import simplejson
from bottle import request

from constants import redis_connection

class Swarm(object):
    def number_of_seeds(self):
        return sum(1 for p in redis_connection.hvals(self.info_hash + ".swarm")
                     if not Peer.from_json(p).is_complete())

    def number_of_leechers(self):
        return sum(1 for p in redis_connection.hvals(self.info_hash + ".swarm")
                     if not Peer.from_json(p).is_complete())

    def times_downloaded(self):
        redis_connection.hget("completions", self.info_hash)

    @classmethod
    def all(cls):
        return (cls.from_hex_hash(key[:-6])
                for key in redis_connection.keys("*.swarm"))

    @classmethod
    def from_hex_hash(cls, hex_hash):
        s = Swarm()
        s.info_hash = hex_hash
        return s

    def from_info_hash(cls, info_hash):
        s = Swarm()
        s.info_hash = info_hash.encode("hex")
        return s

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
