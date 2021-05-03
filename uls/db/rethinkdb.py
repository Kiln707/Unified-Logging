from rethinkdb import RethinkDB as r


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
        self._session = r.connect(self._host,
                                  self._port,
                                  self._db,
                                  self._username,
                                  self._password,
                                  self._timeout,
                                  self._ssl)

    def close(self):
        self._session.close()

    def prepare_database(self):
        tables = r.table_list().run(self._session)
        if 'logs' not in tables:
            r.table_create('logs').run(self._session)

    def insert_log(self, data):
        r.table('logs').insert(data).run(self._session)
