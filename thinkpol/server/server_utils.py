import threading
from datetime import datetime
import os
import pathlib
from thinkpol.parsers import parsers


#RAW_DATA_DIR = os.path.join(os.getcwd(), 'raw_data')
RAW_DATA_DIR = pathlib.Path("opt/thinkpol/raw_data")


lock = threading.Lock()
def save_images(snapshot):
    """
    Gets a snapshot, saves the color and depth data in bytes to files on disk,
    and returns the file paths.

    :param snapshot: the snapshot from which we get the data
    :type snapshot: Snapshot
    :returns: a 2-tuple - (color_image_path, depth_image_path)
    :rtype: tuple
    """
    print(f"save_images: RAW_DATA_DIR is {RAW_DATA_DIR}")
    datetime_obj = datetime.fromtimestamp(
        snapshot.datetime / 1000
        )
    formatted_time = datetime.strftime(
        datetime_obj, "%Y-%m-%d_%H-%M-%S-%f"
        )
    subdir_path_name = os.path.join(
        RAW_DATA_DIR, formatted_time
        )
    subdir_path = pathlib.Path(subdir_path_name)
    color_file_path_name = os.path.join(
        subdir_path_name, 'color_raw_data'
        )
    color_file_path = pathlib.Path(color_file_path_name)
    depth_file_path_name = os.path.join(
        subdir_path_name, 'depth_raw_data'
        )
    depth_file_path = pathlib.Path(depth_file_path_name)
    print(f"save_images: depth_file_path_name is {depth_file_path_name}")
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
    """
    Returns a list of the fields we can currently handle, according
    to which parsers we currently have.
    
    :returns: a list of the names (strings) of the available fields
    :rtype: list
    """
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
    """
    Receives a dictionary with snapshot data and returns
    an updated dict, containing only the fields our
    parsers can handle.

    :param snapshot_dict: the original dict
    :type snapshot_dict: dict
    :returns: the filtered dict
    :rtype: dict
    """
    new_dict = snapshot_dict.copy()
    new_fields = ['user_id', 'username', 'birthday', 'gender', 'datetime']
    new_fields += available_fields()
    for field in snapshot_dict.keys():
        if field not in new_fields:
            del new_dict[field]
    return new_dict


gender_dict = {0: "man", 1: "woman", 2: "other"}


def make_snapshot_dict(user, snapshot, c_path, d_path):
    """
    Gets user and snapshot objects and creates a dict with
    their corresponding info to be turned into a json
    and parsed.

    :param user: the user object
    :type user: cortex_pb2.User
    :param snapshot: the snapshot object
    :type snapshot: Snapshot
    :param c_path: the path to the color image
    :type c_path: str
    :param d_path: the path to the depth image
    :type d_path: str
    :returns: the dict that was created
    :rtype: dict
    """ 
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
        'color_image' : c_path,   # this is only the path to the data, not the data itself
        'd_height' : snapshot.d_height,
        'd_width' : snapshot.d_width,
        'depth_image' : d_path,   # likewise
        'hunger' : snapshot.hunger,
        'thirst' : snapshot.thirst,
        'exhaustion' : snapshot.exhaustion,
        'happiness' : snapshot.happiness
        }
    return snapshot_dict