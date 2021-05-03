
class RethinkdbConnection:
    def __init__(self, host, port, db, username, password, timeout='', ssl=None):
        self._session = None
        self._host = host
        self._port = port
        self._db = db
        self._username = username
        self._password = password
        self._timeout = timeout
        self._ssl = ssl

    def connect(self):
        self._session = ''
