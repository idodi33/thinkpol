from datetime import datetime
import json
from ..utils.snapshot import Snapshot, ImageData


_HOST = '127.0.0.1'
_PORT = 8000
_MQ_PORT = 5672


_USER_ID = 1
_USERNAME = "Anony Mous"
_BIRTHDAY = int(datetime(year=2000, month=1, day=1).timestamp())
_GENDER = "o"
_DATETIME = int(datetime(year=2020, month=1, day=1).timestamp() * 1000)
_TRANSLATION_X = -1.5
_TRANSLATION_Y = -1.0
_TRANSLATION_Z = -0.5
_ROTATION_X = 0.0
_ROTATION_Y = 0.5
_ROTATION_Z = 1.0
_ROTATION_W = 1.5
_C_HEIGHT = 3
_C_WIDTH = 3
_C_DATA = 27 * b'a'
_C_PATH = 'color.jpg'
_D_WIDTH = 3
_D_HEIGHT = 3
_D_DATA = 9 * [0.5]
_D_PATH = 'depth.jpg'
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