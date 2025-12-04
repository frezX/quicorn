from pathlib import Path

from pydantic import BaseModel, IPvAnyAddress, SecretStr, conint


class Config(BaseModel):
    host: IPvAnyAddress | str = 'localhost'
    port: conint(ge=1, le=65535) = 80
    certfile: Path = Path('keys/cert.pem')
    keyfile: Path = Path('keys/key.pem')
    password: SecretStr | None = None
    debug: bool = False
