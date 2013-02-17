from wsgiref.simple_server import make_server

import bottle

from thehighseas import (
    rootapp,
    hypertext,
    tracker,
    constants
)

def main():
    try:
        http_server = make_server("", int(constants.port), rootapp.app)
        http_server.serve_forever()
    except KeyboardInterrupt:
        print("Quitting!")

if __name__ == "__main__":
    main()
