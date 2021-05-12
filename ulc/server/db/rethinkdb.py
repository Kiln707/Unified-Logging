from rethinkdb import RethinkDB as r
from uls.api import LoggingHandler


class RethinkdbConnection(LoggingHandler):
    def __init__(self, host='localhost', port=28015, db='test', username='admin', password='', timeout='', ssl=None):
        self._session = None
        self._host = host
        self._port = port
        self._db = db
        self._username = username
        self._password = password
        self._timeout = timeout
        self._ssl = ssl

    def connect(self):
        self._session = r.connect(self._host,
                                  self._port,
                                  self._db,
                                  self._username,
                                  self._password,
                                  self._timeout,
                                  self._ssl)

    def close(self):
        self._session.close()

    def initialize(self):
        tables = r.table_list().run(self._session)
        if 'logs' not in tables:
            r.table_create('logs').run(self._session)

    def insert_log(self, data):
        try:
            r.table('logs').insert(data).run(self._session)
            return True
        except:
            return False
