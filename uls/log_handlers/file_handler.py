from uls.api import LoggingHandler


class FileHandler(LoggingHandler):
    def __init__(self, file_location):
        self._location = file_location
        self._file_handle = None

    def initialize(self):
        self._file_handle = open(self._location, 'w+')

    def insert_log(self, data):
        try:
            self._file_handle.write(str(data))
            return True
        except:
            return False
