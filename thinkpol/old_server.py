import time
import struct
import threading
import pathlib
import os
from .utils import listener as lsn
#from .utils import protocol
from .utils import snapshot as snp
import cortex_pb2
import config_pb2
from .parsers import parsers


def run_server(address, publish):
    print(f"Parsers dict is: {parsers}")
    if type(address) == str:
        ip, port = address.split(':')
    else: # it's a tuple
        ip, port = address
    with lsn.Listener(int(port), ip, 1000, True) as listener:
        while True:
            # client is a connection object
            client = listener.accept()
            handler = Handler(client, publish)
            handler.start()


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, publish):
        super().__init__()
        self.connection = connection
        self.publish = publish

    def run(self):
        """
        Handles one client's request and opens/edits a corresponding file.
        """
        '''
        hello_msg = self.connection.receive_message()
        hello = protocol.Hello.deserialize(hello_msg)
        dir_address = os.path.join(self.data_dir, str(hello.user_id))
        '''
        user_msg = self.connection.receive_message()
        user = cortex_pb2.User()
        user.ParseFromString(user_msg)
        #dir_address = os.path.join(self.data_dir, str(user.user_id))
        #context = Context(user, publish)
        '''
        config = protocol.Config(["translation", "color_image"])
        config_msg = config.serialize()
        '''
        fields_to_parse = ["translation", "color_image"]
        config = config_pb2.Config(
            fields = fields_to_parse
            )
        config_msg = config.SerializeToString()
        self.connection.send_message(config_msg)
        snapshot_msg = self.connection.receive_message()
        snapshot = snp.Snapshot.from_bytes(snapshot_msg)
        '''
        for field in fields_to_parse:
            if parsers[field]:
                parsers[field](context, snapshot)
            else:
                raise ValueError(f"No parser for {field}.")
        '''
        self.publish(user, snapshot)
        #parse_translation(context, snapshot)
        #parse_color_image(context, snapshot)
        self.connection.close()

'''An object with common utilities the parsers are likely to need.
class Context:
    lock = threading.Lock()
    def __init__(self, user_data):
        self.user_data = user_data
        self.dir = dir

    
    def get_file_path(self, subdir, file):
        """
        Constructs a subdirectory  named 'subdir' in self.dir
        (if it doesn't exist yet).
        Constructs a file named 'file' in self.dir / subdir
        (if it doesn't exist yet) and returns it.
        """
        with Context.lock:
            subdir_pathname = os.path.join(self.dir , subdir)
            subdir_path = pathlib.Path(subdir_pathname)
            if not subdir_path.is_dir():
                subdir_path.mkdir(parents=True)
            file_pathname = os.path.join(subdir_pathname, file)
            file_path = pathlib.Path(file_pathname)
            if not file_path.is_file():
                file_path.touch()
            return file_path
    '''