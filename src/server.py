import cProfile

from gevent import monkey; monkey.patch_all()
import bottle

from thehighseas import (
    rootapp,
    hypertext,
    tracker
)

def main():
    try:
        rootapp.app.mount("/tracker", tracker.app)
        bottle.run(port=11235, server="gevent", app=rootapp.app)
    except KeyboardInterrupt:
        print("Quitting!")

if __name__ == "__main__":
    main()
