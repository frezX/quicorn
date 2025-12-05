from time import perf_counter
from dataclasses import dataclass
from contextvars import ContextVar

__all__: list[str] = ['Timer', 'TimerData']


@dataclass
class TimerData:
    start: float | None = None
    finish: float | None = None
    duration: float | None = None


class Timer:
    def __init__(self, *, data: ContextVar[TimerData]) -> None:
        self.data: ContextVar[TimerData] = data

    async def __aenter__(self) -> None:
        self.data.set(TimerData(start=perf_counter()))

    async def __aexit__(self, *args) -> None:
        data: TimerData = self.data.get()
        data.finish = perf_counter()
        data.duration = data.finish - data.start
