from datetime import datetime
from twisted.internet.protocol import ClientFactory, Factory, Protocol
from twisted.internet.error import ConnectionDone
from json import JSONDecodeError

from extendable_json import extendable_json as json


class ULSLoggingProtocol(Protocol):
    def __init__(self, factory):
        self._factory = factory
        self._peer = None

    def sendData(self, data):
        self.transport.write(data.encode('UTF-8'))

    def dataReceived(self, data):
        self._factory.dataReceived(self, data.decode('UTF-8'))

    def connectionLost(self, reason=ConnectionDone):
        self._factory.connectionLost(self, reason)

    def connectionMade(self):
        self._peer = self.transport.getPeer()
        self._factory.connectionMade(protocol=self)

    def getPeer(self):
        return self._peer

    def disconnect(self):
        """disconnect
        Close the connection to/from the logging server.
        """
        self.transport.loseConnection()


class ULSLoggingProtocolClientFactory(ClientFactory):
    def __init__(self):
        super().__init__()
        self.protocol = None

    def sendLog(self, data):
        """sendLog
        Send structured log data to Unified Logging Server
        """
        if not self.protocol:
            return
        j_data = json.dumps(data)
        self.protocol.sendData(j_data)

    def connectionMade(self, protocol):
        self.protocol = protocol

    def buildProtocol(self, addr):
        self.protocol = ULSLoggingProtocol(factory=self)
        return self.protocol


class ULSLoggingProtocolServerFactory(Factory):
    def __init__(self, callback):
        self._callback = callback

    def dataReceived(self, protocol, data):
        try:
            j_data = json.loads(data.decode('UTF-8'))
        except JSONDecodeError:
            j_data = {'error': 'Received malformed message'}
        self._callback(j_data, protocol)

    def connectionMade(self, protocol):
        j_data = {
            'connection_made': protocol.getPeer(),
        }
        self._callback(j_data, protocol)

    def connectionLost(self, protocol, reason):
        j_data = {
            'Connection lost': protocol.getPeer(),
            'reason': reason
        }
        self._callback(j_data, protocol)

    def buildProtocol(self, addr):
        return ULSLoggingProtocol(factory=self)
