import socket
import time

import pytest

from ..listener import Listener


_PORT = 1234
_HOST = '127.0.0.1'
_BACKLOG = 5000
_REUSEADDR = True
_DATA = b'Hello, world!'


@pytest.fixture
def listener():
    return Listener(_PORT, host=_HOST, backlog=_BACKLOG, reuseaddr=_REUSEADDR)


def test_attributes(listener):
    assert listener.port == _PORT
    assert listener.host == _HOST
    assert listener.backlog == _BACKLOG
    assert listener.reuseaddr == _REUSEADDR


def test_defaults():
    listener = Listener(_PORT)
    assert listener.host == '0.0.0.0'
    assert listener.backlog == 1000
    assert listener.reuseaddr is True


def test_repr(listener):
    assert repr(listener) == f'Listener(port={_PORT!r}, host={_HOST!r}, backlog={_BACKLOG!r}, reuseaddr={_REUSEADDR!r})'


def test_close(listener):
    assert socket.socket().connect_ex((_HOST, _PORT)) != 0
    listener.start()
    try:
        time.sleep(0.1)
        assert socket.socket().connect_ex((_HOST, _PORT)) == 0
    finally:
        listener.stop()
    assert socket.socket().connect_ex((_HOST, _PORT)) != 0


def test_accept(listener):
    sock = socket.socket()
    listener.start()
    try:
        time.sleep(0.1)
        sock.connect((_HOST, _PORT))
        connection = listener.accept()
        try:
            sock.sendall(_DATA)
            assert connection.receive(len(_DATA)) == _DATA
        finally:
            connection.close()
    finally:
        listener.stop()
