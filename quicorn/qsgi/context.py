from asyncio import Queue

from contextvars import ContextVar

qsqi_queue_var: ContextVar[Queue] = ContextVar('QSQI_QUEUE', default=Queue())
