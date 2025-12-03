from typing import Annotated
from typing_extensions import Doc

from quicorn.types import LifespanType

type AppType = QuicApp


class QuicApp:
    def __init__(
        self: AppType,
        *,
        title: Annotated[
            str,
            Doc(
                """
                Title of the application
                """
            ),
        ],
        lifespan: Annotated[
            LifespanType[AppType],
            Doc(
                """
                `Lifespan` manages app resources, running code on startup and shutdown.
                """
            ),
        ],
    ) -> None:
        self.title: str = title
        self.lifespan: LifespanType[AppType] = lifespan
