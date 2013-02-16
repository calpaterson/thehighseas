from redis import StrictRedis

redis_connection = StrictRedis()

tracker_id = "thehighseas"

host = "192.168.1.67"

port = "11235"

announce_url = "http://{host}:{port}/tracker/announce".format(host=host, port=port)

interval = 5
