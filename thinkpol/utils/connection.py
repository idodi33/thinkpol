import socket


class Connection:
    def __init__(self, sock):
        self.sock = sock

    def __repr__(self):
        sockip, sockport = self.sock.getsockname()
        peerip, peerport = self.sock.getpeername()
        return f'<Connection from {sockip}:{sockport} to {peerip}:{peerport}>'

    def send(self, data):
        self.sock.sendall(data)

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
