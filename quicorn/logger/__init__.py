from types import TracebackType

from loguru._logger import Logger  # noqa: _logger
from loguru import logger as loguru_logger

from pydantic import BaseModel

from quicorn.logger._formatter import StrFormatter

__all__: list[str] = ['logger', 'formatter', 'DEFAULT_OPTIONS']

type ExcInfo = tuple[type[BaseException] | None, BaseException | None, TracebackType | None]


class LoguruOptions(BaseModel, arbitrary_types_allowed=True):
    exception: bool | ExcInfo | BaseException | None = None
    record: bool = False
    lazy: bool = False
    colors: bool = False
    raw: bool = False
    capture: bool = True
    depth: int = 0
    ansi: bool = False


DEFAULT_OPTIONS: LoguruOptions = LoguruOptions(colors=True)

logger: Logger = loguru_logger.opt(**DEFAULT_OPTIONS.model_dump(exclude_defaults=True))
formatter: StrFormatter = StrFormatter()
