from api.network import ULCLoggingProtocolServerFactory
from structlog import getLogger
from configuration import get_configuration
from server import Aggregator


class UnifiedLoggingCenter:
    def __init__(self):
        self.log = getLogger()
        self.log.msg('Starting up server.')
        self.web = None
        self.log.msg('Started web server.')
        self.aggregator = Aggregator()
        self.log.msg('Started Aggregator.')
        self.network = None
        self.log.msg('Gathering configuration')
        self.config = get_configuration()
        self.log.msg('Gathered configuration')
        self.reactor = None

    def initialize(self):
        self.log.msg("Begin Initialization of Unified Logging Server.")
        from twisted.internet import reactor
        self.log.msg("Preparing network.")
        self.reactor = reactor
        self.network = ULCLoggingProtocolServerFactory()
        self.network.onConnectionMade.connect(self.aggregator.new_peer)
        self.network.onConnectionLost.connect(self.aggregator.remove_peer)
        self.network.onDataReceived.connect(self.data_received)
        self.aggregator.log = self.log
        port = self.config.valueOf('port', default=8123, type_=int)
        self.log.msg("Aggregator is listening on port: %s" % port)
        self.reactor.listenTCP(port, self.network)
        self.log.msg("Unified Logging Server initialized. Ready to start")

    def data_received(self, connection, **data):
        self.log.msg("Data Received", connection=connection.getPeer(), data=data)
        self.log.msg('aggregator status', clients=self.aggregator.clients)
        if 'ULC' in data:
            if data['ULC'] == 'CLIENT_UPDATE':
                computername = data['computername']
                application = data['application']
                self.aggregator.update_peer(connection, computer_name=computername, application=application)
        else:
            self.aggregator.receive_log(connection, **data)

    def run(self):
        self.log.msg("Starting Server...")
        self.reactor.run()


if __name__ == '__main__':
    server = UnifiedLoggingCenter()
    server.initialize()
    server.run()
