from os import environ

from redis import StrictRedis

redis_connection = StrictRedis()

tracker_id = "thehighseas"

host = environ.get("THS_HOST", "localhost")

port = environ.get("THS_PORT", "11235")

announce_url = "http://{host}:{port}/tracker/announce".format(host=host, port=port)

interval = 5
