import time
import struct
import threading
import pathlib
import os
from .utils import listener as lsn


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
        msg = self.connection.receive(1024)

        user_id, formatted_time, thought = self.parse_message(msg)
        dir_address = os.path.join(self.data_dir, str(user_id))
        time_with_end = formatted_time + ".txt"
        file_address = os.path.join(self.data_dir, str(user_id), time_with_end)
        print("file address: {0}".format(file_address))
        dir_path = pathlib.Path(dir_address)
        file_path = pathlib.Path(file_address)
        self.lock.acquire()
        if not dir_path.is_dir():
            # If the directory or its parent directories don't exist,
            # they are generated.
            dir_path.mkdir(parents=True)
        if not file_path.is_file():
            file_path.touch()
            print(file_path.is_file())
            print("Made file {0}".format(file_path))
        # Write the thought to the file in append mode
        # so that you don't run over previous lines.
        with file_path.open("a") as f:
            if not self.file_is_empty(file_path):
                # File is not empty, we need to add a new line.
                f.write("\n")
            f.write(thought)
        self.lock.release()
        self.connection.close()

    def parse_message(self, message):
        """
        Recieves a message in bytes and converts it
        into the corresponding id, time and text.
        """
        user_id, cur_time, m_size = struct.unpack("QQI", message[:20])
        thought = message[20:].decode("utf-8")
        # cur time is converted from seconds since epoch
        # to a time struct and then to a nice printable format.
        local_time = time.localtime(cur_time)
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)

        if not m_size == len(message[20:]):
            raise Exception("Incomplete data")
        print("{0}, {1}, {2}".format(user_id, formatted_time, thought))
        return user_id, formatted_time, thought

    def file_is_empty(self, path):
        """
        Recieves a path object that points to a file
        and returns whether or not it's empty.
        """
        return os.stat(path).st_size == 0
