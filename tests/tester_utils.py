from datetime import datetime
import json
import os
from pathlib import Path
from thinkpol.utils.snapshot import Snapshot, ImageData

_IMAGES_DIR = Path(__file__).absolute().parent / 'test_data'
_SERVER_IMAGES_DIR = _IMAGES_DIR / 'server_data'
_HOST = '127.0.0.1'
_PORT = 8000
_MQ_PORT = 5672
_DB_PORT = 27017
_DB = "mongodb"


_USER_ID = 1
_USERNAME = "Anony Mous"
_BIRTHDAY = int(datetime(year=2000, month=1, day=1).timestamp())
_GENDER = "o"
_DATETIME = int(datetime.strptime("2019-12-04_10-08-08-608000", "%Y-%m-%d_%H-%M-%S-%f").timestamp() * 1000)
print(f"_DATETIME: {_DATETIME}")
#_DATETIME = int(datetime(year=2020, month=1, day=1).timestamp() * 1000)
_TRANSLATION_X = -1.5
_TRANSLATION_Y = -1.0
_TRANSLATION_Z = -0.5
_ROTATION_X = 0.0
_ROTATION_Y = 0.5
_ROTATION_Z = 1.0
_ROTATION_W = 1.5
_C_HEIGHT = 1080
_C_WIDTH = 1920
#_C_DATA = 27 * b'a'
_C_PATH = os.path.join(_IMAGES_DIR, 'color_raw_data')
with open(_C_PATH, 'rb') as f:
    _C_DATA = f.read()
_C_PATH_BGR = os.path.join(_IMAGES_DIR, 'color_raw_data_bgr')
with open(_C_PATH_BGR, 'rb') as f:
    _C_DATA_BGR = f.read()
_PARSED_C_PATH = os.path.join(_IMAGES_DIR, 'color_image.jpg')
with open(_PARSED_C_PATH, 'rb') as f:
    _PARSED_C_DATA = f.read() 
_D_WIDTH = 224
_D_HEIGHT = 172
_D_PATH = os.path.join(_IMAGES_DIR, 'depth_raw_data')
with open(_D_PATH, 'rb') as f:
    _D_DATA = f.read()
_PARSED_D_PATH = os.path.join(_IMAGES_DIR, 'depth_image.jpg')
with open(_PARSED_D_PATH, 'rb') as f:
    _PARSED_D_DATA = f.read() 
_HUNGER = -0.5
_THIRST = -0.25
_EXHAUSTION = 0.25
_HAPPINESS = 0.5
_SNAPSHOT = Snapshot(_DATETIME,
    (_TRANSLATION_X, _TRANSLATION_Y, _TRANSLATION_Z), 
    (_ROTATION_X, _ROTATION_Y, _ROTATION_Z, _ROTATION_W), 
    _C_HEIGHT, 
    _C_WIDTH, 
    ImageData("color", _C_WIDTH, _C_HEIGHT, _C_DATA),
    _D_HEIGHT, 
    _D_WIDTH, 
    ImageData("depth", _D_WIDTH, _D_HEIGHT, _D_DATA),
    _HUNGER,
    _THIRST,
    _EXHAUSTION,
    _HAPPINESS)
_SAVE_IMAGES_TUPLE = (str(_SERVER_IMAGES_DIR) + "/2019-12-04_10-08-08-608000/color_raw_data",
                    str(_SERVER_IMAGES_DIR) + "/2019-12-04_10-08-08-608000/depth_raw_data" )
server_gender_dict = {"m": "man", "f": "woman", "o": "other"}
_DICT = {
            'user_id' : _USER_ID,
            'username' : _USERNAME,
            'birthday' : _BIRTHDAY,
            'gender' : server_gender_dict[_GENDER],
            'datetime' : _DATETIME,
            'translation' : (_TRANSLATION_X, _TRANSLATION_Y, _TRANSLATION_Z),
            'rotation' : (_ROTATION_X, _ROTATION_Y, _ROTATION_Z, _ROTATION_W),
            'c_height' : _C_HEIGHT,
            'c_width' : _C_WIDTH,
            'color_image' : _C_PATH,   # this is only the path to the data, not the data itself
            'd_height' : _D_HEIGHT,
            'd_width' : _D_WIDTH,
            'depth_image' : _D_PATH,   # likewise
            'hunger' : _HUNGER,
            'thirst' : _THIRST,
            'exhaustion' : _EXHAUSTION,
            'happiness' : _HAPPINESS
        }
_JSON = json.dumps(_DICT)

_D_IMAGE_JSON = json.dumps({
    "user_id": _USER_ID,
    "username": _USERNAME, 
    "birthday": _BIRTHDAY, 
    "gender": server_gender_dict[_GENDER], 
    "datetime": _DATETIME, 
    "depth_image": _PARSED_D_PATH
    })

_C_IMAGE_JSON = json.dumps({
    "user_id": _USER_ID,
    "username": _USERNAME, 
    "birthday": _BIRTHDAY, 
    "gender": server_gender_dict[_GENDER], 
    "datetime": _DATETIME, 
    "color_image": _PARSED_C_PATH
    })

_POSE_JSON = json.dumps({
    "user_id": _USER_ID,
    "username": _USERNAME, 
    "birthday": _BIRTHDAY, 
    "gender": server_gender_dict[_GENDER], 
    "datetime": _DATETIME, 
    "translation_x": _TRANSLATION_X,
    "translation_y": _TRANSLATION_Y,
    "translation_z": _TRANSLATION_Z,
    "rotation_x": _ROTATION_X,
    "rotation_y": _ROTATION_Y,
    "rotation_z": _ROTATION_Z,
    "rotation_w": _ROTATION_W,
    })

_FEELINGS_JSON = json.dumps({
    "user_id": _USER_ID,
    "username": _USERNAME, 
    "birthday": _BIRTHDAY, 
    "gender": server_gender_dict[_GENDER], 
    "datetime": _DATETIME, 
    "hunger": _HUNGER,
    "thirst": _THIRST,
    "exhaustion": _EXHAUSTION,
    "happiness": _HAPPINESS
    })

