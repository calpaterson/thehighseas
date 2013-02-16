import cProfile

from gevent import monkey; monkey.patch_all()
import bottle

from thehighseas import (
    rootapp,
    hypertext,
    tracker,
    constants
)

def main():
    try:
        bottle.run(host=constants.host, port=constants.port,
                   server="gevent", app=rootapp.app)
    except KeyboardInterrupt:
        print("Quitting!")

if __name__ == "__main__":
    main()
