from pathlib import Path
from ssl import VerifyMode

from pydantic import IPvAnyAddress, ConfigDict, validate_call

from aioquic.quic.packet import QuicProtocolVersion
from aioquic.quic.configuration import SMALLEST_MAX_DATAGRAM_SIZE

from quicorn.server import Server
from quicorn.graceful import event_loop_factory
from quicorn.types import QSGIApplication, LoopFactory
from quicorn.config import Config, DEFAULT_QUIC_PROTOCOL_VERSIONS


@validate_call(config=ConfigDict(arbitrary_types_allowed=True, strict=True))
def run(
    app: QSGIApplication,
    loop_factory: LoopFactory = event_loop_factory,
    host: IPvAnyAddress | str = 'localhost',
    port: int = 80,
    debug: bool = False,
    workers: int = 1,
    certfile: Path = Path('keys/cert.pem'),
    keyfile: Path = Path('keys/key.pem'),
    password: str | bytes | None = None,
    connection_id_length: int = 8,
    idle_timeout: float = 60.0,
    max_data: int = 2**20,
    max_datagram_size: int = SMALLEST_MAX_DATAGRAM_SIZE,
    max_stream_data: int = 2**20,
    supported_versions: list[QuicProtocolVersion] | None = None,
    verify_mode: VerifyMode = VerifyMode.CERT_REQUIRED,
) -> None:
    config: Config = Config(
        host=host,
        port=port,
        debug=debug,
        workers=workers,
        certfile=certfile,
        keyfile=keyfile,
        password=password,
        connection_id_length=connection_id_length,
        idle_timeout=idle_timeout,
        max_data=max_data,
        max_datagram_size=max_datagram_size,
        max_stream_data=max_stream_data,
        supported_versions=supported_versions or DEFAULT_QUIC_PROTOCOL_VERSIONS.copy(),
        verify_mode=verify_mode,
    )
    server: Server = Server(app=app, config=config, loop_factory=loop_factory)
    server.run()
