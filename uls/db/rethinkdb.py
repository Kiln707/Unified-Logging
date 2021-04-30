from subprocess import Popen
import sys
from os import path


class RethinkDBService:
    WINDOWS_RDB_EXE = path.join(path.abspath(path.dirname(sys.modules['__main__'].__file__)), 'assets', 'rethinkdb.exe')

    def __init__(self):
        self._process = None

    def start(self):
        print(self.WINDOWS_RDB_EXE)
        # self._process = Popen()
