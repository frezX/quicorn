from contextlib import suppress
from functools import wraps, partial
from typing import TypeGuard, Any, overload
from collections.abc import Awaitable, Callable
from concurrent.futures import ThreadPoolExecutor
from contextvars import Context, ContextVar, copy_context
from asyncio import Task, AbstractEventLoop, Semaphore, get_running_loop, iscoroutinefunction

from quicorn.graceful import TASKS
from quicorn.logger import logger, formatter
from quicorn.types import Sentinel, SentinelContextManager

from quicorn.graceful.timer import Timer, TimerData

__all__: list[str] = ['run_in_background']

type Func[**P, R] = Callable[P, Awaitable[R]] | Callable[P, R]
type Wrapper[**P, R] = Callable[P, Task[R]]
type OuterWrapper[**P, R] = Callable[[Func[P, R]], Wrapper[P, R]]
type Builder[**P, R] = Wrapper[P, R] | OuterWrapper[P, R]

_func: Sentinel = Sentinel()
_semaphore: SentinelContextManager = SentinelContextManager()

waiting_timer_data_var: ContextVar[TimerData] = ContextVar('quicorn.timer.waiting', default=TimerData())
execution_timer_data_var: ContextVar[TimerData] = ContextVar('quicorn.timer.execution', default=TimerData())

executor: ThreadPoolExecutor = ThreadPoolExecutor(thread_name_prefix='quicorn.background')


def _is_func[**P, R](_func: Any) -> TypeGuard[Func[P, R]]:
    return callable(_func)


@overload
def run_in_background[**P, R](_func: Func[P, R], *, semaphore: Semaphore = _semaphore) -> Wrapper[P, R]: ...
@overload
def run_in_background[**P, R](*, semaphore: Semaphore = _semaphore) -> OuterWrapper[P, R]: ...


def run_in_background[**P, R](_func: Func[P, R] = _func, *, semaphore: Semaphore = _semaphore) -> Builder[P, R]:
    def callback(task: Task[R]) -> None:
        name: str = task.get_name()
        waiting_data: TimerData = waiting_timer_data_var.get()
        execution_data: TimerData = execution_timer_data_var.get()
        if execution_data.duration is not None:
            duration: str = f'execution duration: <lr>{execution_data.duration:.3f} s</lr>'
        elif waiting_data.duration is not None:
            duration: str = f'waiting duration: <lr>{waiting_data.duration:.3f} s</lr>'
        else:
            duration: str = 'unknown duration'
        with suppress(ValueError):
            TASKS.remove(task)
        if task.cancelled():
            logger.warning(formatter.join(f'Background task <m>`{name}`</m> has been canceled', duration))
        elif exc := task.exception():
            logger.exception(
                formatter.join(f'Background task <c>`{name}`</c> completed with error', formatter.escape(exc), duration)
            )
        else:
            logger.success(formatter.join(f'Background task <e>`{name}`</e> completed successfully', duration))

    def builder(func: Func[P, R]) -> Wrapper[P, R]:
        @wraps(wrapped=func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> Task[R]:
            async def run_func() -> R:
                async with Timer(data=waiting_timer_data_var), semaphore, Timer(data=execution_timer_data_var):
                    if iscoroutinefunction(func=func):
                        return await func(*args, **kwargs)
                    return await loop.run_in_executor(executor, partial(func, **kwargs), *args)

            context: Context = copy_context()
            loop: AbstractEventLoop = get_running_loop()
            task: Task[R] = loop.create_task(run_func(), name=func.__name__, context=context)
            task.add_done_callback(callback, context=context)
            TASKS.append(task)
            return task

        return wrapper

    return builder(func=_func) if _is_func(_func) else builder
