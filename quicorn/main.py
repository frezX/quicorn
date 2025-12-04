from pathlib import Path

from pydantic import IPvAnyAddress, ConfigDict, validate_call

from quicorn.types import QSGIApplication, LoopFactory

from quicorn.config import Config
from quicorn.server import Server
from quicorn.graceful import event_loop_factory


@validate_call(config=ConfigDict(arbitrary_types_allowed=True, strict=True))
def run(
    app: QSGIApplication,
    host: IPvAnyAddress | str = 'localhost',
    port: int = 80,
    certfile: Path = Path('keys/cert.pem'),
    keyfile: Path = Path('keys/key.pem'),
    password: str | None = None,
    debug: bool = False,
    loop_factory: LoopFactory = event_loop_factory,
) -> None:
    config: Config = Config(
        host=host,
        port=port,
        certfile=certfile,
        keyfile=keyfile,
        password=password,
        debug=debug,
    )
    server: Server = Server(app=app, config=config, loop_factory=loop_factory)
    server.run()
