from loguru._logger import Logger  # noqa: _logger
from loguru import logger as loguru_logger

from quicorn.logger.formatter import Colors, StrFormatter

__all__: list[str] = ['logger', 'Colors', 'StrFormatter']

logger: Logger = loguru_logger.opt(colors=True)
