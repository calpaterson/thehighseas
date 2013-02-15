from base64 import b64encode, b64decode
import hashlib
import time

from bencode import bencode, bdecode
from bottle import request
import simplejson

from constants import redis_connection

_announce_url_ = "http://localhost:11235/tracker/announce"

class NoInfoException(Exception):
    pass

class Swarm(object):
    def number_of_seeds(self):
        return sum(1 for p in redis_connection.hvals(self.info_hash + ".swarm")
                     if Peer.from_json(p).is_complete())

    def number_of_leechers(self):
        return sum(1 for p in redis_connection.hvals(self.info_hash + ".swarm")
                     if not Peer.from_json(p).is_complete())

    def times_downloaded(self):
        times = redis_connection.hget("completions", self.info_hash)
        if times is not None:
            return times
        else:
            return 0

    def name(self):
        try:
            return bdecode(redis_connection.get(self.info_hash + ".info"))["name"]
        except TypeError:
            return "-"

    def completed_by(self, peer):
        redis_connection.hincrby("completions", self.info_hash, 1)
        self.update(peer)

    def stopped_by(self, peer):
        redis_connection.hdel(self.info_hash + ".swarm", peer.peer_id)

    def update(self, peer):
        redis_connection.hset(self.info_hash + ".swarm", peer.peer_id, peer.to_json())

    def to_metainfo(self):
        try:
            info_as_dict = bdecode(redis_connection.get(self.info_hash + ".info"))
            return bencode({"announce": _announce_url_,
                            "info": info_as_dict })
        except TypeError:
            raise NoInfoException()

    def peers(self):
        values = redis_connection.hvals(self.info_hash + ".swarm")
        return [Peer.from_json(e).to_dict() for e in values]

    def _save_info_(self, info_as_dict):
        bencoded_info_dict = bencode(info_as_dict)
        h = hashlib.new("sha1")
        h.update(bencoded_info_dict)
        self.info_hash = h.hexdigest()
        print("info_hash = " + self.info_hash)
        redis_connection.set(self.info_hash + ".info", bencoded_info_dict)

    def _ensure_recorded_(self):
        redis_connection.sadd("hashes", self.info_hash)

    @classmethod
    def all(cls):
        return (cls.from_hex_hash(hash)
                for hash in redis_connection.smembers("hashes"))

    @classmethod
    def from_hex_hash(cls, hex_hash):
        s = Swarm()
        s.info_hash = hex_hash
        return s

    @classmethod
    def from_metainfo_file(cls, metainfo_file, filename):
        metainfo = bdecode(metainfo_file.read())
        s = Swarm()
        s._save_info_(metainfo["info"])
        s._ensure_recorded_()        
        return s

    @classmethod
    def from_announcement(cls, announcement):
        s = Swarm()
        s.info_hash = announcement["info_hash"].encode("hex")
        s._ensure_recorded_()
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
