from pykit.logger import BasicLogger

_log = None


def Logger() -> BasicLogger:
    global _log
    if _log is None:
        _log = BasicLogger.get_logger()
    return _log


def SetLogger(log: BasicLogger):
    global _log
    _log = log
