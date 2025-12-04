from signal import Signals
from asyncio import AbstractEventLoop
from collections.abc import Callable, Awaitable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING, Literal, Protocol, runtime_checkable

from pydantic import BaseModel

# Graceful

type LoopFactory = Callable[[], AbstractEventLoop]
type SignalCallbackType = Callable[[Signals], None]

# QSGI Event


class QSGIEvent(BaseModel):
    type: str


class QSGISendEvent(QSGIEvent):
    type: Literal['quic.send']


class QSGIReceiveEvent(QSGIEvent):
    type: Literal['quic.receive']


type Event = QSGIEvent | QSGISendEvent | QSGIReceiveEvent

# QSGI Scope


class QSGIScope(BaseModel):
    type: str


type Scope = QSGIScope

# QSGI Callable

type QSGIReceive = Callable[[], Awaitable[QSGIReceiveEvent]]

type Receive = QSGIReceive

type QSGISend = Callable[[QSGISendEvent], Awaitable[None]]

type Send = QSGISend

# QSGI Application

if TYPE_CHECKING:
    type QSGIApplication = Callable[[Scope, Receive, Send], Awaitable[None]]
else:
    @runtime_checkable
    class QSGIApplication(Protocol):
        async def __call__(self, /, *, scope: Scope, receive: Receive, send: Send) -> None: ...


# Lifespan


type Lifespan[AppType: QSGIApplication] = Callable[[AppType], AbstractAsyncContextManager[None]]
