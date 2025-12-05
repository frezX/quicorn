from asyncio import Runner

from quicorn.config import Config
from quicorn.types import QSGIApplication, LoopFactory

from quicorn.graceful import SHUTDOWN_EVENT


class Server:
    def __init__(self, app: QSGIApplication, config: Config, loop_factory: LoopFactory) -> None:
        self.app: QSGIApplication = app
        self.config: Config = config
        self.runner: Runner = Runner(debug=self.config.debug, loop_factory=loop_factory)

    async def _run(self) -> None:
        await SHUTDOWN_EVENT.wait()

    def run(self) -> None:
        with self.runner:
            self.runner.run(self._run())
