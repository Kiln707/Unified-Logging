from datetime import datetime
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.error import ConnectionDone

from uhs.extendable_json import extendable_json as json


class UHSLoggingProtocol(Protocol):
    def __init__(self, factory):
        self._factory = factory
        self._peer = None

    def sendData(self, data):
        self.transport.write(data)

    def dataReceived(self, data):
        self._factory.data_received(data)

    def connectionLost(self, reason=connectionDone):
        self._factory.connectionLost(self, reason)

    def connectionMade(self):
        self._peer = self.transport.getPeer()
        self._factory.data_received('Connection Made, remote: %s' % self._peer)

    def getPeer(self):
        return self._peer

    def disconnect(self):
        """disconnect
        Close the connection to/from the logging server.
        """
        self.transport.loseConnection()


class UHSLoggingFactoryMixin:
    def __init__(self, logger):
        self._logger = logger

    def dataReceived(self, protocol, data):
        j_data = json.loads(data)
        if 'peer_ip' not in j_data:
            j_data['peer_ip'] = protocol.getPeer()
        self._logger.handle(j_data)

    def connectionMade(self, protocol):
        j_data = {
            'time': datetime.utcnow(),
            'event': 'Connection Made',
            'peer': protocol.getPeer(),
        }
        self._logger.handle(j_data)

    def connectionLost(self, protocol, reason):
        j_data = {
            'time': datetime.utcnow(),
            'event': 'Connection lost',
            'peer': protocol.getPeer(),
            'reason': reason
        }
        self._logger.handle(j_data)


class UHSLoggingProtocolClientFactory(Factory, UHSLoggingFactoryMixin):
    def buildProtocol(self, addr):
        return UHSLoggingProtocol(factory=self)


class UHSLoggingProtocolServerFactory(Factory, UHSLoggingFactoryMixin):
    def buildProtocol(self, addr):
        return UHSLoggingProtocol(factory=self)