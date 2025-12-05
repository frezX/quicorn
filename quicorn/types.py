from signal import Signals
from asyncio import AbstractEventLoop
from collections.abc import Callable, Awaitable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Annotated, TypedDict, Literal, Protocol, NotRequired, Any, runtime_checkable

from pydantic import BeforeValidator, conint
from pydantic_core import PydanticCustomError


# Base
def aligned_int_validator(value: int) -> int:
    if value & (value - 1) != 0:
        raise PydanticCustomError('aligned_int_type', 'value must be a power of two (2^n)')
    return value


type AlignedInt = Annotated[conint(ge=2**16), BeforeValidator(func=aligned_int_validator)]


class Sentinel:
    __slots__: tuple[str, ...] = tuple()


class SentinelContextManager(Sentinel):
    __slots__: tuple[str, ...] = tuple()

    def __enter__(self) -> None: ...

    def __exit__(self, *excinfo) -> None: ...

    async def __aenter__(self) -> None: ...

    async def __aexit__(self, *excinfo) -> None: ...


# Graceful
type LoopFactory = Callable[[], AbstractEventLoop]
type SignalCallbackType = Callable[[Signals], None]


# QSGI
class QuicScope(TypedDict):
    type: Literal['quic']
    quic_version: str


class LifespanScope(TypedDict):
    type: Literal['lifespan']
    state: NotRequired[dict[str, Any]]


type Scope = QuicScope | LifespanScope


class QuicConnectEvent(TypedDict):
    type: Literal['quic.connect']


class QuicAcceptEvent(TypedDict):
    type: Literal['quic.accept']


class QuicReceiveEvent(TypedDict):
    type: Literal['quic.receive']
    bytes: bytes


class QuicSendEvent(TypedDict):
    type: Literal['quic.send']
    bytes: bytes


class QuicDisconnectEvent(TypedDict):
    type: Literal['quic.disconnect']
    code: int
    reason: NotRequired[str]


class QuicCloseEvent(TypedDict):
    type: Literal['quic.close']
    code: NotRequired[int]
    reason: NotRequired[str]


class LifespanStartupEvent(TypedDict):
    type: Literal['lifespan.startup']


class LifespanShutdownEvent(TypedDict):
    type: Literal['lifespan.shutdown']


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal['lifespan.startup.complete']


class LifespanStartupFailedEvent(TypedDict):
    type: Literal['lifespan.startup.failed']
    message: str


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal['lifespan.shutdown.complete']


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal['lifespan.shutdown.failed']
    message: str


type QSGIReceiveEvent = (
    QuicConnectEvent |
    QuicReceiveEvent |
    QuicDisconnectEvent |
    LifespanStartupEvent |
    LifespanShutdownEvent
)
type QSGISendEvent = (
    QuicAcceptEvent |
    QuicSendEvent |
    QuicCloseEvent |
    LifespanStartupCompleteEvent |
    LifespanStartupFailedEvent |
    LifespanShutdownCompleteEvent |
    LifespanShutdownFailedEvent
)

# QSGI Callable
type QSGIReceiveCallable = Callable[[], Awaitable[QSGIReceiveEvent]]
type QSGISendCallable = Callable[[QSGISendEvent], Awaitable[None]]

# QSGI Application
if TYPE_CHECKING:
    type QSGIApplication = Callable[[Scope, QSGIReceiveCallable, QSGISendCallable], Awaitable[None]]
else:
    @runtime_checkable
    class QSGIApplication(Protocol):
        async def __call__(self, /, *, scope: Scope, receive: QSGIReceiveCallable, send: QSGISendCallable) -> None: ...


# Lifespan
type Lifespan[AppType: QSGIApplication] = Callable[[AppType], AbstractAsyncContextManager[None]]
