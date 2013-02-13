import cProfile

from gevent import monkey; monkey.patch_all()
import bottle

from thehighseas import (
    tracker
)

def main():
    try:
        app = bottle.Bottle()
        app.mount("/tracker", tracker.app)
        bottle.run(port=11235, server="gevent", app=app)
    except KeyboardInterrupt:
        print("Quitting!")

if __name__ == "__main__":
    main()

