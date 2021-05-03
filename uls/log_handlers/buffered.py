from uls.api import LoggingHandler


class BufferedLogHandler(LoggingHandler):
    def __init__(self):
        self._buffer = []

    def initialize(self):
        pass

    def insert_log(self, data):
        self._buffer.append(data)

    def buffered_data(self):
        for data in self._buffer:
            yield data
