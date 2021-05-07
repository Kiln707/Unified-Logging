
class LoggingHandler:
    """LoggingHandler
    Parent class for logging handlers for use by Unified Logging Server.
    Extend this class to create a custom class.
    """
    def initialize(self):
        """initialize
        Initialization for handler. Use this method to create connections to databases, open file handlers, etc.
        """
        pass

    def insert_log(self, data):
        """insert_log
        Insert structured log data into the storage of this handler
        @:param
        data - A dict containing structured Log data.
        """
        pass
