from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.sock = socket.socket()
        if reuseaddr:
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}', " + \
                f"backlog={self.backlog}, reuseaddr={self.reuseaddr})"

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        self.sock.close()

    def accept(self):
        peer, peer_address = self.sock.accept()
        return Connection(peer)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        try:
            if exception:
                raise exception
        finally:
            self.stop()
