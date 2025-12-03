from collections.abc import Callable
from contextlib import AbstractAsyncContextManager

type LifespanType[AppType] = Callable[[AppType], AbstractAsyncContextManager[None]]
