from quicorn.app import QuicApp
from quicorn.config import Config


class Server:
    def __init__(self, app: QuicApp, config: Config) -> None:
        self.app: QuicApp = app
        self.config: Config = config

    def run(self) -> None:
        print(self.app)
        print(self.config)
