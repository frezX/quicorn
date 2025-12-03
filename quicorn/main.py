from pathlib import Path

from pydantic import IPvAnyAddress, ConfigDict, validate_call

from quicorn.app import AppType
from quicorn.config import Config
from quicorn.server import Server


@validate_call(config=ConfigDict(arbitrary_types_allowed=True))
def run(
    app: AppType,
    host: IPvAnyAddress | str = 'localhost',
    port: int = 80,
    certfile: Path = Path('keys/cert.pem'),
    keyfile: Path = Path('keys/key.pem'),
    password: str | None = None,
) -> None:
    config: Config = Config(
        host=host,
        port=port,
        certfile=certfile,
        keyfile=keyfile,
        password=password,
    )
    server: Server = Server(app=app, config=config)
    server.run()
