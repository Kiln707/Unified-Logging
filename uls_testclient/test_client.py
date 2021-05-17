from ulc.api import ULCLoggingProtocolClientFactory
from twisted.internet.task import LoopingCall


class ULSTestClient:
    def __init__(self):
        self.reactor = None
        self.network_connection = None

    def initialize(self):
        from twisted.internet import reactor
        self.reactor = reactor
        self.network_connection = ULCLoggingProtocolClientFactory(application_name='Test Client')
        self.reactor.connectTCP('localhost', 8123, self.network_connection)
        lc = LoopingCall(self.timed_test)
        lc.start(1)

    def timed_test(self):
        data = {'event': 'test Event', 'test': 'asdfasdkfjasdf'}
        self.network_connection.sendLog(data)

    def run(self):
        self.reactor.run()


if __name__ == "__main__":
    client = ULSTestClient()
    client.initialize()
    client.run()
