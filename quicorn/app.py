from typing import Annotated
from typing_extensions import Doc

from quicorn.types import Scope, Receive, Send, QSGIApplication, Lifespan


class QuicApp[AppType: QSGIApplication]:
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
            Lifespan[AppType],
            Doc(
                """
                `Lifespan` manages app resources, running code on startup and shutdown.
                """
            ),
        ],
    ) -> None:
        self.title: str = title
        self.lifespan: Lifespan[AppType] = lifespan

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...
