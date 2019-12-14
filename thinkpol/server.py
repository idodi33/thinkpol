import time
from datetime import datetime
import struct
import threading
import pathlib
import os
import json
from PIL import Image
from .utils import listener as lsn
from .utils import protocol
from .utils import snapshot as snp


parsers = dict()


def run_server(address, data):
    if type(address) == str:
        ip, port = address.split(':')
    else: # it's a tuple
        ip, port = address
    with lsn.Listener(int(port), ip, 1000, True) as listener:
        while True:
            # client is a connection object
            client = listener.accept()
            handler = Handler(client, data)
            handler.start()


def parser(field):
    def decorator(f):
        parsers[field] = f
        return f
    return decorator


@parser('translation')
def parse_translation(context, snapshot):
    datetime_obj = datetime.fromtimestamp(snapshot.datetime / 1000)
    formatted_time = datetime.strftime(datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
    file_path = context.get_file_path(formatted_time, 'translation.json')
    x, y, z = snapshot.translation
    data_dict = {"x": x, "y": y, "z": z}
    with open(file_path, 'w') as f:
        js = json.dumps(data_dict)
        print(js)
        f.write(js)


@parser('color_image')
def parse_color_image(context, snapshot):
    datetime_obj = datetime.fromtimestamp(snapshot.datetime / 1000)
    formatted_time = datetime.strftime( datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
    file_path = context.get_file_path(formatted_time, 'color_image.jpg')
    data = snapshot.color_image.data
    data_len = snapshot.color_image.size
    rgb_triplets = [(data[i], data[i + 1], data[i + 2]) for i in range(0, data_len, 3)]
    image = Image.new("RGB", (snapshot.c_width, snapshot.c_height))
    image.putdata(rgb_triplets)
    image.save(file_path)


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        """
        Handles one client's request and opens/edits a corresponding file.
        """
        #with Handler.lock:
        print("meow")
        hello_msg = self.connection.receive_message()
        hello = protocol.Hello.deserialize(hello_msg)
        dir_address = os.path.join(self.data_dir, str(hello.user_id))
        context = Context(dir_address)
        config = protocol.Config(["translation", "color_image"])
        config_msg = config.serialize()
        self.connection.send_message(config_msg)
        snapshot_msg = self.connection.receive_message()
        snapshot = snp.Snapshot.from_bytes(snapshot_msg)
        parse_translation(context, snapshot)
        parse_color_image(context, snapshot)
        self.connection.close()


class Context:
    lock = threading.Lock()
    def __init__(self, dir):
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
