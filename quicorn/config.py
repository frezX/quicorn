from pathlib import Path
from ssl import VerifyMode
from typing import ClassVar

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    IPvAnyAddress,
    SecretStr,
    SecretBytes,
    conint,
    confloat,
)

from aioquic.quic.packet import QuicProtocolVersion
from aioquic.quic.configuration import SMALLEST_MAX_DATAGRAM_SIZE, QuicConfiguration

from quicorn.types import AlignedInt

DEFAULT_QUIC_PROTOCOL_VERSIONS: list[QuicProtocolVersion] = [
    QuicProtocolVersion.VERSION_1,
    QuicProtocolVersion.VERSION_2,
]


class Config(BaseModel):
    host: IPvAnyAddress | str = 'localhost'
    port: conint(ge=1, le=65535) = 80
    debug: bool = False
    workers: conint(ge=1, le=10) = 1
    certfile: Path = Path('keys/cert.pem')
    keyfile: Path = Path('keys/key.pem')
    password: SecretStr | SecretBytes | None = None
    connection_id_length: conint(ge=8) = 8
    idle_timeout: confloat(ge=10, multiple_of=.1) = 60.0
    max_data: AlignedInt = 2**20
    max_datagram_size: conint(ge=1200) = SMALLEST_MAX_DATAGRAM_SIZE
    max_stream_data: AlignedInt = 2**20
    supported_versions: list[QuicProtocolVersion] = Field(default_factory=lambda: DEFAULT_QUIC_PROTOCOL_VERSIONS.copy())
    verify_mode: VerifyMode = VerifyMode.CERT_REQUIRED

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True)

    @property
    def quic_configuration(self) -> QuicConfiguration:
        configuration: QuicConfiguration = QuicConfiguration(
            is_client=False,
            connection_id_length=self.connection_id_length,
            idle_timeout=self.idle_timeout,
            max_data=self.max_data,
            max_datagram_size=self.max_datagram_size,
            max_stream_data=self.max_stream_data,
            supported_versions=self.supported_versions,
            verify_mode=self.verify_mode,
        )
        configuration.load_cert_chain(
            certfile=self.certfile,
            keyfile=self.keyfile,
            password=self.password and self.password.get_secret_value(),
        )
        return configuration
