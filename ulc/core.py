from api.network import ULSLoggingProtocolServerFactory
from server import Log
from configuration import get_configuration


class UnifiedLoggingCenter:
    def __init__(self):
        self.log = Log()
        self.web = None
        self.log.msg("Setup", msg='Starting up server, gathering configuration')
        self.config = get_configuration()
        self.log.msg("Setup", msg='Gathered configuration')
        self.reactor = None

    def initialize(self):
        self.log.msg("Initialization", msg="Begin Initialization of Unified Logging Server.")
        self.log.initialize(self.config)
        from twisted.internet import reactor
        self.reactor = reactor
        self.reactor.listenTCP(self.config.valueOf('port', default=8123, type_=int),
                               ULSLoggingProtocolServerFactory(self.log))
        self.log.msg("Initialization", msg="Unified Logging Server initialized. Ready to start")

    def run(self):
        self.log.msg("Start", msg="Starting Server...")
        self.reactor.run()


if __name__ == '__main__':
    server = UnifiedLoggingServer()
    server.initialize()
    server.run()
