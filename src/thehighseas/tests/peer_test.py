import unittest
from base64 import b64encode, b64decode

from hamcrest import *
import simplejson
import ipaddr

from domain import Peer, Clock, NonIPv4AddressException

class FakeClock(object):
    def __init__(self, canned_time):
        self.canned_time = canned_time
    
    def now(self):
        return self.canned_time

class PeerTest(unittest.TestCase):
    def test_to_json(self):
        peer = Peer()
        peer.peer_id = "test"
        peer.port = 6881
        peer.uploaded = 0
        peer.downloaded = 0
        peer.left = 1 
        peer.ip = ipaddr.IPAddress("10.10.10.10")
        peer.last_seen = 0
        
        expected_json = {"peer_id": b64encode("test"),
                         "port": peer.port,
                         "uploaded": peer.uploaded,
                         "downloaded": peer.downloaded,
                         "left": peer.left,
                         "last_seen": peer.last_seen,
                         "ip": peer.ip.exploded}

        assert_that(simplejson.loads(peer.to_json()), is_(expected_json))

    def test_from_json(self):
        peer_id = "test"
        port = 6881
        uploaded = 0
        downloaded = 0
        left = 1 
        ip = ipaddr.IPAddress("10.10.10.10")
        last_seen = 0
        peer_json = simplejson.dumps({"peer_id": b64encode(peer_id),
                                      "port": port,
                                      "uploaded": uploaded,
                                      "downloaded": downloaded,
                                      "left": left,
                                      "ip": ip.exploded,
                                      "last_seen": last_seen})
        peer = Peer.from_json(peer_json)

        assert_that(peer.peer_id, is_(peer_id))
        assert_that(peer.port, is_(port))
        assert_that(peer.uploaded, is_(uploaded))
        assert_that(peer.downloaded, is_(downloaded))
        assert_that(peer.left, is_(left))
        assert_that(peer.ip, is_(ip))
        assert_that(peer.last_seen, is_(last_seen))

    def test_to_dict(self):
        peer = Peer()
        peer.peer_id = "test"
        peer.port = 6881
        peer.ip = ipaddr.IPAddress("10.10.10.10")

        expected_dict = {"peer_id": peer.peer_id,
                         "port": peer.port,
                         "ip": peer.ip.exploded}
        
        assert_that(peer.to_dict(), is_(expected_dict))

    def test_to_binary(self):
        peer = Peer()
        peer.port = 6881
        peer.ip = ipaddr.IPAddress("10.10.10.10")

        assert_that(len(peer.to_binary()), is_(6))

    def test_to_binary_with_ipv6(self):
        peer = Peer()
        peer.port = 6881
        peer.ip = ipaddr.IPAddress("::")

        try:
            peer.to_binary()
            assert False
        except NonIPv4AddressException:
            pass
