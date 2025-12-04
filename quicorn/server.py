from asyncio import Runner

from quicorn.types import QSGIApplication, LoopFactory

from quicorn.config import Config


class Server:
    def __init__(self, app: QSGIApplication, config: Config, loop_factory: LoopFactory) -> None:
        self.app: QSGIApplication = app
        self.config: Config = config
        self._runner: Runner = Runner(debug=self.config.debug, loop_factory=loop_factory)

    def run(self) -> None:
        print(self.app)
        print(self.config)
        print(self._runner)
