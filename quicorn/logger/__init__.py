from loguru._logger import Logger  # noqa: _logger
from loguru import logger as loguru_logger

from quicorn.logger._formatter import StrFormatter

__all__: list[str] = ['logger', 'formatter']

logger: Logger = loguru_logger.opt(colors=True)
formatter: StrFormatter = StrFormatter()
