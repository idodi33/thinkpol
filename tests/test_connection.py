import socket
import time

import pytest

from ..connection import Connection


_PORT = 1234
_DATA = b'Hello, world!'


@pytest.fixture
def server():
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', _PORT))
    server.listen(1000)
    try:
        time.sleep(0.1)
        yield server
    finally:
        server.close()


def test_repr(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    _, other_port = sock.getsockname()
    assert repr(connection) == f'<Connection from 127.0.0.1:{other_port} to 127.0.0.1:{_PORT}>'


def test_close(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    assert not sock._closed
    connection.close()
    assert sock._closed


def test_send(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        connection.send(_DATA)
    finally:
        connection.close()
    chunks = []
    while True:
        chunk = client.recv(4096)
        if not chunk:
            break
        chunks.append(chunk)
    assert b''.join(chunks) == _DATA


def test_receive(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        client.sendall(_DATA)
        first = connection.receive(1)
        assert first == _DATA[:1]
        rest = connection.receive(len(_DATA) - 1)
        assert rest == _DATA[1:]
    finally:
        connection.close()

'''
def test_incomplete_data(server):
    sock = socket.socket()
    sock.connect(('127.0.0.1', _PORT))
    connection = Connection(sock)
    try:
        client, _ = server.accept()
        client.sendall(b'1')
        client.close()
        with pytest.raises(Exception):
            connection.receive(2)
    finally:
        connection.close()
'''
