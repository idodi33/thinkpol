from .connection import Connection
import socket


class Listener:
    """
    Wraps a socket in functions that enable it to operate like 
    a server socket. 
    Provides start, stop and accept methods. 
    Also functions as a context manager with start and stop.

    :param port: the socket's port
    :type port: int
    :param host: the socket's host, defaults to localhost
    :type host: str, optional
    :param backlog: the amount of clients the socket handles,
    defaults to 1000
    :type backlog: int, optional
    :param reuseaddr: whether we cancel cooling off the socket's
    port to allow reusage, defaults to True
    :type reuseaddr: boolean, optional
    """
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
        """
        Starts listening on host:port through the socket.
        """
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def stop(self):
        """
        Stops listening on host:port through the socket.
        """
        self.sock.close()

    def accept(self):
        """
        Accepts a new client through the socket.
        
        :returns: a Connection object representing the connection to the client
        :rtype: Connection
        """
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
