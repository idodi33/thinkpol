import pytest
from datetime import datetime
from thinkpol.utils import  connection
import thinkpol.reader.reader as rd
from thinkpol.protobufs import cortex_pb2
from thinkpol.protobufs import config_pb2
from thinkpol.client import client
import tester_utils as tu
from thinkpol.parsers import parsers
import time


@pytest.fixture
def mock_reader(monkeypatch):
    monkeypatch.setattr(rd, 'Reader', MockReader)


class MockReader:
    def __init__(self, path, format):
        self.user_id = tu._USER_ID
        self.user_name = tu._USERNAME
        self.birth_date = tu._BIRTHDAY
        self.gender = gender_dict[tu._GENDER]

    def __iter__(self):
        return iter([tu._SNAPSHOT])


@pytest.fixture
def mock_connection(monkeypatch):
    monkeypatch.setattr(connection, 'Connection', MockConnection)


gender_dict = {"m": 0, "f": 1, "o": 2}


class MockConnection:
    def __init__(self, sock):
        pass

    def send_message(self, data):
        time.sleep(0.5)
        user = cortex_pb2.User(
        user_id = tu._USER_ID,
        username = tu._USERNAME,
        birthday = tu._BIRTHDAY,
        gender = gender_dict[tu._GENDER]
        )
        user_msg = user.SerializeToString()
        snapshot_msg = tu._SNAPSHOT.serialize_request(
            parsers.keys()
            )
        assert data == user_msg or data == snapshot_msg

    def receive_message(self):
        time.sleep(0.5)
        config = config_pb2.Config(
            fields = parsers.keys()
            )
        return config.SerializeToString()

    @classmethod
    def connect(cls, host, port):
        return cls(None)

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        pass


def test_client(mock_reader, mock_connection):
    cl = client.upload_sample(tu._HOST, tu._PORT, 'name.mind')
