from blinker import signal
from extendable_json import extendable_json as json
from json import JSONDecodeError
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import ClientFactory, Factory, Protocol
import os


class ULCLoggingProtocol(Protocol):
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


class ULCLoggingProtocolClientFactory(ClientFactory):
    def __init__(self, application_name):
        super().__init__()
        self.protocol = None
        self.application_name = application_name

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
        self.updateServer()

    def connectionLost(self):
        pass

    def updateServer(self):
        computername = os.environ['COMPUTERNAME']
        self.sendLog({"ULC": "CLIENT_UPDATE",
                               "computername": computername,
                               "application": self.application_name
                               })

    def buildProtocol(self, addr):
        self.protocol = ULCLoggingProtocol(factory=self)
        return self.protocol


class ULCLoggingProtocolServerFactory(Factory):
    def __init__(self):
        self.onConnectionMade = signal('ULC_onConnectionMade')
        self.onConnectionLost = signal('ULC_onConnectionLost')
        self.onDataReceived = signal('ULC_onDataReceived')

    def dataReceived(self, protocol, data):
        try:
            j_data = json.loads(data)
        except JSONDecodeError:
            j_data = {'error': 'Received malformed message'}
        self.onDataReceived.send(protocol, **j_data)

    def connectionMade(self, protocol):
        self.onConnectionMade.send(protocol)

    def connectionLost(self, protocol, reason):
        self.onConnectionLost.send(protocol, reason=reason)

    def buildProtocol(self, addr):
        return ULCLoggingProtocol(factory=self)
