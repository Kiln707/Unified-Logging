
class Aggregator:
    def __init__(self):
        self.clients = {}
        self.outputs = []
        self.log = None

    def new_peer(self, connection):
        self.clients[connection.getPeer()] = {'connection': connection}

    def remove_peer(self, connection):
        self.clients.pop(connection.getPeer())

    def update_peer(self, connection, **data):
        self.clients[connection.getPeer()].update(data)

    def receive_log(self, connection, **msg):
        client = self.clients[connection.getPeer()]
        computer_name = client['computer_name']
        application = client['application']
        event = msg.pop('event')
        self.log.msg(event, computer_name=computer_name, application=application, **msg)
