from .buffer import Buffer
from .processors import TimeStamper


class Log:
    """Log
    Log object directs flow of incoming logs, to be properly formatted and forwarded to various loggers.
    """
    def __init__(self):
        self.buffer = Buffer()
        self._initialized = False
        self._processors = []
        self._loggers = []
        self._handles = {}

    def initialize(self, configuration, processors=[], loggers=[]):
        self._processors.append(TimeStamper())
        self._initialized = True

    def add_handle(self, peer, information):
        pass

    def remove_handle(self, peer):
        pass

    def _process(self, event_dict):
        for processor in self._processors:
            print(processor)
            print(processor(self, '', event_dict))
            event_dict = processor(self, '', event_dict)
        return event_dict

    def msg(self, event, **msg):
        if not self._initialized:
            self.buffer.msg(**msg)
            print(msg)
            return
        msg['event'] = event
        msg = self._process(msg)
