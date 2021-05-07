from uls.api import LoggingHandler


class BufferedLogHandler(LoggingHandler):
    """BufferedLogHandler
    Creates a buffered layer for the given handler.
    If the handler is unable to write its log msg, the msg will be buffered.
    Any time a write to the handler is called, it will attempt to clear the buffer
    to the handler.
    Arguments:
    @:param
    handler - Log Handler this will buffer for.
    """
    def __init__(self, handler):
        self._handler = handler
        self._buffer = BufferedHandler()

    def is_empty(self):
        """is_empty
        Returns whether the buffer is empty, or if there is buffered data.
        """
        return self._buffer.empty()

    def insert_log(self, data):
        """insert_log
        Write to log handler. This will first try to write any buffered data.
        it will then try to have handler write log msg. If it fails, the data
        will be buffered.
        """
        if not self.is_empty():
            self._buffer.dump(self._handler)
        if self._handler.insert_log(data):
            return True
        else:
            self._handler.insert_log(data)
            return False


class BufferedHandler(LoggingHandler):
    """BufferedHandler
    Stores Log Entries in a buffer to be later used.
    """
    def __init__(self):
        self._buffer = []

    def is_empty(self):
        """is_empty
        returns whether there is data in the buffer.
        """
        if self._buffer:
            return False
        return True

    def dump(self, handler):
        """dump
        This will try to push the buffered data into the given handler.
        @:param
        handler: The Log Handler this buffer should try to dump to.
        """
        while not self.is_empty():
            msg = self._buffer.pop()
            if not handler.insert_log(msg):
                self._buffer.push(msg)
                break

    def insert_log(self, data):
        """insert_log
        Insert structured log data into the buffer
        @:param
        data: Structured log data
        """
        self._buffer.append(data)

    def buffered_data(self):
        """buffered_data
        This can be used to iterate over all the buffered data.
        """
        for data in self._buffer:
            yield data
