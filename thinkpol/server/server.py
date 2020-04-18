import time
import struct
import threading
import pathlib
import os
from ..utils import listener as lsn
#from .utils import protocol
from ..utils import snapshot as snp
from ..protobufs import cortex_pb2
from ..protobufs import config_pb2
import json
from ..parsers import parsers
from datetime import datetime
import time


RAW_DATA_DIR = os.path.join(os.getcwd(), 'raw_data')
KILLED = False


def run_server(host, port, publish):
    print("started run_server")
    with lsn.Listener(int(port), host, 1000, True) as listener:
        while not KILLED:
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
        print("Started handling a client.")
        '''
        hello_msg = self.connection.receive_message()
        hello = protocol.Hello.deserialize(hello_msg)
        dir_address = os.path.join(self.data_dir, str(hello.user_id))
        '''
        global KILLED
        user_msg = self.connection.receive_message()
        if user_msg == "kill":
            KILLED = True
            return
        user = cortex_pb2.User()
        user.ParseFromString(user_msg)
        #dir_address = os.path.join(self.data_dir, str(user.user_id))
        #context = Context(user, publish)
        '''
        config = protocol.Config(["translation", "color_image"])
        config_msg = config.serialize()
        '''
        fields_to_parse = available_fields()
        config = config_pb2.Config(
            fields = parsers.keys()
            )
        config_msg = config.SerializeToString()
        self.connection.send_message(config_msg)
        snapshot_msg = self.connection.receive_message()
        snapshot = snp.Snapshot.from_bytes(snapshot_msg)
        print(f"Server: type of datetime is {type(snapshot.datetime)}")
        print(f"Server: datetime is {snapshot.datetime}")
        '''
        for field in fields_to_parse:
            if parsers[field]:
                parsers[field](context, snapshot)
            else:
                raise ValueError(f"No parser for {field}.")
        '''
        color_image_path, depth_image_path = save_images(snapshot)
        gender_dict = {0: "man", 1: "woman", 2: "other"}
        #print(f"gender_dict[user.gender] is {gender_dict[user.gender]}")
        snapshot_dict = {
            'user_id' : user.user_id,
            'username' : user.username,
            'birthday' : user.birthday,
            'gender' : gender_dict[user.gender],
            'datetime' : snapshot.datetime,
            'translation' : snapshot.translation,
            'rotation' : snapshot.rotation,
            'c_height' : snapshot.c_height,
            'c_width' : snapshot.c_width,
            'color_image' : color_image_path,   # this is only the path to the data, not the data itself
            'd_height' : snapshot.d_height,
            'd_width' : snapshot.d_width,
            'depth_image' : depth_image_path,   # likewise
            'hunger' : snapshot.hunger,
            'thirst' : snapshot.thirst,
            'exhaustion' : snapshot.exhaustion,
            'happiness' : snapshot.happiness
        }
        json_dict = filter_dict(snapshot_dict)
        print(f"json_dict for this snapshot is {json_dict}")
        json_data = json.dumps(json_dict)
        self.publish(json_data)
        #parse_translation(context, snapshot)
        #parse_color_image(context, snapshot)
        print("closing connection")
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

lock = threading.Lock()
def save_images(snapshot):
    '''
    Gets a snapshot, saves the color and depth data in bytes to files on disk,
    and returns the file paths.
    '''
    datetime_obj = datetime.fromtimestamp(snapshot.datetime / 1000)
    formatted_time = datetime.strftime(datetime_obj, "%Y-%m-%d_%H-%M-%S-%f")
    subdir_path_name = os.path.join(RAW_DATA_DIR, formatted_time)
    subdir_path = pathlib.Path(subdir_path_name)
    color_file_path_name = os.path.join(subdir_path_name, 'color_raw_data')
    color_file_path = pathlib.Path(color_file_path_name)
    depth_file_path_name = os.path.join(subdir_path_name, 'depth_raw_data')
    depth_file_path = pathlib.Path(depth_file_path_name)
    with lock:
        if not subdir_path.is_dir():
            subdir_path.mkdir(parents=True)
        if not color_file_path.is_file():
            color_file_path.touch()
        if not depth_file_path.is_file():
            depth_file_path.touch()
    color_file_path.write_bytes(snapshot.color_image.data)
    depth_file_path.write_bytes(snapshot.depth_image.data)
    print(f"save_images: size of depth_image.data is {len(snapshot.depth_image.data)}")
    return color_file_path_name, depth_file_path_name

def available_fields():
    '''
    Gets a list of the fields we can currently handle, according
    to which parsers we currently have.
    '''
    fields = []
    if 'pose' in parsers.keys():
        fields += ['translation', 'rotation']
    if 'color_image' in parsers.keys():
        fields += ['c_height', 'c_width', 'color_image']
    if 'depth_image' in parsers.keys():
        fields += ['d_height', 'd_width', 'depth_image']
    if 'feelings' in parsers.keys():
        fields += ['happiness', 'hunger', 'thirst', 'exhaustion']
    return fields

def filter_dict(snapshot_dict):
    '''
    Gets a dictionary with snapshot and user info 
    to filter it according to the parsers we currently have.
    Returns a filtered dict (always includes the user info).
    '''
    new_dict = snapshot_dict.copy()
    new_fields = ['user_id', 'username', 'birthday', 'gender', 'datetime']
    new_fields += available_fields()
    for field in snapshot_dict.keys():
        if field not in new_fields:
            del new_dict[field]
    return new_dict

