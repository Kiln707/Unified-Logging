
class Buffer:
    def __init__(self):
        self._buffer = []

    def msg(self, **msg):
        self._buffer.append(msg)

    def dump(self, f):
        for msg in self._buffer:
            f(msg)

    def is_empty(self):
        if self._buffer:
            return False
        return True
