from api.network import UHSLoggingProtocolServerFactory
from .configuration import get_configuration


class UnifiedLoggingServer:
    def __init__(self):
        self.config = get_configuration()
        self.reactor = None
        self.log_handlers = []

    def initialize(self):
        from twisted.internet import reactor
        self.reactor = reactor
        self.reactor.listenTCP(8123, UHSLoggingProtocolServerFactory(self.log))

        

    def add_handler(self, handle):
        self.log_handlers.append(handle)

    def log(self, msg):
        print(msg)
        for handler in self.log_handlers:
            handler(msg)

    def run(self):
        self.reactor.run()


if __name__ == '__main__':
    server = UnifiedLoggingServer()
    server.initialize()
    server.run()
