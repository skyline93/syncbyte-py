class SyncByteException(Exception):
    pass


class NotSupport(SyncByteException):
    pass


class DumpFailed(SyncByteException):
    pass
