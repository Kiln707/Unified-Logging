from db import RethinkDBService


class UnifiedLoggingServer:
    def __init__(self):
        self.db_service = None

    def initialize(self):
        self.db_service = RethinkDBService()
        self.db_service.start()

    def run(self):
        pass


if __name__ == '__main__':
    server = UnifiedLoggingServer()
    server.initialize()
    server.run()
