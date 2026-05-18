"""Structlog compatibility shim — falls back to stdlib logging when structlog not installed."""
import logging as _logging

try:
    import structlog as _structlog
    def get_logger(name: str | None = None):
        return _structlog.get_logger(name) if name else _structlog.get_logger()
    _using_structlog = True
except ImportError:
    _using_structlog = False

    class _StdlibAdapter:
        def __init__(self, logger):
            self._logger = logger

        def info(self, event, **kw):
            self._logger.info(f"{event} {kw}" if kw else event)

        def debug(self, event, **kw):
            self._logger.debug(f"{event} {kw}" if kw else event)

        def warning(self, event, **kw):
            self._logger.warning(f"{event} {kw}" if kw else event)

        def warn(self, event, **kw):
            self._logger.warning(f"{event} {kw}" if kw else event)

        def error(self, event, **kw):
            self._logger.error(f"{event} {kw}" if kw else event)

        def exception(self, event, **kw):
            self._logger.exception(f"{event} {kw}" if kw else event)

    def get_logger(name: str | None = None):
        logger = _logging.getLogger(name or "mios")
        if not logger.handlers:
            _logging.basicConfig(level=_logging.INFO,
                                  format="%(levelname)s %(name)s %(message)s")
        return _StdlibAdapter(logger)
