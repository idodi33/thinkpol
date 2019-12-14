import socket
import struct

class Connection:
    def __init__(self, sock):
        self.sock = sock

    def __repr__(self):
        sockip, sockport = self.sock.getsockname()
        peerip, peerport = self.sock.getpeername()
        return f'<Connection from {sockip}:{sockport} to {peerip}:{peerport}>'

    # TODO: maybe delete this after we have send_message.
    def send(self, data):
        self.sock.sendall(data)

    def send_message(self, data):
        """
        Sends data with prepended size of data.
        """
        size = len(data)
        message = struct.pack("I", size)
        message += data
        self.send(message)

    # TODO: maybe delete this after we have recieve_message.
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
        sock = socket.socket()
        sock.connect((host, int(port)))
        return cls(sock)
