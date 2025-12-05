from asyncio import Runner, Queue

from aioquic.asyncio import serve

from quicorn.config import Config
from quicorn.types import QSGIApplication, LoopFactory

from quicorn.graceful import SHUTDOWN_EVENT
from quicorn.qsgi.protocol import QSGIProtocol
from quicorn.qsgi.context import qsqi_queue_var


class Server:
    def __init__(self, app: QSGIApplication, config: Config, loop_factory: LoopFactory) -> None:
        self.app: QSGIApplication = app
        self.config: Config = config
        self.runner: Runner = Runner(debug=self.config.debug, loop_factory=loop_factory)

    async def serve(self) -> None:
        queue: Queue = qsqi_queue_var.get()
        await serve(
            str(self.config.host),
            self.config.port,
            configuration=self.config.quic_configuration,
            create_protocol=QSGIProtocol
        )
        while not SHUTDOWN_EVENT.is_set():
            event = await queue.get()
            print(f'Received event: {event}')

    def run(self) -> None:
        with self.runner:
            self.runner.run(self.serve())
