from api.network import UHSLoggingProtocolServerFactory
from configuration import get_configuration
from log_handlers import BufferedLogHandler


class UnifiedLoggingServer:
    def __init__(self):
        self._buffer = BufferedLogHandler()
        self.config = get_configuration()
        self.reactor = None
        self.log_handlers = []

    def initialize(self):
        from twisted.internet import reactor
        self.reactor = reactor
        self.reactor.listenTCP(self.config.valueOf('port', default=8123, type_=int),
                               UHSLoggingProtocolServerFactory(self.log))
        self.configure_handlers()

    def configure_handlers(self):
        for log_type, data in self.config.valueOf('logging').items():
            if log_type == "file":
                from uls.log_handlers.file_handler import FileHandler
                self.add_handler(FileHandler(file_location=data['file_location']))
            elif log_type == "db":
                pass
        for handle in self.log_handlers:
            handle.initialize()

    def add_handler(self, handle):
        self.log_handlers.append(BufferedLogHandler(handle))

    def _write_buffer(self):
        if self._buffer:
            for msg in self._buffer:
                self._write_log(msg)

    def _write_log(self, msg):
        log_success = 0
        for handler in self.log_handlers:
            if handler.insert_log(msg):
                log_success += 1
        return log_success

    def log(self, msg):
        if not self.log_handlers:
            self._buffer.insert_log(msg)
            return False
        self._write_buffer()
        if not self._write_log(msg):
            self._buffer.insert_log(msg)

    def run(self):
        self.reactor.run()


if __name__ == '__main__':
    server = UnifiedLoggingServer()
    server.initialize()
    server.run()
