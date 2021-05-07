from datetime import datetime
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.error import ConnectionDone
from json import JSONDecodeError

from extendable_json import extendable_json as json


class UHSLoggingProtocol(Protocol):
    def __init__(self, factory):
        self._factory = factory
        self._peer = None

    def sendData(self, data):
        self.transport.write(data)

    def dataReceived(self, data):
        self._factory.dataReceived(self, data)

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


class UHSLoggingProtocolClientFactory(Factory):
    def __init__(self):
        self.protocol = None

    def sendLog(self, data):
        """sendLog
        Send structured log data to Unified Logging Server
        """
        j_data = json.dumps(data)
        self.protocol.sendData(j_data)

    def buildProtocol(self, addr):
        self.protocol = UHSLoggingProtocol(factory=self)
        return self.protocol


class UHSLoggingProtocolServerFactory(UHSLoggingFactoryMixin, Factory):
    def __init__(self, callback):
        self._callback = callback

    def dataReceived(self, protocol, data):
        try:
            j_data = json.loads(data)
        except JSONDecodeError:
            j_data = {'time': datetime.utcnow(),
                      'event': 'Generic Log Event',
                      'peer': protocol.getPeer(),
                      'msg': data.decode('UTF-8')
                      }
        if 'peer_ip' not in j_data:
            j_data['peer_ip'] = protocol.getPeer()
        self._callback(j_data)

    def connectionMade(self, protocol):
        j_data = {
            'time': datetime.utcnow(),
            'event': 'Connection Made',
            'peer': protocol.getPeer(),
        }
        self._callback(j_data)

    def connectionLost(self, protocol, reason):
        j_data = {
            'time': datetime.utcnow(),
            'event': 'Connection lost',
            'peer': protocol.getPeer(),
            'reason': reason
        }
        self._callback(j_data)

    def buildProtocol(self, addr):
        return UHSLoggingProtocol(factory=self)
