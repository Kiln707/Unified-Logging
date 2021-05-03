from uls.api.network import UHSLoggingProtocolServerFactory
from uhs.simpleconfig import simpleconfig

class LoggingServer:
    def __init__(self):
        from twisted.internet import reactor
        self.reactor = reactor
        self.config = simpleconfig.load_or_create()

    def run(self):
        self.reactor.run()




if __name__ == '__main__':
    pass