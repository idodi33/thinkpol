import datetime
from . import connection as cn
from . import thought as tht


def upload_thought(address, user, thought):
    # Form the message according to the protocol.
    thought_obj = tht.Thought(user, datetime.datetime.now(), thought)
    msg = thought_obj.serialize()
    if type(address) == str:
        ip, port = address.split(':')
    else: # it's a tuple
        ip, port = address
    with cn.Connection.connect(ip, int(port)) as connection:
        connection.send(msg)
