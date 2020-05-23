import threading
from thinkpol.server.server_utils import save_images, available_fields, filter_dict, make_snapshot_dict
from thinkpol.parsers import parsers
from thinkpol.utils import listener as lsn
from thinkpol.utils import snapshot as snp
from thinkpol.protobufs import cortex_pb2
from thinkpol.protobufs import config_pb2
import json
import os

RAW_DATA_DIR = os.path.join(os.getcwd(), 'raw_data')
KILLED = False


def run_server(host, port, publish):
    """
    Starts receiving connections from clients on host:port, and publishing
    the data we receive to the function publish.

    :param host: the host on which we're listening
    :type host: str
    :param port: the port on which we're listening
    :type port: str
    :param publish: the function to which we publish the data
    :type publish: callable
    """
    print("started run_server")
    with lsn.Listener(int(port), host, 1000, True) as listener:
        while not KILLED:
            # client is a connection object
            client = listener.accept()
            handler = Handler(client, publish)
            handler.start()


class Handler(threading.Thread):
    """
    Handles connection the server gets in a multithreaded way.
    :param connection: the connection the server gets
    :type connection: Connection
    :param publish: the function to which we publish the data
    :type publish: callable
    """
    lock = threading.Lock()

    def __init__(self, connection, publish):
        super().__init__()
        self.connection = connection
        self.publish = publish

    def run(self):
        """
        Handles one client's request and opens/edits a corresponding file.
        """
        print("Started handling a client.")
        global KILLED
        user_msg = self.connection.receive_message()
        if user_msg == "kill":
            KILLED = True
            return
        user = cortex_pb2.User()
        user.ParseFromString(user_msg)
        fields_to_parse = available_fields()
        config = config_pb2.Config(fields = parsers.keys())
        config_msg = config.SerializeToString()
        self.connection.send_message(config_msg)
        snapshot_msg = self.connection.receive_message()
        snapshot = snp.Snapshot.from_bytes(snapshot_msg)

        c_path, d_path = save_images(snapshot)
        snapshot_dict = make_snapshot_dict(
            user, snapshot, c_path, d_path
            )
        json_dict = filter_dict(snapshot_dict)
        print(f"json_dict for this snapshot is {json_dict}")
        json_data = json.dumps(json_dict)
        self.publish(json_data)
        print("closing connection")
        self.connection.close()

