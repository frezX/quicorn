from typing import Any
from signal import Signals
from collections.abc import Iterable
from asyncio import Task, Event, AbstractEventLoop, gather, new_event_loop

from quicorn.types import SignalCallbackType

from quicorn.logger import logger

__all__: list[str] = [
    'TASKS',
    'SHUTDOWN_EVENT',
    'add_signals_handler',
    'event_loop_factory',
    'wait_for_shutdown',
]

TASKS: list[Task[Any]] = []
SHUTDOWN_EVENT: Event = Event()


def shutdown_callback(signal: Signals) -> None:
    logger.info(f'Shutdown signal: <r>`{signal.name}(<lr>{signal.value}</lr>)`</r>')
    SHUTDOWN_EVENT.set()


def add_signals_handler(loop: AbstractEventLoop, callback: SignalCallbackType, signals: Iterable[Signals]) -> None:
    for signal in signals:
        loop.add_signal_handler(signal, callback, signal)


def event_loop_factory() -> AbstractEventLoop:
    loop: AbstractEventLoop = new_event_loop()
    add_signals_handler(loop=loop, callback=shutdown_callback, signals=(Signals.SIGINT, Signals.SIGTERM))
    return loop


async def wait_for_shutdown(return_exceptions: bool = True) -> None:
    await SHUTDOWN_EVENT.wait()
    await gather(*TASKS, return_exceptions=return_exceptions)
