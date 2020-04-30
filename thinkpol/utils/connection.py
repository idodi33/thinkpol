import socket
import struct

class Connection:
    """
    Wraps a socket with functions that enable sending and receiving whole messages.
    Provides a send_message, receive_message, connect and close methods.
    Also functions as a context manager using connect and close.

    :param sock: the socket that the connection wraps
    :type sock: socket
    """
    def __init__(self, sock):
        self.sock = sock

    def __repr__(self):
        sockip, sockport = self.sock.getsockname()
        peerip, peerport = self.sock.getpeername()
        return f'<Connection from {sockip}:{sockport} to {peerip}:{peerport}>'

    def send(self, data):
        self.sock.sendall(data)

    def send_message(self, data):
        """
        Sends a chunk of binary data with its size prepended to it in binary.

        :param data: the binary data we're sending
        :type data: bytes
        """
        size = len(data)
        message = struct.pack("I", size)
        message += data
        self.send(message)

    def receive(self, size):
        msg = b''
        buf = b''
        received_size = 0
        while received_size < size:
            buf = self.sock.recv(size - received_size)
            if not buf:
                break
            msg += buf
            received_size += len(buf)
        return msg

    def receive_message(self):
        """
        Receives the size of message in bytes, and then message itself.

        :returns: the binary message (without the size prepended)
        :rtype: bytes
        """
        b_size = self.receive(4)
        size = struct.unpack("I", b_size)[0]
        b_msg = self.receive(size)
        return b_msg

    def close(self):
        self.sock.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        try:
            if exception:
                raise exception
        finally:
            self.sock.close()

    @classmethod
    def connect(cls, host, port):
        """
        Creates a new socket connected to host:port, wraps it in
        a Connection object and returns that.

        :param host: the host we connect to
        :type host: str
        :param port: the port we connect to
        :type port: str
        :returns: the Connection object connected to host:port
        :rtype: Connection
        """
        sock = socket.socket()
        sock.connect((host, int(port)))
        return cls(sock)
