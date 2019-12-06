import datetime
import time
import struct
_STR_FORMAT = "{0} user {1}: {2}"


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = int(user_id)
        self.timestamp = timestamp  # a datetime object
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, timestamp={self.timestamp!r}, '\
                + f'thought="{self.thought}")'

    def __str__(self):
        formatted_time = f'[{self.timestamp}]'
        return _STR_FORMAT.format(formatted_time, self.user_id, self.thought)

    def __eq__(self, other):
        if not type(self) == type(other):
            return False
        if not self.user_id == other.user_id:
            return False
        if not self.timestamp == other.timestamp:
            return False
        return self.thought == other.thought

    def serialize(self):
        time_in_secs = time.mktime(self.timestamp.timetuple())
        b_user = struct.pack("Q", self.user_id)
        b_time = struct.pack("Q", int(time_in_secs))
        b_tht = self.thought.encode("utf-8")
        b_len = struct.pack("I", len(b_tht))
        return b_user + b_time + b_len + b_tht

    def deserialize(data):
        user_id, time, m_len = struct.unpack("QQI", data[:20])
        timestamp = datetime.datetime.fromtimestamp(time)
        thought = data[20:].decode("utf-8")
        return Thought(user_id, timestamp, thought)
