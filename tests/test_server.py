import pytest
import tester_utils as tu
from thinkpol.utils import listener
from thinkpol.protobufs import cortex_pb2
from thinkpol.protobufs import config_pb2
from thinkpol.parsers import parsers
from thinkpol.server import server
from thinkpol.server import server_utils
import time


@pytest.fixture
def mock_listener(monkeypatch):
    monkeypatch.setattr(listener, 'Listener', MockListener)


class MockListener:
    def __init__(self, port, host, backlog, reuseaddr):
        pass

    def accept(self):
        return MockConnection(None)

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        pass


gender_dict = {"m": 0, "f": 1, "o": 2}
got_user_msg = False
got_snap_msg = False


class MockConnection:
    def __init__(self, sock):
        pass

    def receive_message(self):
        global got_user_msg
        global got_snap_msg
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
        if not got_user_msg:
            try:
                return user_msg
            finally:
                got_user_msg = True
        elif not got_snap_msg:
            try:
                return snapshot_msg
            finally:
                got_snap_msg = True
        else:
            return "kill"

    def send_message(self, data):
        config = config_pb2.Config(
            fields =
            parsers.keys()
            )
        config_msg = config.SerializeToString()
        assert data == config_msg

    def close(self):
        pass


@pytest.fixture
def mock_data_dir(monkeypatch):
    monkeypatch.setattr(server_utils, 'RAW_DATA_DIR', tu._SERVER_IMAGES_DIR)


def test_server(mock_listener):
    server.run_server(tu._HOST, tu._PORT, lambda x: x)


def test_server_utils(mock_data_dir):
    """
    This tests functions in server_utils such as save_images.
    """
    user = cortex_pb2.User(
    user_id = tu._USER_ID,
    username = tu._USERNAME,
    birthday = tu._BIRTHDAY,
    gender = gender_dict[tu._GENDER]
    )
    c_path, d_path = server_utils.save_images(tu._SNAPSHOT)
    assert (c_path, d_path) == tu._SAVE_IMAGES_TUPLE
    snapshot_dict = server_utils.make_snapshot_dict(user, tu._SNAPSHOT, c_path, d_path)
    snapshot_dict['color_image'] = tu._C_PATH
    snapshot_dict['depth_image'] = tu._D_PATH
    assert snapshot_dict == tu._DICT
    assert server_utils.filter_dict(snapshot_dict) == tu._DICT
